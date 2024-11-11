import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process

# Load the dataset (only load this once in your app, or pass it as needed to avoid reloading)
df = pd.read_csv('notbooks\c.csv')

# Preprocess the dataset to create the similarity matrix (run once for the app)
features_df = df.drop(['name'], axis=1, errors='ignore')
similarity_matrix = cosine_similarity(features_df)

# Preprocess name for consistency
def preprocess_name(name):
    return name.strip().lower()

# Find the closest matching restaurant
def find_closest_restaurant(user_input, df):
    processed_input = preprocess_name(user_input)
    closest_match = process.extractOne(processed_input, df['name'])
    if closest_match:
        matched_name = closest_match[0]
        matched_index = df[df['name'] == matched_name].index
        return matched_index.tolist()
    else:
        return []

# Recommend top 5 similar restaurants
def recommend_restaurants(restaurant_indices, similarity_matrix, df, top_n=10):
    similarity_scores = similarity_matrix[restaurant_indices].sum(axis=0)
    similar_restaurants_indices = similarity_scores.argsort()[-top_n-1:-1][::-1]
    return df.iloc[similar_restaurants_indices]['name'].tolist()

def get_recommendations(user_inputs):
    # Collect indices for all restaurants provided by the user
    all_indices = []
    for user_input in user_inputs:
        restaurant_indices = find_closest_restaurant(user_input, df)
        all_indices.extend(restaurant_indices)  # Collect all matched indices

    # Ensure there are indices to recommend from
    if all_indices:
        return recommend_restaurants(all_indices, similarity_matrix, df)
    else:
        return ["No matching restaurants found."]
    
# Example usage
# user_inputs = ["mellow", "chipolte", "dunkin"]
# recommendations = get_recommendations(user_inputs)
# print("Recommended Restaurants:", recommendations)