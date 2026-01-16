import logging
import requests

class WundergroundClient:
    def __init__(self, url, api_key: str, station_id: str):
        self.url = url
        self.api_key = api_key
        self.station_id = station_id

    def fetch_data(self):
        params = {
            'stationId': self.station_id,
            'format': 'json',
            'units': 'e',
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()

            data = response.json()
            current_observations = data.get('observations', [])

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from Wunderground API: {e}")
            raise
        
        return current_observations
