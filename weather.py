import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc


from apscheduler.schedulers.background import BackgroundScheduler

import pandas as pd

from scrape_wunderground import WeatherStation
from plotly_graphs import create_temperature_dewpoint_graph, create_humidity_graph, create_wind_graph, create_rain_graph, create_pressure_graph


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME])

ws = WeatherStation()

df = pd.DataFrame()

def update_data():
    global df
    df = ws.scrape_wunderground()

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=5)
scheduler.start()

update_data()

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '10px'},
    children=[
        html.H1("weather.kellykemnitz.com", style={'textAlign': 'center', 'color': '#007ACC'}),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000,  # in milliseconds
            n_intervals=0
        ),
        dcc.Graph(
            id='temperature-dewpoint-graph',
            figure=create_temperature_dewpoint_graph(df)
        ),
        dcc.Graph(
            id='humidity-graph',
            figure=create_humidity_graph(df)
        ),
        dcc.Graph(
            id='wind-graph',
            figure=create_wind_graph(df)
        ),
        dcc.Graph(
            id='rain-graph',
            figure=create_rain_graph(df)
        ),
        dcc.Graph(
            id='pressure-graph',
            figure=create_pressure_graph(df)
        )
])

@app.callback(
    [Output('temperature-dewpoint-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('wind-graph', 'figure'),
     Output('rain-graph', 'figure'),
     Output('pressure-graph', 'figure')],
    [Input('interval-component', 'n_intervals')])

def update_graphs(n):
    return (create_temperature_dewpoint_graph(df),
            create_humidity_graph(df),
            create_wind_graph(df),
            create_rain_graph(df),
            create_pressure_graph(df))


if __name__ == '__main__':
    app.run_server(debug=True)
