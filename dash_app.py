import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
from scrape_wunderground import WeatherStation
from plotly_graphs import create_temperature_dewpoint_graph, create_humidity_graph, create_wind_graph, create_rain_graph, create_pressure_graph

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME
    ],
    assets_folder='assets/css'
)

def fetch_data():
    ws = WeatherStation()
    return ws.scrape_wunderground()

df = fetch_data()

app.layout = dbc.Container([
    html.Div([
        html.Div([
            dcc.Interval(
                id='interval-component',
                interval=30*60*1000,  # in milliseconds
                n_intervals=0),

            dbc.Tabs(id='tabs', children=[
                dbc.Tab(label='Temperature & Dewpoint', tab_id='tab-1', children=[
                    dcc.Graph(id='temperature-dewpoint-graph', figure=create_temperature_dewpoint_graph(df), config={'displayModeBar': True})
                ]),
                dbc.Tab(label='Humidity', tab_id='tab-2', children=[
                    dcc.Graph(id='humidity-graph', figure=create_humidity_graph(df), config={'displayModeBar': True})
                ]),
                dbc.Tab(label='Wind', tab_id='tab-3', children=[
                    dcc.Graph(id='wind-graph', figure=create_wind_graph(df), config={'displayModeBar': True})
                ]),
                dbc.Tab(label='Rain', tab_id='tab-4', children=[
                    dcc.Graph(id='rain-graph', figure=create_rain_graph(df), config={'displayModeBar': True})
                ]),
                dbc.Tab(label='Pressure', tab_id='tab-5', children=[
                    dcc.Graph(id='pressure-graph', figure=create_pressure_graph(df), config={'displayModeBar': True})
                ]),
                dbc.Tab(label='Radar', tab_id='tab-6', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.A([
                                html.Img(src="https://radar.weather.gov/ridge/standard/KICT_loop.gif", className="image")
                                ], href="https://radar.weather.gov/ridge/standard/KICT_loop.gif", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.A([
                                html.Img(src="https://s.w-x.co/staticmaps/wu/wxtype/county_loc/sln/animate.png", className="image")
                                ], href="https://s.w-x.co/staticmaps/wu/wxtype/county_loc/sln/animate.png", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.A([
                                html.Img(src="http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmasirks_.gif", className="image")
                                ], href="http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmasirks_.gif", target="_blank")
                        ]), className="col")
                    ], className="row")
                ]),
                dbc.Tab(label='Watches/Warnings', tab_id='tab-7', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.A([
                                html.Img(src="http://www.spc.noaa.gov/products/watch/validww.png", className="image")
                            ], href="http://www.spc.noaa.gov/products/watch/validww.png", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.A([
                                html.Img(src="https://www.weather.gov/wwamap/png/ict.png", className="image")
                            ], href="https://www.weather.gov/wwamap/png/ict.png", target="_blank")
                        ]), className="col")
                    ], className="row")
                ]),
                dbc.Tab(label='Forecast', tab_id='tab-8', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("NOAA - Today's Forecast"),
                            html.A([
                                html.Img(src="https://www.wpc.ncep.noaa.gov/noaa/noaad1.gif", className="image")
                            ], href="https://www.wpc.ncep.noaa.gov/noaa/noaad1.gif", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.H5("NOAA - Tomorrow's Forecast"),
                            html.A([
                                html.Img(src="https://www.wpc.ncep.noaa.gov/noaa/noaad2.gif", className="image")
                            ], href="https://www.wpc.ncep.noaa.gov/noaa/noaad2.gif", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.H5("NOAA - Day 3 Forecast"),
                            html.A([
                                html.Img(src="https://www.wpc.ncep.noaa.gov/noaa/noaad3.gif", className="image")
                            ], href="https://www.wpc.ncep.noaa.gov/noaa/noaad3.gif", target="_blank")
                       ]), className="col"),
                    ], className="row"),
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("KSN Forecast"),
                            html.A([
                                html.Img(src="https://media.psg.nexstardigital.net/ksnw/weather/images/wx_weekly_full.jpg", className="image")
                            ], href="https://media.psg.nexstardigital.net/ksnw/weather/images/wx_weekly_full.jpg", target="_blank")
                        ]), className="col")
                    ], className="row")
                ]),
                dbc.Tab(label='Outlook', tab_id='tab-9', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("SPC Day 1 Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/outlook/day1otlk_1300.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/outlook/day1otlk_1300.gif", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.H5("SPC Day 2 Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/outlook/day2otlk_0600.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/outlook/day2otlk_0600.gif", target="_blank")
                        ]), className="col"),
                        dbc.Col(html.Div([
                            html.H5("SPC Day 3 Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/outlook/day3otlk_0730.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/outlook/day3otlk_0730.gif", target="_blank")
                        ]), className="col")
                    ], className="row"),
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("ICT Hazardous Weather Outlook"),
                            html.A([
                                html.Img(src="https://www.weather.gov/images/ict/ghwo/SevereThunderstormsDay1.jpg", className="image")
                            ], href="https://www.weather.gov/images/ict/ghwo/SevereThunderstormsDay1.jpg", target="_blank")
                        ]), className="col")
                    ], className="row")
                ])
            ])
        ], className="container")
    ])
])

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