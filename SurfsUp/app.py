import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Write homepage and define all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"insert date search in year-m-d format<br/>"
        f"/api/v1.0/<start><br/>"
        f"insert date range in year-m-d/year-m-d format<br/>"
        f"/api/v1.0/<start>/<end>"
    )

# write out route for precipitation
@app.route("/api/v1.0/precipitation")
def date():

    # start session and connect to engine
    session = Session(engine)

    # create variable to hold date from one year ago 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # create variable to hold date and precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= year_ago).all()
    
    # close session
    session.close()

    # run precipitaiton data as dictionary
    prcp = dict(results)

    # return precipitation data
    return jsonify(prcp)

# write out route for stations
@app.route("/api/v1.0/stations")
def stations():

    # start session and connect to engine
    session = Session(engine)

    # create variable to hold station data
    results = session.query(Measurement.station).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # close session
    session.close()

    # run station names as list
    station_names = list(np.ravel(results))

    # return station names
    return jsonify(station_names)

# write out route for temperature
@app.route("/api/v1.0/tobs")
def dates():

    # start session and connect to engine
    session = Session(engine)

    # create variable to hold date from one year ago
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # create variable to hold most active station's temperature and date data
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281', Measurement.date >= year_ago).all()

    # close session
    session.close()

    # run temperature observations as list
    temp_obv = list(np.ravel(results))

    # return temp observations
    return jsonify(temp_obv)

# write dynamic route for any start date
@app.route("/api/v1.0/<start>")
def date_start(start):
     
     # start session and connect to engine
     session = Session(engine)

     # define start date input
     start_dt = dt.datetime.strptime(start, '%Y-%m-%d')

     # create variable to run min, max, and avg temperature for all dates from a specified start date to the end of the data set
     results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
     .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_dt)\
     .group_by(Measurement.date).all()

     # close session
     session.close()

     # create temperature variable to hold all data
     temps = []

     # create for loop to run through all temperature data
     for ts in results:
         date_dict = {}
         date_dict["Date"] = ts[0]
         date_dict["Temp: Low"] = ts[1]
         date_dict["Temp: Max"] = ts[2]
         date_dict["Temp: Avg"] = ts[3]
         temps.append(date_dict)
     return jsonify(temps)

# write dynamic route for any start date to any end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
     
     # start session and connect to engine
     session = Session(engine)

     # define start/end date input
     start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
     end_dt = dt.datetime.strptime(end, '%Y-%m-%d')

     # create variable to run min, max, and avg temperature for all dates from a specified start date to a specified end date
     results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)) \
     .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_dt, func.strftime("%Y-%m-%d", Measurement.date) <= end_dt)\
     .group_by(Measurement.date).all()

     # close session
     session.close()

     # create temperature range variable to hold all data
     temps_range = []

     # create for loop to run through all temperature data
     for ts in results:
         dates_dict = {}
         dates_dict["Date"] = ts[0]
         dates_dict["Temp: Low"] = ts[1]
         dates_dict["Temp: Max"] = ts[2]
         dates_dict["Temp: Avg"] = ts[3]
         temps_range.append(dates_dict)
     return jsonify(temps_range)

if __name__ == '__main__':
    app.run(debug=True)