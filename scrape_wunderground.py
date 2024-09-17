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

from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
from plotly.subplots import make_subplots
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import yaml


class WeatherStation:
    def __init__(self):
        with open('settings.yaml', 'r') as file:
            settings = yaml.safe_load(file)

        self.station = settings['station']
        self.date = datetime.today().strftime("%Y-%m-%d")
        self.freq = settings['freq']
        self.chromedriver_path = settings['chromedriver_path']
        self.attempts = settings['attempts']
        self.wait_time = settings['wait_time']

    def get_settings(self):
        return self.station, self.date, self.freq, self.chromedriver_path, self.attempts, self.wait_time

    def render_page(self, url):
        """Given a url, render it with chromedriver and return the html source

        Parameters
        ----------
            url : str
                url to render

        Returns
        -------
            r :
                rendered page source
        """

        chrome_service = Service(self.chromedriver_path)
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
        driver.get(url)
        time.sleep(3) # Could potentially decrease the sleep time
        rendered_page = driver.page_source
        driver.quit()

        return rendered_page

    def scrape_wunderground(self):
        """Given a PWS station ID and date, scrape that day's data from Weather
        Underground and return it as a dataframe.

        Returns
        -------
            df : dataframe or None
                A dataframe of weather observations, with index as pd.DateTimeIndex
                and columns as the observed data
        """

        # the url for 5-min data is called "daily" on weather underground
        if self.freq == '5min':
            timespan = 'daily'
        # the url for daily summary data (avg/min/max) is called "monthly" on wunderground
        elif self.freq == 'daily':
            timespan = 'monthly'

        # Render the url and open the page source as BS object
        url = 'https://www.wunderground.com/dashboard/pws/%s/table/%s/%s/%s' % (self.station,
                                                                                self.date, self.date,
                                                                                timespan)
        r = self.render_page(url)
        soup = BS(r, "html.parser")

        container = soup.find('lib-history-table')

        # Check that lib-history-table is found
        if container is None:
            raise ValueError("could not find lib-history-table in html source for %s" % url)

        # Get the timestamps and data from two separate 'tbody' tags
        all_checks = container.find_all('tbody')
        time_check = all_checks[0]
        data_check = all_checks[1]

        # Iterate through 'tr' tags and get the timestamps
        hours = []
        for i in time_check.find_all('tr'):
            trial = i.get_text()
            hours.append(trial)

        # For data, locate both value and no-value ("--") classes
        classes = ['wu-value wu-value-to', 'wu-unit-no-value ng-star-inserted']

        # Iterate through span tags and get data
        data = []
        for i in data_check.find_all('span', class_=classes):
            trial = i.get_text()
            data.append(trial)

        columns = {'5min': ['Temperature', 'Dew Point', 'Humidity', 'Wind Speed',
                            'Wind Gust', 'Pressure', 'Precip. Rate', 'Precip. Accum.'],
                'daily': ['Temperature_High', 'Temperature_Avg', 'Temperature_Low',
                            'DewPoint_High', 'DewPoint_Avg', 'DewPoint_Low',
                            'Humidity_High', 'Humidity_Avg', 'Humidity_Low',
                            'WindSpeed_High', 'WindSpeed_Avg', 'WindSpeed_Low',
                            'Pressure_High', 'Pressure_Low', 'Precip_Sum']}

        # Convert NaN values (stings of '--') to np.nan
        data_nan = [np.nan if x == '--' else x for x in data]

        # Convert list of data to an array
        data_array = np.array(data_nan, dtype=float)
        data_array = data_array.reshape(-1, len(columns[self.freq]))

        # Prepend date to HH:MM strings
        if self.freq == '5min':
            timestamps = ['%s %s' % (self.date, t) for t in hours]
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
    
    def create_graphs(self, df):
        if df is None:
            return None
        
        temperature = go.Scatter(
            x = df['Timestamp'],
            y = df['Temperature'],
            name = 'Temperature'
        )

        dewpoint = go.Scatter(
            x = df['Timestamp'],
            y = df['Dew Point'],
            name = 'Dewpoint'
        )

        humidity = go.Scatter(
            x = df['Timestamp'],
            y = df['Humidity'],
            name = 'Humidity'
        )

        windspeed = go.Scatter(
            x = df['Timestamp'],
            y = df['Wind Speed'],
            name = 'Wind Speed'
        )

        windgust = go.Scatter(
            x = df['Timestamp'],
            y = df['Wind Gust'],
            name = 'Wind Gust'
        )

        pressure = go.Scatter(
            x = df['Timestamp'],
            y = df['Pressure'],
            name = 'Pressure'
        )

        precip_rate = go.Scatter(
            x = df['Timestamp'],
            y = df['Precip. Rate'],
            name = 'Precipitation Rate'
        )

        precip_accum = go.Scatter(
            x = df['Timestamp'],
            y = df['Precip. Accum.'],
            name = 'Precipitation Accumulation'
        )

        temp_dew_graph = make_subplots(specs=[[{"secondary_y": True}]])
        temp_dew_graph.add_trace(temperature, secondary_y=False)
        temp_dew_graph.add_trace(dewpoint, secondary_y=True)
        
        humidity_graph, windspeed_graph, windgust_graph, pressure_graph, precip_rate_graph, precip_accum_graph = go.Figure()
        
        humidity_graph.add_trace(humidity)
        windspeed_graph.add_trace(windspeed)
        windgust_graph.add_trace(windgust)
        pressure_graph.add_trace(pressure)
        precip_rate_graph.add_trace(precip_rate)
        precip_accum_graph.add_trace(precip_accum)

        graphs = {
            "temp_dew_graph": json.dumps(temp_dew_graph, cls=plotly.utils.PlotlyJSONEncoder),
            "humidity_graph": json.dumps(humidity_graph, cls=plotly.utils.PlotlyJSONEncoder),
            "windspeed_graph": json.dumps(windspeed_graph, cls=plotly.utils.PlotlyJSONEncoder),
            "windgust_graph": json.dumps(windgust_graph, cls=plotly.utils.PlotlyJSONEncoder),
            "pressure_graph": json.dumps(pressure_graph, cls=plotly.utils.PlotlyJSONEncoder),
            "precip_rate_graph": json.dumps(precip_rate_graph, cls=plotly.utils.PlotlyJSONEncoder),
            "precip_accum_graph": json.dumps(precip_accum_graph, cls=plotly.utils.PlotlyJSONEncoder),
        }
        
        return graphs

# @app.route('/graph')
# def graph():
#     # temp_dew_json, windspeed_json = create_graphs(df)
#     temp_dew_json = create_graphs(df)
#     # return jsonify(temp_dew=temp_dew_json, windspeed=windspeed_json)
#     return jsonify(temp_dew=temp_dew_json)
#     # return temp_dew_json

# @app.route('/')
# def index():
#     temp_dew_json = create_graphs(df)
#     return render_template('index.html', graphJSON=temp_dew_json)

# if __name__ == "__main__":
#     ws = WeatherStation()
#     try:
#         df = ws.scrape_wunderground()
#         if df is not None:
#             # html_file = ws.to_html(df)
#             # csv_file = ws.to_csv(df)
#             # graph_json = ws.create_graphs(df)
#             pass
#             # app.run()
#         else:
#             print(f'No data available for station {ws.station} on {ws.date}')

#     except Exception as e:
#         print(f'Unable to return data for station {ws.station}: {e}')