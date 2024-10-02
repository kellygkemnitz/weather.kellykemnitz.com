import plotly.graph_objects as go


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
        yaxis_title='Degrees (°)',
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
        yaxis_title='Humidity %',
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
        yaxis_title='MPH',
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
        yaxis_title='Inches',
        barmode='group',
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
        yaxis_title='Inches',
    )

    return pressure_graph