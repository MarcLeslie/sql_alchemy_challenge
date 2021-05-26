import numpy as np
import sqlalchemy
import os 
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#### Database Setup CHANGE WHERE THE DATABASE POINTS TO ####
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
#print(Base.classes.keys())
measurements = Base.classes.measurement 
stations = Base.classes.station

#### Flask Setup ####
app = Flask(__name__)

#### Flask Routes ####

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        #f"/api/v1.0/&lt;start&gt;<br/>" #ACCORDING TO ASK BCS
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; [NOTE: FORMAT IS yyyy-mm-dd] <br/>"
    )

#### DONT CHANGE ANYTHING ABOVE THIS ONCE IT IS WORKING ####
    
################ PRECIP ##############

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    last_date = session.query(measurements.date).order_by(measurements.date.desc()).first()
    year_ago = dt.datetime.strptime(str(last_date[0]), "%Y-%m-%d") - dt.timedelta(days=365)
    year_limit = session.query(measurements.date, measurements.prcp).filter(measurements.date >= year_ago).order_by(measurements.date).all()
    session.close()
       
    # Create a dictionary from the row data and append to a list
    all_precip = []
    for date, prcp in year_limit:
        all_precip_dict = {}
        all_precip_dict[date] = prcp
        all_precip.append(all_precip_dict)

    return jsonify(all_precip) #### this is the final step of the method that started with def precipitaiton(): ####

################ ALL STATIIONS ##############
@app.route("/api/v1.0/stations")
def stations2():
    session = Session(engine)
    results = session.query(stations.name, stations.station).all()
    session.close()

    all_stations=[]

    for name, station in results:
        all_stations_dict={}
        all_stations_dict[name] = station 
        all_stations.append(all_stations_dict)

    return jsonify(all_stations)

################ MOST ACTIVE ##############

@app.route("/api/v1.0/tobs")
def tobias_funke():
    session = Session(engine)
    most_active = session.query(measurements.date).filter(measurements.station == "USC00519281").order_by(measurements.date.desc()).first()
    year_ago2 = dt.datetime.strptime(str(most_active[0]), "%Y-%m-%d") - dt.timedelta(days=365)
    year_limit = session.query(measurements.date, measurements.prcp).filter(measurements.date >= year_ago2).order_by(measurements.date).all()
    session.close()
       
    so_very_active = []
    for date, prcp in year_limit:
        so_very_active_dict = {}
        so_very_active_dict[date] = prcp
        so_very_active.append(so_very_active_dict)

    return jsonify(so_very_active) #### this is the final step of the method that started with def precipitaiton(): ####

################ START/END ##############

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start_end(start=None, end=None): 
    session = Session(engine) 
    three_temps = [func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)]
    if not end:
       results = session.query(*three_temps).\
       filter(measurements.date <= start).all()
       temps = list(np.ravel(results))
       return jsonify(temps)

    results = session.query(*three_temps).\
    filter(measurements.date >= start).\
    filter(measurements.date <= end).all()
    temps = list(np.ravel(results))

    return jsonify(temps=temps)

#THIS GOES AT THE VERY, VERY END!  IF NOT IT WILL TERMINATE THE API OR WHATEVER IT IS EARLY
if __name__ == '__main__':
    app.run(debug=True)