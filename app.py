# import Flask
from flask import Flask, jsonify

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, Date
import os

# reflect an existing database into a new model
Base = automap_base()
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect the tables
Base.prepare(engine, reflect=True)

# print all the classes to reflect the database tables
Base.classes.keys()

# We can view all of the classes that automap found
Station = Base.classes.station
Measurement = Base.classes.measurement

# create a session
session = Session(engine)

# Save references to precipitation
Base.prepare(engine, reflect=True)
results = session.query(Measurement.date, Measurement.prcp)
df = pd.DataFrame(results[:], columns=['Measurement.date', 'Measurement.prcp'])
_dict = {}
for index, row in df.iterrows():
    _dict[row['Measurement.date']] = row['Measurement.prcp']

# Save reference to stations
station = session.query(Measurement.date, Measurement.station)
df_station = pd.DataFrame(station[:], columns=['Measurement.date','Measurement.station'])
station_list = df_station['Measurement.station'].unique().tolist()

_dict_station = {}
_dict_station['station'] = station_list
print(_dict_station)


# create an app for precipitation
app = Flask(__name__)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""

    return jsonify(_dict)

@app.route("/api/v1.0/stations")
def station():
    """Return the station data as json"""
    return jsonify(_dict_station)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation:<br/>"
        f"/api/v1.0/stations:<br/>"

    )


if __name__ == "__main__":
    app.run(debug=True)
