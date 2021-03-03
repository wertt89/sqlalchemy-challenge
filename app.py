import numpy as np

import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

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
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of all dates and precipitation data"""
    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Return the JSON representation of your dictionary.
    all_date_prcp = []
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        all_date_prcp.append(date_prcp_dict)

    return jsonify(all_date_prcp)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of all stations names"""
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Return a JSON list of stations from the dataset.
    all_stations = []
    for station, name in results:
        all_stations_dict = {}
        all_stations_dict["station"] = station
        all_stations_dict["name"] = name
        all_stations.append(all_stations_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latestdate = dt.datetime.strptime(lateststr, '%Y-%m-%d')
    querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)
    sel = [Measurement.date,Measurement.tobs]
    queryresult = session.query(*sel).filter(Measurement.date >= querydate).all()
    session.close()

    tobsall = []
    for date, tobs in queryresult:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

if __name__ == "__main__":
    app.run(debug=True)