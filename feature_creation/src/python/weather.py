import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import datetime, timedelta
import requests

geolocator = Nominatim(user_agent="geoapi")


def get_lat_long(location: str):
    if location[-1].isdigit():
        location = location[:-2]
    if location == 'Queens Club':
        location = 'West Kensington London'
    try:
        loc = geolocator.geocode(location, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
        return None, None
    except GeocoderTimedOut:
        return None, None


def add_lat_long(matches: pd.DataFrame) -> pd.DataFrame:

    unique_locations = matches['tournament_location'].unique()
    location_dict = {location: get_lat_long(location) for location in unique_locations}

    location_dict['Cordoba'] = (-31.4, -64.183)
    location_dict['Santiago'] = (-33.45, -70.67)
    location_dict['Los Cabos'] = (22.883, -109.917)
    location_dict['Cologne 1'] = (50.933, 6.95)
    location_dict['Cologne 2'] = (50.933, 6.95)

    matches['latitude'] = matches['tournament_location'].map(lambda x: location_dict[x][0])
    matches['longitude'] = matches['tournament_location'].map(lambda x: location_dict[x][1])
    return matches


def get_weather(latitude, longitude, date, time, variables):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&hourly={','.join(variables)}&start_date={date}&end_date={date}&timezone=UTC"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None

    if not data.get("hourly"):
        print("No hourly data found:", url, data)
        return None

    datetime_str = f"{date}T{time}"
    for i, hourly_time in enumerate(data["hourly"]["time"]):
        if hourly_time == datetime_str:
            return {var: data["hourly"][var][i] for var in variables}

    return None


def convert_utc_plus1_to_utc(date, time):
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    dt_utc = dt - timedelta(hours=1)
    return dt_utc.strftime("%Y-%m-%d"), dt_utc.strftime("%H:%M")


def round_time_to_nearest_hour(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    if time_obj.minute >= 30:
        time_obj += timedelta(minutes=60 - time_obj.minute)
    else:
        time_obj -= timedelta(minutes=time_obj.minute)
    return time_obj.strftime("%H:00")


def fetch_weather_data(row):
    variables = ["temperature_2m", "relative_humidity_2m", "windspeed_10m", "apparent_temperature"]
    date_utc, time_utc = convert_utc_plus1_to_utc(row["Date"], row["time"])
    rounded_time_utc = round_time_to_nearest_hour(time_utc)
    weather_data = get_weather(row["latitude"], row["longitude"], date_utc, rounded_time_utc, variables)
    return weather_data


def add_weather_data(matches: pd.DataFrame):
    matches = add_lat_long(matches)

    weather_columns = ["temperature_2m", "relative_humidity_2m", "windspeed_10m", "apparent_temperature"]
    weather_results = matches.apply(fetch_weather_data, axis=1)

    weather_df = pd.DataFrame(weather_results.tolist(), columns=weather_columns, index=matches.index)

    matches = pd.concat([matches, weather_df], axis=1)
    return matches