# recommendation_system.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process  #used for find similar restuarant that user typed in 


# Load your dataset
df = pd.read_csv('c.csv')



def preprocess_name(name):
    return name.strip().lower()

#we are going to run 1-3 time to find the closet restaurant and put it in a list
def find_closest_restaurant(user_input, df):
    processed_input = preprocess_name(user_input)
    
    # Use fuzzy matching to find the closest match
    closest_match = process.extractOne(processed_input, df['name'])
    
    if closest_match:
        matched_name = df[df['name'] == closest_match[0]]['name'].values[0]
        return matched_name
    else:
        return None

# Example user input
#future changes here is based on the database we have from webiste input, we add the restuarnt into this list
user_input = "mellow"
matched_restaurant = find_closest_restaurant(user_input, df)

# Find the index of the matched restaurant in df
if matched_restaurant:
    # Get index of the matched restaurant in df (this assumes names are unique in df)
    matched_index = df[df['name'] == matched_restaurant].index
    
    # Check if matched_index exists and convert it to a list of liked restaurant indices
    if not matched_index.empty:
        liked_restaurants_indices = matched_index.tolist()
    else:
        liked_restaurants_indices = []

    # Add matched_index to a list for similarity recommendations
    user_prev_restaurant = liked_restaurants_indices
    print(f"Matched Restaurant: {matched_restaurant} at index {user_prev_restaurant}")
else:
    print("No matching restaurant found.")


# Calculate cosine similarity based on relevant features in df
features_df = df.drop(['name'], axis=1, errors='ignore')
similarity_matrix = cosine_similarity(features_df)

# Define recommendation function
def recommend_restaurants(restaurant_indices, similarity_matrix, top_n=5):
    similarity_scores = similarity_matrix[restaurant_indices].sum(axis=0)
    similar_restaurants_indices = similarity_scores.argsort()[-top_n-1:-1][::-1]
    return df.iloc[similar_restaurants_indices]['name'].tolist()

# Get recommended restaurants based on matched index
if user_prev_restaurant:
    recommended_restaurants = recommend_restaurants(user_prev_restaurant, similarity_matrix)
    print("Recommended Restaurants:", recommended_restaurants)
else:
    print("No liked restaurants found for recommendation.")