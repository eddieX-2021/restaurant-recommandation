import requests
import pandas as pd

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

def save_restaurants_to_csv(restaurants, filename='restaurants_data.csv'):
    # Create a list of dictionaries for each restaurant
    restaurant_data = []
    for restaurant in restaurants:
        restaurant_data.append({
            'name': restaurant.get('name'),
            'rating': restaurant.get('rating', 'N/A'),
            'lat': restaurant['geometry']['location']['lat'],
            'lng': restaurant['geometry']['location']['lng'],
            'vicinity': restaurant.get('vicinity', 'N/A'),
            'price_level': restaurant.get('price_level', 'N/A'),
            'types': ', '.join(restaurant.get('types', []))
        })
    
    # Create a DataFrame from the list
    df = pd.DataFrame(restaurant_data)
    
    # Save DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')


latitude = 38.003155
longitude = -78.494190
restaurants = get_restaurants(latitude, longitude)
save_restaurants_to_csv(restaurants)