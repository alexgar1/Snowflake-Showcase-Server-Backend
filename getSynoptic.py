import requests
import json


# Replace these variables with your own values
API_TOKEN = '3d5845d69f0e47aca3f810de0bb6fd3f'
STATION_ID = 'ATH20'  # Example: Salt Lake City Airport
START_TIME = '202301010000'  # January 1, 2023, 00:00 UTC
END_TIME = '202301012359'  # January 1, 2023, 23:59 UTC

def get_station_timeseries(token, station_id, start, end, variables, units='metric'):
    """
    Fetches time series data for a given station.

    Parameters:
    - token: API token for authentication.
    - station_id: Station identifier.
    - start: Start time in format YYYYmmddHHMM.
    - end: End time in format YYYYmmddHHMM.
    - variables: Comma-separated list of variables to fetch. Defaults to 'air_temp'.
    - units: Unit system for the returned data ('metric', 'english', or custom). Defaults to 'metric'.

    Returns:
    - JSON response containing the requested time series data.
    """
    base_url = "https://api.synopticdata.com/v2/stations/timeseries"
    params = {
        'token': token,
        'stid': station_id,
        'start': start,
        'end': end,
        'vars': variables,
        'units': units
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        #print(json.dumps(response.json(), indent=2))
        return formatJ(response.json())
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def formatJ(json_data):
    """
    Formats the JSON data into a dictionary with timestamps as keys.
    """

    data = {}
    try:
        observations = json_data['STATION'][0]['OBSERVATIONS']
        times = observations['date_time']
        for key in observations:
            if key != 'date_time':
                pointkey = key

        points = observations[key]

        for i, time in enumerate(times):
            data[time] = points[i]

    except (KeyError, IndexError):
        print("Error processing data")
    return data

        

# # Example usage
# if __name__ == "__main__":


#     temp = formatJ(get_station_timeseries(API_TOKEN, STATION_ID, START_TIME, END_TIME, 'air_temp'))
#     rh = formatJ(get_station_timeseries(API_TOKEN, STATION_ID, START_TIME, END_TIME, 'relative_humidity'))
#     snowdepth = get_station_timeseries(API_TOKEN, STATION_ID, START_TIME, END_TIME, 'snow_depth')
#     wind = formatJ(get_station_timeseries(API_TOKEN, STATION_ID, START_TIME, END_TIME, 'wind_speed')) 

#     if snowdepth:
#         print(snowdepth)
#         pass
#     else:
#         print("Failed to retrieve data.")
