import requests

API_KEY = 'YOUR_GOOGLE_PLACES_API_KEY'
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

def get_restaurants(latitude, longitude, radius=1000):
    params = {
        'location': f'{latitude},{longitude}',
        'radius': radius,
        'type': 'restaurant',
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"Error: {response.status_code}")
        return None
