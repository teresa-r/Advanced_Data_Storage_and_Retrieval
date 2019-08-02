
import pandas as pd
import numpy as np
import datetime as dt


import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement= Base.classes.measurement
Station= Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

##Find the latest_date ----------------> ('2017-08-23')
latest_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
latest_date
##Assign period range to query
query_period=(dt.date(2017,8,23))-dt.timedelta(days=365)
measurement_table=session.query(Measurement.date,Measurement.prcp).\
                    filter(Measurement.date>=query_period).\
                    order_by(Measurement.date).all()

#declear date for variable for last 12 month 

last_year='2016-08-23'

####################################################################################################################
# Home page.
@app.route("/")
# List all routes that are available.
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )

####################################################################################################################
# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
# Convert the query results to a Dictionary using date as the key and prcp as the value.
def precipitation():
    session=Session(engine)
    prcp_results=session.query(Measurement.date, Measurement.prcp).all()
    # prcp_result= session.query(Measurement.date, func.avg(Measurement.prcp)).\
    #             filter(Measurement.date >= last_year).\
    #             group_by(Measurement.date).all()

# Return the JSON representation of your dictionary.
    return jsonify (prcp_results)



####################################################################################################################
# /api/v1.0/stations
@app.route("/api/v1.0/station")
def station():
    session=Session(engine)
    station_results=session.query(Station.station, Station.name).all()

# Return a JSON list of stations from the dataset.
    all_stations=list(np.ravel(station_results))
    return jsonify (all_stations)
    

# ####################################################################################################################    
# # /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
# query for the dates and temperature observations from a year from the last data point.
def tobs():
    query_period=(dt.date(2017,8,23))-dt.timedelta(days=365)
    session=Session(engine)
    query_tobs=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=query_period).order_by(Measurement.date).all()
    
# Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify (query_tobs)



# ####################################################################################################################
# # /api/v1.0/<start> 
# # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<date>")
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
def start_date(date):

    cannonicalized=date.replace(" ", "").lower()
    for charater in measurement_table:
        search_date= charater["date"].replace(" ", "").lower()

        if search_date== cannonicalized:
            return jsonify(charater)
    
    return jsonify({"error":f"Character with date{date} not found."}),404

    # startDate=(dt.date(2017,8,23))-dt.timedelta(days=365)
    # day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= startDate).all()



####################################################################################################################
if __name__== "__main__":
    app.run(debug=True)


