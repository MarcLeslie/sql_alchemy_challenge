import numpy as np
import sqlalchemy
import os 

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
def Measurement():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all 
    results = session.query(measurements.date, measurements.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    all_precip = []
    for date, prcp in results:
        all_precip_dict = {}
        all_precip_dict["date"] = date
        all_precip_dict["prcp"] = prcp
        all_precip.append(all_precip_dict)

    return jsonify(all_precip)


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
