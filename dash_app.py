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
                ]),
                dbc.Tab(label='Radar', tab_id='tab-6', children=[
                    dbc.Row([
                        dbc.Col(html.Div(html.Img(src="https://radar.weather.gov/ridge/standard/KICT_loop.gif"))),
                        dbc.Col(html.Div(html.Img(src="http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmasirks_.gif")))
                    ])
                ]),
                dbc.Tab(label='Watches/Warnings', tab_id='tab-7', children=[
                    dbc.Row([
                        dbc.Col(html.Div(html.Img(src="http://www.spc.noaa.gov/products/watch/validww.png")))
                    ])
                ]),
                dbc.Tab(label='Forecast', tab_id='tab-8', children=[
                    dbc.Row([
                        html.Div(html.Img(src="https://media.psg.nexstardigital.net/ksnw/weather/images/wx_weekly_full.jpg"))
                    ])
                ]),
                dbc.Tab(label='Outlook', tab_id='tab-9', children=[
                    dbc.Row([
                        html.Div(html.Img(src="https://www.spc.noaa.gov/products/outlook/day1otlk_1300.gif")),
                        html.Div(html.Img(src="https://www.spc.noaa.gov/products/outlook/day2otlk_0600.gif")),
                        html.Div(html.Img(src="https://www.spc.noaa.gov/products/outlook/day3otlk_0730.gif"))
                    ])
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