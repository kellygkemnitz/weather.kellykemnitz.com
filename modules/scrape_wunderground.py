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

from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from dotenv import load_dotenv

import numpy as np
import os
import pandas as pd
import requests
import time


class WeatherStation:
    def __init__(self):
        load_dotenv()

        self.station = os.getenv('STATION')
        self.date = datetime.today().strftime("%Y-%m-%d")
        self.freq = os.getenv('FREQ')
        self.attempts = os.getenv('ATTEMPTS')
        self.wait_time = os.getenv('WAIT_TIME')

        if self.freq == '5min':
            self.timespan = 'daily'
        if self.freq == 'daily':
            self.timespan = 'monthly'

        self.url = f'https://www.wunderground.com/dashboard/pws/{self.station}/table/{self.date}/{self.date}/{self.timespan}'

    def get_settings(self):
        settings = {
            'station': self.station,
            'url': self.url,
            'date': self.date,
            'freq': self.freq,
            'timespan': self.timespan,
            'attempts': self.attempts,
            'wait_time': self.wait_time
        }

        return settings

    def scrape_wunderground(self):
        """Given a PWS station ID and date, scrape that day's data from Weather
        Underground and return it as a dataframe.

        Returns
        -------
            df : dataframe or None
                A dataframe of weather observations, with index as pd.DateTimeIndex
                and columns as the observed data
        """

        response = requests.get(self.url)
        soup = bs(response.content, "html.parser")
        container = soup.find('lib-history-table')

        # Check that lib-history-table is found
        if container is None:
            raise ValueError(f'could not find lib-history-table in html source for {self.url}')

        # Get the timestamps and data from two separate 'tbody' tags
        all_checks = container.find_all('tbody')
        time_check = all_checks[0]
        data_check = all_checks[1]

        # Iterate through 'tr' tags and get the timestamps
        hours = list(map(lambda i: i.get_text(), time_check.find_all('tr')))

        # For data, locate both value and no-value ("--") classes
        classes = ['wu-value wu-value-to', 'wu-unit-no-value ng-star-inserted']

        # Iterate through span tags and get data
        data = list(map(lambda i: i.get_text(), data_check.find_all('span', class_=classes)))

        columns = {
            '5min': [
                'Temperature', 'Dew Point', 'Humidity', 'Wind Speed',
                'Wind Gust', 'Pressure', 'Precip. Rate', 'Precip. Accum.'
            ],
            'daily': [
                'Temperature_High', 'Temperature_Avg', 'Temperature_Low',
                'DewPoint_High', 'DewPoint_Avg', 'DewPoint_Low',
                'Humidity_High', 'Humidity_Avg', 'Humidity_Low',
                'WindSpeed_High', 'WindSpeed_Avg', 'WindSpeed_Low',
                'Pressure_High', 'Pressure_Low', 'Precip_Sum'
            ]
        }

        # Convert NaN values (stings of '--') to np.nan
        data_nan = list(map(lambda x: np.nan if x == '--' else x, data))

        # Convert list of data to an array
        data_array = np.array(data_nan, dtype=float)
        data_array = data_array.reshape(-1, len(columns[self.freq]))

        # Prepend date to HH:MM strings
        if self.freq == '5min':
            timestamps = list(map(lambda t: f'{self.date} {t}', hours))
        else:
            timestamps = hours

        # Convert to dataframe
        df = pd.DataFrame(index=timestamps, data=data_array, columns=columns[self.freq])
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d %I:%M %p')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Timestamp'}, inplace=True)

        return df

    def scrape_multiattempt(self):
        """Try to scrape data from Weather Underground. If there is an error on the
        first attempt, try again.

        Returns
        -------
            df : dataframe or None
                A dataframe of weather observations, with index as pd.DateTimeIndex
                and columns as the observed data
        """

        # Try to download data limited number of attempts
        for n in range(self.attempts):
            try:
                df = self.scrape_wunderground()
            except:
                # if unsuccessful, pause and retry
                time.sleep(self.wait_time)
            else:
                # if successful, then break
                break
        # If all attempts failed, return empty df
        else:
            df = pd.DataFrame()

        return df

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
        dates = []
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            dates.append(day)
        dates = [date.strftime('%Y-%m-%d') for date in dates]

        # Repeat the station name in a list for as many dates are in the date range
        stations = [self.station] * len(dates)

        # Scrape wunderground for data from all dates in range and store in list of dateframes
        df_list = list(map(self.scrape_multiattempt, stations, dates, freq=self.freq))

        # Convert list of dataframes to one dataframe
        df = pd.concat(df_list)

        return df
    
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
