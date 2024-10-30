import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from scrape_wunderground import WeatherStation
from plotly_graphs import create_temperature_dewpoint_graph, create_humidity_graph, create_wind_graph, create_rain_graph, create_pressure_graph


def fetch_data():
    ws = WeatherStation()
    return ws.scrape_wunderground()

df = fetch_data()

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    external_scripts=[
        "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js",
        "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js",
        "https://use.fontawesome.com/releases/v6.3.0/js/all.js"
    ])

app.index_string = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="weather.kellykemnitz.com">
    <meta name="author" content="Kelly Kemnitz">
    {%metas%} <title>{%title%}</title>
    {%favicon%}
    {%css%}
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
  </body>
</html>
"""

app.title = "weather.kellykemnitz.com"

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
                            html.H5("NWS"),
                            html.A([
                                html.Img(src="https://radar.weather.gov/ridge/standard/KICT_loop.gif", className="image")
                                ], href="https://radar.weather.gov/?settings=v1_eyJhZ2VuZGEiOnsiaWQiOiJsb2NhbCIsImNlbnRlciI6Wy05Ny40NDMsMzcuNjU0XSwibG9jYXRpb24iOm51bGwsInpvb20iOjguMTI2ODc1NzIxODAzODIsImZpbHRlciI6IldTUi04OEQiLCJsYXllciI6InNyX2JyZWYiLCJzdGF0aW9uIjoiS0lDVCJ9LCJhbmltYXRpbmciOmZhbHNlLCJiYXNlIjoic3RhbmRhcmQiLCJhcnRjYyI6ZmFsc2UsImNvdW50eSI6ZmFsc2UsImN3YSI6ZmFsc2UsInJmYyI6ZmFsc2UsInN0YXRlIjpmYWxzZSwibWVudSI6dHJ1ZSwic2hvcnRGdXNlZE9ubHkiOnRydWUsIm9wYWNpdHkiOnsiYWxlcnRzIjowLjgsImxvY2FsIjowLjYsImxvY2FsU3RhdGlvbnMiOjAuOCwibmF0aW9uYWwiOjAuNn19#/", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("Weather Underground"),
                            html.A([
                                html.Img(src="https://s.w-x.co/staticmaps/wu/wu/wxtype1200_cur/ussln/animate.png", className="image")
                                ], href="https://www.wunderground.com/radar/us/ks/salina", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("Accuweather"),
                            html.A([
                                html.Img(src="http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmasirks_.gif", className="image")
                                ], href="https://www.accuweather.com/en/us/kansas/weather-radar", target="_blank")
                        ], className="container"), className="col")
                    ], className="row")
                ]),
                dbc.Tab(label='Storm Reports & Watches/Warnings', tab_id='tab-7', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("SPC Mesoscale Discussions"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/md/validmd.png", className="image")
                            ], href="https://www.spc.noaa.gov/products/md/", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("SPC Watches"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/watch/validww.png", className="image")
                            ], href="https://www.spc.noaa.gov/products/watch/", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("NWS ICT Watches, Warnings, & Advisories"),
                            html.A([
                                html.Img(src="https://www.weather.gov/wwamap/png/ict.png", className="image")
                            ], href="https://www.weather.gov/ict/", target="_blank")
                        ], className="container"), className="col")
                    ], className="row"),
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("SPC Storm Reports"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/climo/reports/today.gif", className="image")
                            ], href="https://www.spc.noaa.gov/climo/online/", target="_blank")
                        ], className="container"), className="col")
                    ], className="row")
                ]),
                dbc.Tab(label='Forecast', tab_id='tab-8', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("NOAA - Today's Forecast"),
                            html.A([
                                html.Img(src="https://www.wpc.ncep.noaa.gov/noaa/noaad1.gif", className="image")
                            ], href="https://www.wpc.ncep.noaa.gov/national_forecast/natfcst.php", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("NOAA - Tomorrow's Forecast"),
                            html.A([
                                html.Img(src="https://www.wpc.ncep.noaa.gov/noaa/noaad2.gif", className="image")
                            ], href="https://www.wpc.ncep.noaa.gov/national_forecast/natfcst.php", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("NOAA - Day 3 Forecast"),
                            html.A([
                                html.Img(src="https://www.wpc.ncep.noaa.gov/noaa/noaad3.gif", className="image")
                            ], href="https://www.wpc.ncep.noaa.gov/national_forecast/natfcst.php", target="_blank")
                       ], className="container"), className="col"),
                    ], className="row"),
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("KSN Forecast"),
                            html.A([
                                html.Img(src="https://media.psg.nexstardigital.net/ksnw/weather/images/wx_weekly_full.jpg", className="image")
                            ], href="https://www.ksn.com/weather/", target="_blank")
                        ], className="container"), className="col")
                    ], className="row")
                ]),
                dbc.Tab(label='Outlooks', tab_id='tab-9', children=[
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("SPC Day 1 Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/outlook/day1otlk_1300.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/outlook/", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("SPC Day 2 Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/outlook/day2otlk_0600.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/outlook/", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("SPC Day 3 Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/outlook/day3otlk_0730.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/outlook/", target="_blank")
                        ], className="container"), className="col")
                    ], className="row"),
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H5("ICT Hazardous Weather Outlook"),
                            html.A([
                                html.Img(src="https://www.weather.gov/images/ict/ghwo/SevereThunderstormsDay1.jpg", className="image")
                            ], href="https://www.weather.gov/erh/ghwo?wfo=ict", target="_blank")
                        ], className="container"), className="col"),
                        dbc.Col(html.Div([
                            html.H5("SPC Fire Outlook"),
                            html.A([
                                html.Img(src="https://www.spc.noaa.gov/products/fire_wx/day1fireotlk-overview.gif", className="image")
                            ], href="https://www.spc.noaa.gov/products/fire_wx/overview.html", target="_blank")
                        ], className="container"), className="col")
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
