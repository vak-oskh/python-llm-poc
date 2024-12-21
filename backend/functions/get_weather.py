import openmeteo_requests
import requests
from retry_requests import retry

####### Needs cleaning up return data #########
# EX. {'temprature': 9.267499923706055, 'weather_code': 51, 'weather_description': 'Drizzle: Light, moderate, and dense intensity'}
# return needs to be a rounded temp

# Main function to fetch weather
# the Open-Meteo API: https://open-meteo.com/en/docs
# return current_weather_data {
#   temprature,
#   weather_code,
#   weather_description
# }


def get_weather():
    # Get current location
    latitude, longitude, city = get_current_location()

    # 1. Setup the Open-Meteo API client with cache (it creates .chache file)
    # cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    # retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    # 2. Setup the Open-Meteo API client WITHOUT cache
    session = requests.Session()
    retry_session = retry(session, retries=5, backoff_factor=0.2)

    openmeteo = openmeteo_requests.Client(session=retry_session)

    if latitude is None or longitude is None:
        print("Unable to get current location.")
        return

    # Open-Meteo API parameters for current weather
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "weather_code"]
    }

    # Make the API request
    try:
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        print("response", response)

        # Get current weather
        current = response.Current()

        current_temperature_2m = current.Variables(0).Value()
        current_weather_code = int(current.Variables(1).Value())

        # Map with 'weather code' and 'description'
        def map_weather_code(code):
            match code:
                case 0:
                    return "Clear sky"
                case 1 | 2 | 3:
                    return "Mainly clear, partly cloudy, and overcast"
                case 45 | 48:
                    return "Fog and depositing rime fog"
                case 51 | 53 | 55:
                    return "Drizzle: Light, moderate, and dense intensity"
                case 56 | 57:
                    return "Freezing Drizzle: Light and dense intensity"
                case 61 | 63 | 65:
                    return "Rain: Slight, moderate, and heavy intensity"
                case 66 | 67:
                    return "Freezing Rain: Light and heavy intensity"
                case 71 | 73 | 75:
                    return "Snow fall: Slight, moderate, and heavy intensity"
                case 77:
                    return "Snow grains"
                case 80 | 81 | 82:
                    return "Rain showers: Slight, moderate, and violent"
                case 85 | 86:
                    return "Snow showers: Slight and heavy"
                case 95:
                    return "Thunderstorm: Slight or moderate"
                case 96 | 99:
                    return "Thunderstorm with slight and heavy hail"
                case _:
                    return "Unknown weather condition"

        weather_description = map_weather_code(current_weather_code)

        current_weather_data = {
            "temprature": current_temperature_2m,
            "weather_code": current_weather_code,
            "weather_description": weather_description
        }

        print("current_weather_data", current_weather_data)

    except Exception as e:
        print(f"Error fetching weather data: {e}")

    return current_weather_data


# Sample for Getting current location's latitude, longitude and city name using IP geolocation
# return latitude, longitude, city_name
def get_current_location():
    try:
        response = requests.get("http://ip-api.com/json/").json()
        latitude = response.get("lat")
        longitude = response.get("lon")
        city = response.get("city")
        return latitude, longitude, city
    except Exception as e:
        print(f"Error getting location: {e}")
        return None, None, None

