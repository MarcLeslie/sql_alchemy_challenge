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

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")


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


    
################CHANGE SHIT UP HERE AND LOOK AT HW TO CHANGE THIS SHIT UP  THEN COPY AND MODIFY SHIT TO MEET THE REQUIREMENTS##############
@app.route("/api/v1.0/precipitation")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
