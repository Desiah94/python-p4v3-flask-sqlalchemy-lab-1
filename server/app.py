#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = None

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
        return make_response(jsonify({'error': 'Earthquake not found'}), 404)

    # If an earthquake is found, return its attributes as a JSON string
    return jsonify({
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
