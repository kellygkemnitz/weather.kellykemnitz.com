import requests

class APIClient:
    def __init__(self, api_key: str, station_id: str):
        self.api_key = api_key
        self.station_id = station_id
        self.base_url = "https://api.weather.com/v2/pws/observations/current"

    def fetch_data(self):
        params = {
            'stationId': self.station_id,
            'format': 'json',
            'units': 'e',
            'apiKey': self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        
        data = response.json()
        
        # Process the JSON data into a DataFrame
        current_observations = data.get('observations', [])

        return current_observations