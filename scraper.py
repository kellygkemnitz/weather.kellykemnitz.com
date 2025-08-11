import os

from dotenv import load_dotenv

from modules.wunderground import Wunderground
from modules.plotly_graphs import Graphs

if __name__ == "__main__":
    load_dotenv()

    station = os.getenv('STATION')
    attempts = int(os.getenv('ATTEMPTS'))
    wait_time = os.getenv('WAIT_TIME')
    freq = os.getenv('FREQ')

    wunderground = Wunderground(station, attempts, wait_time, freq)
    df = wunderground.scrape()  # This should return a DataFrame

    graphs = Graphs()
    all_graphs = graphs.create_graphs(df)

    temperature_dewpoint_graph = all_graphs['temperature_dewpoint']
    humidity_graph = all_graphs['humidity']
    wind_graph = all_graphs['wind']
    rain_graph = all_graphs['rain']
    pressure_graph = all_graphs['pressure']

    # Save the graph as HTML or display it (not implemented here)
    # temperature_dewpoint_graph.write_html("temperature_dewpoint_graph.html")