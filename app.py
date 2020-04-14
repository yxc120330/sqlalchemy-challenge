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


Base.prepare(engine, reflect=True)

##########################################################################################################################

#Json file 

#Convert the query results to a dictionary using date as the key and prcp as the value
results = session.query(Measurement.date, Measurement.prcp)
df = pd.DataFrame(results[:], columns=['Measurement.date', 'Measurement.prcp'])
_dict = {}
for index, row in df.iterrows():
    _dict[row['Measurement.date']] = row['Measurement.prcp']

# Return a JSON list of stations from the dataset
station = session.query(Measurement.date, Measurement.station)
df_station = pd.DataFrame(station[:], columns=['Measurement.date','Measurement.station'])
station_list = df_station['Measurement.station'].unique().tolist()

_dict_station = {}
_dict_station['station'] = station_list
print(_dict_station)

#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

query_most_active_station = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station== 'USC00519281').filter(Measurement.date>='2016-08-23').filter(Measurement.date<='2017-08-22').statement
df_active_station = pd.read_sql_query(query_most_active_station,session.bind)
tobs = df_active_station['tobs'].tolist()
_dict_tobs = {}
_dict_tobs["tobs"]= tobs













###########################################################################################################################################

##################################### Flask Setup##########################################
app = Flask(__name__)

###################################### Flask Route#########################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""

    return jsonify(_dict)

@app.route("/api/v1.0/stations")
def station():
    """Return the station data as json"""
    return jsonify(_dict_station)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the tobs data as json"""
    return jsonify(_dict_tobs)




@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        
        f"<br/>"
        
        f"/api/v1.0/precipitation:<br/>"
        f"return precipitation for all years"
        
        f"<br/>"
        
        f"/api/v1.0/stations:<br/>"
        f"return all available station"
        
        f"<br/>"
        
        f"/api/v1.0/tobs:<br/>"
        f"return temperature observation from the most active station for the last year of data"
        
        f"<br/>"
        
    )


if __name__ == '__main__':
    app.run(debug=True)
