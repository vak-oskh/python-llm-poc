import os
from dotenv import load_dotenv

# Load client IDs
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# token to get the user profile using client_id and client_secret
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)

    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Function to get authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


#putting a variable to get the token of the user
token = get_token()


def play_music(token, song_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": song_name,
        "type": "track",
        "limit": 1  # Number of results to return currently most played in spotify
    }

    result = get(url, headers=headers, params=params)
    if result.status_code == 200:
        json_result = result.json()
        tracks = json_result['tracks']['items']

        if len(tracks) > 0:
            track = tracks[0]  # Get the first track in the list
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            spotify_url = track['external_urls']['spotify']

            os.system(f'start {spotify_url}')
            print(f"Playing '{track_name}' by {artist_name}. Listen here: {spotify_url}")
        else:
            print("No results found.")
    else:
        print(f"Failed to search for the song: {result.status_code}")
