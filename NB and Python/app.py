import numpy as np
import sqlalchemy
import os 
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup CHANGE WHERE THE DATABASE POINTS TO
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# # reflect the tables
Base.prepare(engine, reflect=True)
#print(Base.classes.keys())
# # Save reference to the table
measurements = Base.classes.measurement 
stations = Base.classes.station

# #################################################
# # Flask Setup
# #################################################
app = Flask(__name__)

# #################################################
# # Flask Routes DONT CHANGE ANYTHING ABOVE THIS
# #################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/start/end<br/>"
    )

# #################################################
# # DONT CHANGE ANYTHING ABOVE THIS
# #################################################
    
################ PRECIP ##############
# Convert query results to a dict using date as key and prcp as value
# Return the json rep of the dict

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

########### ALL STATIONS ####################
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

############ MOST ACTIVE #########################
# date/temp of most active for last year 

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

############ START ROUTE ###############
# Route accepts the start date as a parameter from the URL
# Returns min, max, and avg temp calculated from given start date to end of the dataset
@app.route("/api/v1.0/<start>")
def whatever(start=None):
    session = Session(engine)
    results = session.query(stations.name, stations.station, measurements.date).filter(measurements.date > start).all()
    session.close()

    cats=[]

    for name, station, date in results:
        cats_dict={}
        cats_dict[date] = station, name 
        cats.append(cats_dict)

    return jsonify(cats)






############# START/END ROUTE ##############
# Route accepts the start and end dates as parameters from the URL
# Returns min, max, and avg temp calculated from given start date to end of the dataset
#@app.route("/api/v1.0/start/end")








#THIS GOES AT THE VERY, VERY END!  IF NOT IT WILL TERMINATE THE API OR WHATEVER IT IS EARLY
if __name__ == '__main__':
    app.run(debug=True)





################THIS IS A TEMPLATE ##############
################# DELETE THIS WHEN DONE ##############
# @app.route("/api/v1.0/precipitation")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


# if __name__ == '__main__':
#     app.run(debug=True)
