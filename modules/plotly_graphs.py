import plotly.graph_objects as go

class WeatherGraphs:
    def __init__(self, df):
        self.df = df

    def create_temperature_dewpoint_graph(self):
        temperature_dewpoint_graph = go.Figure()
        temperature_dewpoint_graph.add_trace(go.Scatter(
            x=self.df['Timestamp'],
            y=self.df['Temperature'],
            mode='lines',
            name='Temperature',
            line=dict(color='red')
        ))

        temperature_dewpoint_graph.add_trace(go.Scatter(
            x=self.df['Timestamp'],
            y=self.df['Dew Point'],
            mode='lines',
            name='Dew Point',
            line=dict(color='green')
        ))

        temperature_dewpoint_graph.update_layout(
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=False,
                title='Degrees (°)',
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        )

        return temperature_dewpoint_graph

    def create_temperature_dewpoint_graph(df):
        temperature_dewpoint_graph = go.Figure()
        temperature_dewpoint_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Temperature'],
            mode='lines',
            name='Temperature',
            line=dict(color='red')
        ))

        temperature_dewpoint_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Dew Point'],
            mode='lines',
            name='Dew Point',
            line=dict(color='green')
        ))

        temperature_dewpoint_graph.update_layout(
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=False,
                title='Degrees (°)',
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        )

        return temperature_dewpoint_graph

    def create_humidity_graph(df):
        humidity_graph = go.Figure()
        humidity_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Humidity'],
            mode='lines',
            name='Humidity',
            line=dict(color='lightgreen')
        ))

        humidity_graph.update_layout(
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title='Humidity %',
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        return humidity_graph

    def create_wind_graph(df):
        wind_graph = go.Figure()
        wind_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Wind Speed'],
            mode='lines',
            name='Wind Speed',
            line=dict(color='navy')
        ))

        wind_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Wind Gust'],
            mode='markers',
            name='Wind Gust',
            marker=dict(color='orange')
        ))

        wind_graph.update_layout(
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title='MPH',
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        return wind_graph

    def create_rain_graph(df):
        rain_graph = go.Figure()
        rain_graph.add_trace(go.Bar(
            x=df['Timestamp'],
            y=df['Precip. Accum.'],
            name='Accumulation',
            marker=dict(color='cyan')
        ))

        rain_graph.add_trace(go.Bar(
            x=df['Timestamp'],
            y=df['Precip. Rate'],
            name='Rate',
            marker=dict(color='lawngreen')
        ))

        rain_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Precip. Rate'],
            name='Rate Line',
            mode='lines',
            line=dict(color='lawngreen')
        ))

        rain_graph.update_layout(
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title='Inches',
                showgrid=False
            ),
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        return rain_graph

    def create_pressure_graph(df):
        pressure_graph = go.Figure()
        pressure_graph.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Pressure'],
            mode='lines',
            name='Pressure',
            line=dict(color='black')
        ))

        pressure_graph.update_layout(
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                title='Inches',
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        return pressure_graph