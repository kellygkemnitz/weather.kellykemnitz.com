import logging

from datetime import datetime, timezone
from influxdb_client import InfluxDBClient as InfluxClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBWriter:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.org = org
        self.bucket = bucket
        self.client = InfluxClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_observations(self, observations):
        """Write weather observations to InfluxDB"""

        try:
            points = []
            for obs in observations:
                # Create point with proper field mapping based on normalized data
                point = (
                    Point("weather_observations")
                    .tag("stationID", str(obs.get("stationID", "unknown")))
                    .tag("country", str(obs.get("country", "unknown")))
                    .tag("state", str(obs.get("state", "unknown")))
                    .tag("city", str(obs.get("neighborhood", "unknown")))
                    .tag("longitude", float(obs.get("lon", "0.0")))
                    .tag("latitude", float(obs.get("lat", "0.0")))
                    .tag("elevation", int(obs.get("imperial", {}).get("elev", "0")))

                    .field("humidity", int(obs.get("humidity", 0)))
                    .field("solarRadiation", float(obs.get("solarRadiation", 0.0)))
                    .field("uv", float(obs.get("uv", 0.0)))
                    .field("windDirection", int(obs.get("winddir", 0)))

                    .field("dewpt", int(obs.get("imperial", {}).get("dewpt", 0)))
                    .field("heatIndex", int(obs.get("imperial", {}).get("heatIndex", 0)))
                    .field("precipitationRate", float(obs.get("imperial", {}).get("precipRate", 0.0)))
                    .field("precipitationTotal", float(obs.get("imperial", {}).get("precipTotal", 0.0)))
                    .field("pressure", float(obs.get("imperial", {}).get("pressure", 0.0)))
                    .field("temp", int(obs.get("imperial", {}).get("temp", 0)))
                    .field("windChill", int(obs.get("imperial", {}).get("windChill", 0)))
                    .field("windSpeed", int(obs.get("imperial", {}).get("windSpeed", 0)))

                    .time(obs.get("obsTimeUtc", datetime.now(timezone.utc)), WritePrecision.S)
                )
                points.append(point)
            
            # Write all points in batch
            self.write_api.write(bucket=self.bucket, org=self.org, record=points)
            logging.info(f"Successfully wrote {len(points)} observations to InfluxDB")
            
        except Exception as e:
            
            logging.error(f"Error writing to InfluxDB: {e}")
            raise