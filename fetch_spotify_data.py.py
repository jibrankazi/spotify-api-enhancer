import requests
import pandas as pd
import time

# Your Client ID and Client Secret
client_id = '12edcb01e437450c8785cf976cc8025f'
client_secret = 'fd0891dad7e9437fb6159259bdc3c31d'

# Get the access token
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
)

# Check if the request was successful
if auth_response.status_code == 200:
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
else:
    # Print the response for debugging
    print("Failed to get access token")
    print("Status Code:", auth_response.status_code)
    print("Response:", auth_response.json())
    raise Exception("Failed to authenticate with Spotify API")

# Function to get track ID and album cover URL from Spotify
def get_spotify_data(track_name, artist_name):
    search_url = f"https://api.spotify.com/v1/search"
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q': f'track:{track_name} artist:{artist_name}',
        'type': 'track',
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['tracks']['items']:
            track_id = data['tracks']['items'][0]['id']
            album_cover_url = data['tracks']['items'][0]['album']['images'][0]['url']
            return track_id, album_cover_url
    else:
        # Print the response for debugging
        print(f"Failed to retrieve data for {track_name} by {artist_name}")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    return None, None

# Load your dataset
file_path = 'C:\\Users\\jibra\\OneDrive\\Desktop\\Power BI\\spotify\\spotify-2023.csv'
spotify_df = pd.read_csv(file_path, encoding='latin1')

# Add columns for track ID and album cover URL
spotify_df['track_id'] = None
spotify_df['album_cover_url'] = None

# Loop through the dataframe and fetch data from Spotify API
for index, row in spotify_df.iterrows():
    track_id, album_cover_url = get_spotify_data(row['track_name'], row['artist(s)_name'])
    spotify_df.at[index, 'track_id'] = track_id
    spotify_df.at[index, 'album_cover_url'] = album_cover_url
    time.sleep(0.1)  # To avoid rate limiting

# Save the updated dataframe
output_path = 'C:\\Users\\jibra\\OneDrive\\Desktop\\Power BI\\spotify\\updated_spotify_dataset.csv'
spotify_df.to_csv(output_path, index=False)

print("Dataset updated successfully.")
