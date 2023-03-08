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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def date():

    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= year_ago).all()
    
    session.close()

    prcp = dict(results)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    results = session.query(Measurement.station).\
        group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    station_names = list(np.ravel(results))

    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def dates():

    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281', Measurement.date >= year_ago).all()

    session.close()

    temp_obv = list(np.ravel(results))

    return jsonify(temp_obv)

if __name__ == '__main__':
    app.run(debug=True)