import logging
import os

from datetime import datetime, timedelta

from flask import Flask, send_from_directory, render_template
from flask_caching import Cache

from dotenv import load_dotenv
from modules.wunderground import Wunderground
from modules.plotly_graphs import Graphs

load_dotenv()

station = os.getenv('STATION')
attempts = int(os.getenv('ATTEMPTS'))
wait_time = os.getenv('WAIT_TIME')
freq = os.getenv('FREQ')

app = Flask(__name__, static_folder='static')
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@cache.memoize()
def fetch_data():
    try:
        wunderground = Wunderground(
            station=station,
            attempts=attempts,
            wait_time=wait_time,
            freq=freq
        )
        
        df = wunderground.scrape()
        
        if df is None or df.empty:
            raise ValueError("Empty DataFrame returned from scrape.")

        logging.info("Fetched %d rows of data", len(df))
        return df

    except Exception as e:
        logging.error(f"Failed to fetch data: {e}")
        return None
    
@app.route('/')
def index():
    df = fetch_data()
    
    if df.empty:
        return render_template('index.html', graphs)

    graphs = Graphs()
    figs = graphs.create_graphs(df)

    graphs = {
        name: fig.to_html(full_html=False, include_plotlyjs=False)
        for name, fig in figs.items()
    }

    return render_template(
        'index.html',
        temperature_dewpoint = graphs['temperature_dewpoint'],
        humidity = graphs['humidity'],
        wind = graphs['wind'],
        rain = graphs['rain'],
        pressure = graphs['pressure'],
    )
