from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import streamlit as st

from modules.scrape_wunderground import WeatherStation
from modules.plotly_graphs import create_temperature_dewpoint_graph, create_humidity_graph, create_wind_graph, create_rain_graph, create_pressure_graph

ws = WeatherStation()
df = pd.DataFrame()

def update_data():
    global df
    df = ws.scrape_wunderground()

def update_graphs(n):
    return (create_temperature_dewpoint_graph(df),
            create_humidity_graph(df),
            create_wind_graph(df),
            create_rain_graph(df),
            create_pressure_graph(df))

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=5)
scheduler.start()

update_data()

st.title('weather.kellykemnitz.com')
tabs = st.tabs(['Temperature/Dewpoint','Humidity','Wind','Rain','Pressure'])

with tabs[0]:
    st.header('Temperature/Dewpoint')
    st.plotly_chart(create_temperature_dewpoint_graph(df))

with tabs[1]:
    st.header('Dewpoint')
    st.plotly_chart(create_humidity_graph(df))

with tabs[2]:
    st.header('Wind')
    st.plotly_chart(create_wind_graph(df))

with tabs[3]:
    st.header('Rain')
    st.plotly_chart(create_rain_graph(df))

with tabs[4]:
    st.header('Pressure')
    st.plotly_chart(create_pressure_graph(df))