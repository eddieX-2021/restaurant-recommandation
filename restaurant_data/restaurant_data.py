import googlemaps
import pandas as pd
import time

# Your API key
API_KEY = 'AIzaSyBYpv8vSSnXke0jFdLYWN-AmLuAbIFfq3U'

# Initialize Google Maps Client
gmaps = googlemaps.Client(key=API_KEY)

def get_restaurants(latitude, longitude, radius=2000, max_results=1000):
    all_restaurants = []
    for lat_offset in range(-radius, radius, 500):  # Adjust the step to control how far you go
        for lng_offset in range(-radius, radius, 500):  # Same as above
            place_result = gmaps.places_nearby(
                location=(latitude + lat_offset / 100000, longitude + lng_offset / 100000),
                radius=radius,
                type='restaurant'
            )
            all_restaurants.extend(place_result.get('results', []))
            if len(all_restaurants) >= max_results:
                break
        if len(all_restaurants) >= max_results:
            break

    return all_restaurants



def save_restaurants_to_csv(restaurants, filename='restaurants_data.csv'):
    restaurant_data = []
    for restaurant in restaurants:
        restaurant_data.append({
            'name': restaurant.get('name'),
            'rating': restaurant.get('rating', 'N/A'),
            'lat': restaurant['geometry']['location']['lat'],
            'lng': restaurant['geometry']['location']['lng'],
            'vicinity': restaurant.get('vicinity', 'N/A'),
            'price_level': restaurant.get('price_level', 'N/A'),
            'types': ', '.join(restaurant.get('types', [])),
            'user_ratings_total': restaurant.get('user_ratings_total', 'N/A')
        })

    df = pd.DataFrame(restaurant_data)
    df.to_csv(filename, index=False)

    print(f'Data saved to {filename}')

# Test with latitude and longitude for New York City
latitude = 40.7128
longitude = -74.0060

latitude = 38.0293
longitude = -78.4767

# Get restaurants using googlemaps.Client
restaurants = get_restaurants(latitude, longitude)

# Check if restaurants were found and save them to a CSV file
if restaurants:
    save_restaurants_to_csv(restaurants)
else:
    print("No restaurants found.")



