
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

last_year='2016-08-24'

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
        f"/api/v1.0/start_date/end_date"

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
    all_prcp=list(np.ravel(prcp_results))
    return jsonify (all_prcp)



####################################################################################################################
# /api/v1.0/stations
# @app.route("/api/v1.0/station")
# def station():
#     station_result=session.query(Station.station, Station.name).all()

# # Return a JSON list of stations from the dataset.
#     return jsonify (station_result)
    

# ####################################################################################################################    
# # /api/v1.0/tobs
# @app.rounte("/api/v1.0/tobs")
# # query for the dates and temperature observations from a year from the last data point.
# def tobs():
#     query_tobs=session.query(Measurement.station, Measurement.tobs).\
#             filter(Measurement.station==top_station).\
#             filter(Measurement.date>=query_period).all() 

# # Return a JSON list of Temperature Observations (tobs) for the previous year.
#     return jsonify (query_tobs)



# ####################################################################################################################
# # /api/v1.0/<start> and /api/v1.0/<start>/<end>
# # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# @app.rounte("/api/v1.0/start_date/end_date")
# # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# def start_date():
#     return(f"")


# ####################################################################################################################
# @app.rounte("/api/v1.0/end_date")
# # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# def end_date():
#     return(f"")




####################################################################################################################
if __name__== "__main__":
    app.run(debug=True)


