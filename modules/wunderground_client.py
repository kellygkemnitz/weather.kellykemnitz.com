import logging
import requests

class WundergroundClient:
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

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()
            current_observations = data.get('observations', [])

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from Wunderground API: {e}")
            raise
        
        return current_observations