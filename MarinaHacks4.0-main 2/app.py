from flask import Flask, request, jsonify, render_template, send_from_directory
import requests, json
import os
app = Flask(__name__)
#Opening file with campus places and corresponding lat & long
with open ("cafe_places.json") as f:
        cafe_places = json.load(f)

API_KEY = 'AIzaSyCQPGwg0hxpYHJoc0OHob_MYo5iOms5Fsg'
@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/cafe_places', methods = ['GET'])
def get_campus_places():
    return jsonify(cafe_places)

@app.route('/directions', methods=['GET'])
def get_directions():
    end_name = request.args.get('end')  # Example: 'V Cafe'

    end_location = None
    for place in cafe_places:
        if place['name'] == end_name:
            end_location = place['location']
            break

    if end_location is None:
        return jsonify({'error': 'Cafe location not found'}), 400  # Added status code 400 for clarity

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin=33.78193619731233,-118.11484054578304&destination={end_location['lat']},{end_location['long']}&mode=driving&key={API_KEY}"

    # Make a request to Google Maps API
    try:
        goog_map_response = requests.get(url)
        goog_map_response.raise_for_status()  # Raise an error for bad responses
    except requests.exceptions.RequestException as err:
        return jsonify({'error': f'Failed to connect to Google Maps API: {err}'}), 500

    # Parse the response
    directions_data = goog_map_response.json()
    if directions_data.get('status') != 'OK':
        return jsonify({"error": "Unable to find directions"}), 400  # Fixed the misplaced comma

    # Extract directions steps
    steps = directions_data['routes'][0]['legs'][0]['steps']
    directions = [step['html_instructions'] for step in steps]

    return jsonify(directions)
