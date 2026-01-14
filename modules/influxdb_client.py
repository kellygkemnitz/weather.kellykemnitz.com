import logging

from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBWriter:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket

    def write_observations(self, observations):
        """Write current weather observations to InfluxDB"""
        
        # Use context manager to ensure proper cleanup
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
            try:
                points = []
                
                for obs in observations:
                    # Create point with proper field mapping based on normalized data
                    point = (
                        Point("current_observations")
                        .tag("stationID", str(obs.get("stationID", "unknown")))
                        .tag("country", str(obs.get("country", "unknown")))
                        .tag("city", str(obs.get("neighborhood", "unknown")))
                        .tag("longitude", float(obs.get("lon", "0.0")))
                        .tag("latitude", float(obs.get("lat", "0.0")))
                        .tag("elevation", int(obs.get("imperial", {}).get("elev", "0")))

                        .field("humidity", int(obs.get("humidity", 0)))
                        .field("solarRadiation", float(obs.get("solarRadiation", 0.0)))
                        .field("uv", float(obs.get("uv", 0.0)))
                        .field("windDirection", int(obs.get("winddir", 0)))

                        .field("dewpoint", int(obs.get("imperial", {}).get("dewpt", 0)))
                        .field("heatIndex", int(obs.get("imperial", {}).get("heatIndex", 0)))
                        .field("precipitationRate", float(obs.get("imperial", {}).get("precipRate", 0.0)))
                        .field("precipitationTotal", float(obs.get("imperial", {}).get("precipTotal", 0.0)))
                        .field("pressure", float(obs.get("imperial", {}).get("pressure", 0.0)))
                        .field("temperature", int(obs.get("imperial", {}).get("temp", 0)))
                        .field("windChill", int(obs.get("imperial", {}).get("windChill", 0)))
                        .field("windSpeed", int(obs.get("imperial", {}).get("windSpeed", 0)))

                        .time(obs.get("obsTimeUtc", datetime.now(timezone.utc)), WritePrecision.S)
                    )
                    points.append(point)
                
                # Write all points in batch
                write_api = client.write_api(write_options=SYNCHRONOUS)
                write_api.write(bucket=self.bucket, org=self.org, record=points)
                logging.info(f"Successfully wrote {len(points)} observations to InfluxDB")
            
            except Exception as e:
                logging.error(f"Error writing to InfluxDB: {e}")
                raise

    def query_observerations(self, start: str, stop: str):
        """Query weather observations from InfluxDB within a time range"""
        
        with InfluxDBClient(url=self.url, token=self.token, org=self.org) as client:
            query_api = client.query_api()
            query = f'''
            from(bucket: "{self.bucket}")
              |> range(start: {start}, stop: {stop})
              |> filter(fn: (r) => r._measurement == "weather_observations")
            '''
            try:
                result = query_api.query(org=self.org, query=query)
                records = []
                
                for table in result:
                    for record in table.records:
                        records.append(record.values)
                
                logging.info(f"Queried {len(records)} observations from InfluxDB")
                
                return records
            
            except Exception as e:
                logging.error(f"Error querying InfluxDB: {e}")
                raise
