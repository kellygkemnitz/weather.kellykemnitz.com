import dash
from dash import dcc, html

from apscheduler.schedulers.background import BackgroundScheduler

from scrape_wunderground import WeatherStation
from plotly_graphs import create_temperature_dewpoint_graph, create_humidity_graph, create_wind_graph, create_rain_graph, create_pressure_graph


app = dash.Dash(__name__)

ws = WeatherStation()

def update_data():
    global df
    df = ws.scrape_wunderground()

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', hours=1)
scheduler.start()

update_data()

app.layout = html.Div(children=[
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

if __name__ == '__main__':
    app.run_server(debug=True)
