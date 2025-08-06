#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to scrape 5-min personal weather station data from Weather Underground.

Usage is:
>>> python scrape_wunderground.py   STATION    DATE     FREQ

where station is a personal weather station (e.g., KCAJAMES3), date is in the
format YYYY-MM-DD and FREQ is either 'daily' or '5min' (for daily or 5-minute
observations, respectively).

Alternatively, each function below can be imported and used in a separate python
script. Note that a working version of chromedriver must be installed and the absolute
path to executable has to be updated below ("chromedriver_path").

Zach Perzan, 2021-07-28
Modified ever so slightly by Kelly Kemnitz, 9/12/2024"""

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import numpy as np
import os
import pandas as pd
import requests
import time


class Wunderground:
    def __init__(self, station, attempts, wait_time, freq):
        self.station = station
        self.attempts = attempts
        self.wait_time = wait_time
        self.freq = freq
        
        self.date = datetime.today().strftime("%Y-%m-%d")

        if self.freq == '5min':
            self.timespan = 'daily'
        if self.freq == 'daily':
            self.timespan = 'monthly'

        self.url = (
            f"https://www.wunderground.com/dashboard/pws/{self.station}/"
            f"table/{self.date}/{self.date}/"
            f"{self.timespan}"
        )

        self.columns_map = {
            '5min': [
                'Temperature',
                'Dew Point',
                'Humidity',
                'Wind Speed',
                'Wind Gust',
                'Pressure',
                'Precip. Rate',
                'Precip. Accum.'
            ],
            'daily': [
                'Temperature_High',
                'Temperature_Avg',
                'Temperature_Low',
                'DewPoint_High',
                'DewPoint_Avg',
                'DewPoint_Low',
                'Humidity_High',
                'Humidity_Avg',
                'Humidity_Low',
                'WindSpeed_High',
                'WindSpeed_Avg',
                'WindSpeed_Low',
                'Pressure_High',
                'Pressure_Low',
                'Precip_Sum'
            ]
        }

    def to_dict(self):
        return self.__dict__.copy()

    def to_html(self, df):
        """Convert dataframe to HTML file

        Parameters
        ----------
            df : dataframe
                The dataframe to convert to HTML

        Returns
        -------
            str
                The path to the saved HTML file
        """
        file_path = f'{self.station}_{self.date}.html'
        df.to_html(file_path)
        
        return file_path

    def to_csv(self, df):
        """Convert dataframe to CSV file

        Parameters
        ----------
            df : dataframe
                The dataframe to convert to CSV

        Returns
        -------
            str
                The path to the saved CSV file
        """
        file_path = f'{self.station}_{self.date}.csv'
        df.to_csv(file_path)
        
        return file_path
    
    def scrape(self):
        for attempt in range(1, self.attempts + 1):
            try:
                response = requests.get(self.url, timeout=30)
                response.raise_for_status()  # Raise an error for bad responses

                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find('lib-history-table')
                if not table:
                    raise ValueError(f'lib-history-table not found')
                
                tbody_tags = table.find_all('tbody')
                if len(tbody_tags) < 2:
                    raise ValueError(f'Expected 2 tbody tags. Found {len(tbody_tags)}.')

                time_body, data_body = tbody_tags
                hours = [tr.get_text(strip=True)
                         for tr in time_body.find_all('tr')]

                classes = ['wu-value wu-value-to', 'wu-unit-no-value ng-star-inserted']
                raw_vals = [span.get_text(strip=True)
                            for span in data_body.find_all('span', class_=classes)]

                cleaned = [np.nan if v == '--' else float(v) for v in raw_vals]
                cols = self.columns_map[self.freq]
                arr = np.array(cleaned).reshape(-1, len(cols))

                if self.freq == '5min':
                    timestamps = [f'{self.date} {h}' for h in hours]
                    idx = pd.to_datetime(timestamps, format='%Y-%m-%d %I:%M %p')
                else:
                    idx = pd.to_datetime(hours)

                df = pd.DataFrame(arr, index=idx, columns=cols)
                df = df.reset_index().rename(columns={'index': 'Timestamp'})

                return df

            except Exception as e:
                if attempt == self.attempts:
                    print(f'All {self.attempts} attempts exhausted: {e}')
                    return pd.DataFrame()
                print(f'Attempt {attempt} failed: {e!s}. '
                      f'Retrying in {self.wait_time} seconds...')
                time.sleep(self.wait_time)

    def scrape_multidate(self, start_date, end_date):
        """Given a PWS station ID and a start and end date, scrape data from Weather
            Underground for that date range and return it as a dataframe.

            Parameters
            ----------
                start_date : str
                    The date for which to begin acquiring data, formatted as 'YYYY-MM-DD'
                end_date : str
                    The date for which to end acquiring data, formatted as 'YYYY-MM-DD'

            Returns
            -------
                df : dataframe or None
                    A dataframe of weather observations, with index as pd.DateTimeIndex
                    and columns as the observed data
        """
        
        # Convert end_date and start_date to datetime types
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        # Calculate time delta
        delta = end_date - start_date

        # Create list dates and append all days within the start and end date to dates
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

        # Repeat the station name in a list for as many dates are in the date range
        stations = [self.station] * len(dates)

        # Scrape wunderground for data from all dates in range and store in list of dateframes
        df_list = [self.scrape_multiattempt(station, date, freq=self.freq) for station, date in zip(stations, dates)]
        df_list = [df for df in df_list if df is not None and not df.empty]

        if not df_list:
            print(f'No data was retrieved for the given date range.')
            return pd.DataFrame()

        # Convert list of dataframes to one dataframe
        try:
            df = pd.concat(df_list, ignore_index=True)
        except ValueError as e:
            print(f'Error concatenating dataframes: {e}')
            return pd.DataFrame()

        return df