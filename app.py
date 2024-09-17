from flask import Flask, render_template, jsonify, request
import pandas as pd
from scrape_wunderground import WeatherStation


app = Flask(__name__)

ws = WeatherStation()

@app.route('/', methods=['GET'])
def home():
    try:
        df = ws.scrape_wunderground()
        if not df.empty:
            json_graphs = ws.create_graphs(df)
            return render_template('index.html', json_graphs=json_graphs)
        else:
            return jsonify({"error": "No data available."})
    except Exception as e:
        return jsonify({"error": str(e)})

# @app.route('/scrape', methods=['GET'])
# def scrape_data():
#     try:
#         df = ws.scrape_wunderground()
#         if not df.empty:
#             graph_json = ws.create_graphs(df)
#             return render_template('graph.html', graph_json=graph_json)
#         else:
#             return jsonify({"error": "No data available."})
#     except Exception as e:
#         return jsonify({"error": str(e)})
    
if __name__ == "__main__":
    app.run(debug=True)