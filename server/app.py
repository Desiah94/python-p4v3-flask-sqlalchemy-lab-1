#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(jsonify(body), 200)

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    # Query the database for the earthquake with the specified ID
    earthquake = Earthquake.query.get(id)

    # If no earthquake is found, return an error message
    if earthquake is None:
        return make_response(jsonify({'message': f'Earthquake {id} not found.'}), 404)

    # If an earthquake is found, return its attributes as a JSON string
    return jsonify({
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year,
        'message': f'Earthquake {id} found.'
    })




@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with magnitudes greater than or equal to the parameter value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Count the matching rows
    count = len(earthquakes)

    # Prepare a list containing the data for each row
    earthquakes_data = [{
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year
    } for earthquake in earthquakes]

    # Return a JSON response containing the count and the list of earthquake data
    return jsonify({
        'count': count,
        'quakes': earthquakes_data  # Change 'earthquakes' to 'quakes'
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
