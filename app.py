from flask import Flask, render_template, request, jsonify
from restaurant_data.restaurant_data import get_restaurants
import requests
import json
import sqlite3

app = Flask(__name__)

# Google Places API endpoint
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Your API key
API_KEY = 'AIzaSyBYpv8vSSnXke0jFdLYWN-AmLuAbIFfq3U'

# Function to get restaurants near a location

# Route to display homepage
@app.route('/')
def index():
    return render_template('index.html')

# Function to fetch restaurant data
def get_restaurants(latitude, longitude, radius=10000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': 'restaurant',
        'key': API_KEY 
    }

    # Add referer header to avoid errors
    headers = {'referer': 'https://yourwebsite.com'}  # Replace with your website's URL

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Error: {response.status_code}")
        return None

# Flask route to handle API requests
@app.route('/get_restaurants', methods=['GET'])
def get_restaurants_api():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    radius = request.args.get('radius', 10000)

    if latitude and longitude:
        restaurants = get_restaurants(latitude, longitude, radius)
        if restaurants:
            return jsonify(restaurants)
        else:
            return jsonify({'error': 'No restaurants found'})
    else:
        return jsonify({'error': 'Missing latitude and longitude'})


@app.route('/submit', methods=['POST'])
def submit():
    restaurant_name = request.form['restaurant']
    # Process the restaurant name, e.g., store it in a database
    # ...
    return f"Received: {restaurant_name}"

if __name__ == '__main__':
    app.run(debug=True)
