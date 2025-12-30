import logging
import os
import sys

from dotenv import load_dotenv
from modules.wunderground_client import WundergroundClient
from modules.influxdb_client import InfluxDBWriter


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()

    wunderground_api_key = os.getenv('WUNDERGROUND_API_KEY')
    wunderground_station_id = os.getenv('WUNDERGROUND_STATION_ID')
    influxdb_url = os.getenv('INFLUXDB_URL')
    influxdb_token = os.getenv('INFLUXDB_TOKEN')

    try:
        # Fetch weather data
        client = WundergroundClient(wunderground_api_key, wunderground_station_id)
        observations = client.fetch_data()

        # Write to InfluxDB
        influxdb_client = InfluxDBWriter(
            url=influxdb_url,
            token=influxdb_token,
            org=os.getenv('INFLUXDB_ORG'),
            bucket=os.getenv('INFLUXDB_BUCKET')
        )

        influxdb_client.write_observations(observations)
        
    except Exception as e:
        logging.error(f"Error in weather data pipeline: {e}")
        sys.exit(1)
    
    sys.exit(0)