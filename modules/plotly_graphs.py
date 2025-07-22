import plotly.graph_objects as go

class Graphs:
    def create_graphs(self, df):
        return {
            "temperature_dewpoint": self._create_temperature_dewpoint_graph(df),
            "humidity": self._create_humidity_graph(df),
            "wind": self._create_wind_graph(df),
            "rain": self._create_rain_graph(df),
            "pressure": self._create_pressure_graph(df)
        }

    def _common_layout(self, fig, y_title: str):
        fig.update_layout(
            autosize=True,
            # margin=dict(l=40, r=40, t=40, b=40),
            hovermode='x',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, title=y_title),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5,
            )
        )
        return fig

    def _create_temperature_dewpoint_graph(self, df):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Temperature'],
            mode='lines',
            name='Temperature',
            line=dict(color='red')
        ))

        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Dew Point'],
            mode='lines',
            name='Dew Point',
            line=dict(color='green')
        ))
        
        return self._common_layout(fig, 'Degrees (°)')

    def _create_humidity_graph(self, df):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Humidity'],
            mode='lines',
            name='Humidity',
            line=dict(color='lightgreen')
        ))
        
        return self._common_layout(fig, 'Humidity %')

    def _create_wind_graph(self, df):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Wind Speed'],
            mode='lines',
            name='Wind Speed',
            line=dict(color='navy')
        ))

        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Wind Gust'],
            mode='lines',
            name='Wind Gust',
            line=dict(color='orange')
        ))
        
        return self._common_layout(fig, 'MPH')

    def _create_rain_graph(self, df):
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df['Timestamp'],
            y=df['Precip. Accum.'],
            name='Accumulation',
            marker=dict(color='cyan')
        ))

        fig.add_trace(go.Bar(
            x=df['Timestamp'],
            y=df['Precip. Rate'],
            name='Rate',
            marker=dict(color='lawngreen')
        ))

        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Precip. Rate'],
            name='Rate Line',
            mode='lines',
            line=dict(color='lawngreen')
        ))

        fig.update_layout(barmode='group')

        return self._common_layout(fig, 'Inches')

    def _create_pressure_graph(self, df):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Timestamp'],
            y=df['Pressure'],
            mode='lines',
            name='Pressure',
            line=dict(color='black')
        ))

        return self._common_layout(fig, 'Inches')