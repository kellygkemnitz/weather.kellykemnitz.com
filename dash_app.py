import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from scrape_wunderground import WeatherStation
from plotly_graphs import create_temperature_dewpoint_graph, create_humidity_graph, create_wind_graph, create_rain_graph, create_pressure_graph

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME])

def fetch_data():
    ws = WeatherStation()
    return ws.scrape_wunderground()

df = fetch_data()

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'padding': '10px'},
    children=[
        dcc.Interval(
            id='interval-component',
            interval=30*60*1000,  # in milliseconds
            n_intervals=0),

        html.H1("weather.kellykemnitz.com", style={'textAlign': 'center'}),
        
        dbc.Tabs(
            id='tabs',
            children=[
                dbc.Tab(label='Temperature & Dewpoint', tab_id='tab-1', children=[
                    dcc.Graph(
                        id='temperature-dewpoint-graph',
                        figure=create_temperature_dewpoint_graph(df),
                        config={'displayModeBar': False},
                    )
                ]),
                dbc.Tab(label='Humidity', tab_id='tab-2', children=[
                    dcc.Graph(
                        id='humidity-graph',
                        figure=create_humidity_graph(df),
                        config={'displayModeBar': False},
                    )
                ]),
                dbc.Tab(label='Wind', tab_id='tab-3', children=[
                    dcc.Graph(
                        id='wind-graph',
                        figure=create_wind_graph(df),
                        config={'displayModeBar': False},
                    )
                ]),
                dbc.Tab(label='Rain', tab_id='tab-4', children=[
                    dcc.Graph(
                        id='rain-graph',
                        figure=create_rain_graph(df),
                        config={'displayModeBar': False},
                    )
                ]),
                dbc.Tab(label='Pressure', tab_id='tab-5', children=[
                    dcc.Graph(
                        id='pressure-graph',
                        figure=create_pressure_graph(df),
                        config={'displayModeBar': False},
                    )
                ])
            ]
        )
    ]
)

@app.callback(
    [Output('temperature-dewpoint-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('wind-graph', 'figure'),
     Output('rain-graph', 'figure'),
     Output('pressure-graph', 'figure')],
    [Input('interval-component', 'n_intervals')])

def update_graphs(n):
    df = fetch_data()
    return (create_temperature_dewpoint_graph(df),
            create_humidity_graph(df),
            create_wind_graph(df),
            create_rain_graph(df),
            create_pressure_graph(df))


if __name__ == '__main__':
    app.run(debug=True)

server = app.server