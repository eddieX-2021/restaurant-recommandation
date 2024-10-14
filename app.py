from flask import Flask, render_template, request, jsonify
from restaurant_data.restaurant_data import get_restaurants
import requests
import json

app = Flask(__name__)

# Google Places API endpoint
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Your API key
API_KEY = 'AIzaSyBKkfwtuXxMMysR7pYE3Vf6BW3ySsDp4uU'

# Function to get restaurants near a location
def get_restaurants(latitude, longitude, radius=1000):
    # Parameters for the API request
    params = {
        'location': f'{latitude},{longitude}',  # Location (latitude,longitude)
        'radius': radius,                        # Radius in meters (e.g., 1000m = 1km)
        'type': 'restaurant',                    # Type of place to search
        'key': API_KEY                           # Your API key
    }
    
    # Send the request to the Places API
    response = requests.get(url, params=params)
    
    # Parse the response
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print(f"Error: {response.status_code}")
        return None

# Route to display homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to get restaurant recommendations
@app.route('/get_restaurants', methods=['POST'])
def get_restaurant_data():
    try:
        # Get latitude, longitude, and radius from the request (sent from frontend)
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        radius = request.form.get('radius', 1000)  # default to 1000 meters
        
        # Fetch restaurants from Google Places API
        restaurants = get_restaurants(latitude, longitude, radius)
        
        # Return restaurant data as JSON to be displayed in the frontend
        return jsonify({'status': 'success', 'data': restaurants})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
