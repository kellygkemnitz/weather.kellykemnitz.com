import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_caching import Cache

modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules'))
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from api_client import APIClient
from influxdb_client import InfluxDBClient, InfluxDBWriter

app = Flask(__name__, static_folder='static')
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

load_dotenv()

wunderground_config = {
    'api_key': os.getenv('WUNDERGROUND_API_KEY'),
    'station_id': os.getenv('WUNDERGROUND_STATION_ID')
}

influxdb_config = {
    'url': os.getenv('INFLUXDB_URL'),
    'token': os.getenv('INFLUXDB_TOKEN'),
    'org': os.getenv('INFLUXDB_ORG'),
    'bucket': os.getenv('INFLUXDB_BUCKET')
}


@app.route('/api/temperature')
@cache.cached()
def temperature_data():
    """API endpoint that returns temperature data as JSON"""
    query = f'''
    from(bucket: "{influxdb_config['bucket']}")
        |> range(start: -1d)
        |> filter(fn: (r) => r._measurement == "weather_observations")
        |> filter(fn: (r) => r._field == "temp" or r._field == "dewpoint")
        |> keep(columns: ["_time", "_value"])
        |> sort(columns: ["_time"])
    '''

    try:
        # Use context manager to ensure proper client cleanup
        with InfluxDBClient(
            url=influxdb_config['url'],
            token=influxdb_config['token'],
            org=influxdb_config['org']
        ) as client:
            query_api = client.query_api()
            result = query_api.query(org=influxdb_config['org'], query=query)
            
            timestamps = []
            values = []

            for table in result:
                for record in table.records:
                    timestamps.append(record.get_time().isoformat())
                    values.append(record.get_value())
            
            return jsonify({
                'timestamps': timestamps,
                'values': values
            })
    
    except Exception as e:
        app.logger.error(f"Error querying InfluxDB: {e}")
        return jsonify({
            'timestamps': [],
            'values': [],
            'error': 'Failed to fetch data'
        }), 500

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('new_index.html')
    

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\nShutting down Flask app gracefully...")
    sys.exit(0)


if __name__ == '__main__':
    try:
        # Fetch weather data
        client = APIClient(wunderground_config['api_key'], wunderground_config['station_id'])
        observations = client.fetch_data()

        # Write to InfluxDB
        influx_client = InfluxDBWriter(
            url=influxdb_config['url'],
            token=influxdb_config['token'],
            org=influxdb_config['org'],
            bucket=influxdb_config['bucket']
        )

        influx_client.write_observations(observations)
        
    except Exception as e:
        logging.error(f"Error in weather data pipeline: {e}")
        sys.exit(1)
    
    app.run(host='0.0.0.0', port=8001, debug=True)