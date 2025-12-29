import os

from dotenv import load_dotenv

from modules.api_client import APIClient

if __name__ == "__main__":
    load_dotenv()

    api_key = os.getenv('API_KEY')
    station_id = os.getenv('STATION_ID')
    influxdb_url = os.getenv('INFLUXDB_URL')
    influxdb_token = os.getenv('INFLUXDB_TOKEN')

    client = APIClient(api_key, station_id)
    df = client.fetch_data()

    exit(0)