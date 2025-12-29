import pandas as pd

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBClient:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.url = url
        self.token = token
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_dataframe(self, df: pd.DataFrame):
        for index, row in df.iterrows():
            point = (
                Point("weather_data")
                .tag("station", row.get("station", "unknown"))
                .field("temperature", row.get("temperature", 0.0))
                .field("humidity", row.get("humidity", 0.0))
                .field("wind_speed", row.get("wind_speed", 0.0))
                .field("pressure", row.get("pressure", 0.0))
                .time(row['timestamp'], WritePrecision.NS)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)