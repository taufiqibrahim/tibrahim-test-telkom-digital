from typing import Dict
import csv
import haversine
import json
import requests

BASE_URL = 'http://api.weatherapi.com/v1'
FORECAST_API = 'forecast.json'
API_KEY = '2cabd5a38d1049769e3133656211610'  # TODO: move to env
CITIES_FILE = './cities.csv'
DEBUG = False

print(f'DEBUG={DEBUG}')


def get_forecast(city_data: Dict, days: int = 1, mode: str = 'coordinate', debug: bool = False) -> Dict:
    if mode == 'city':
        q = city_data['Name']
    else:
        q = f"{city_data['Latitude']},{city_data['Longitude']}"

    payload = {
        "key": API_KEY,
        "q": q,
        "days": days,
        "aqi": "no",
        "alerts": "no",
    }
    # TODO: if needed add retry-backoff handler
    response = requests.get(f"{BASE_URL}/{FORECAST_API}", params=payload)
    data = response.json()

    if response.status_code >= 400:
        print(f"ERROR {response.status_code} for {city_data}")
        return {}
    elif data:
        distance = haversine.haversine(
            (float(city_data['Latitude']), float(city_data['Longitude'])),
            (data['location']['lat'], data['location']['lon'])
        )
        data['_validation'] = {
            'corrdinate_distance_between_request_response_km': distance,
        }

        if debug:
            print(data)
        return data
    else:
        print(f"Warning empty result for {city_data}")
        return {}


# Get cities from CSV, no Pandas required here
with open(CITIES_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    cities = list()
    for row in reader:
        cities.append(row)

# Get weather forecast data
num_cities = len(cities)
weather_forecasts = list()
for i, city in enumerate(cities[:]):
    print(F"({i + 1}/{num_cities}) Processing {city['Name']}")
    forecast_data = get_forecast(
        city_data=city, mode='coordinate', debug=DEBUG)
    # print(forecast_data.get("location"), forecast_data.get('_validation'))
    weather_forecasts.append(forecast_data)

# write to JSON file
with open('./result.json', 'w') as fjson:
    json_obj = json.dumps(weather_forecasts, indent=2)
    fjson.write(json_obj)
