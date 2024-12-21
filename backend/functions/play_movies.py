

def get_streaming_availability(title):
    """Fetches streaming availability for a given show or movie title."""
    try:
        encoded_title = urllib.parse.quote(title)  # Safely encode the title
        conn = http.client.HTTPSConnection("streaming-availability.p.rapidapi.com")
        conn.request("GET", f"/shows/search/title?title={encoded_title}&country={COUNTRY_CODE}&output_language=en", headers=STREAMING_API_HEADERS)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    except Exception as e:
        print(f"An error occurred while fetching streaming info: {e}")
        return None

def play_movie(movie_name):
    """Handles the request to play a movie by fetching its streaming availability."""
    print(f"Fetching streaming availability for the movie: {movie_name}")
    streaming_info = get_streaming_availability(movie_name)
    print(f"Streaming info for '{movie_name}': ")

    pprint.PrettyPrinter(streaming_info)
    return streaming_info
