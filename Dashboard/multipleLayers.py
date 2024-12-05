import json
import dash
from dash import html
from dash import dcc
import dash_leaflet as dl
from dash.dependencies import Output, Input
from flask import Flask, send_from_directory
import os
import pandas as pd
import plotly.graph_objects as go  # Voor het genereren van de willekeurige staafgrafiek

# Configuration settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration settings
TILES_DIR = os.path.join(BASE_DIR, 'tiles/rgb')
CIR_TILES_DIR = os.path.join(BASE_DIR, 'tiles/cir')
TREE_DETECT_DIR = os.path.join(BASE_DIR, 'tiles/Processed_Tiles')
COLLOR_TILES_DIR = os.path.join(BASE_DIR, 'tiles/Collor_Tiles')  # Path for Collor Tiles
DEFAULT_TILE = os.path.join(BASE_DIR, 'tree_pattern.avif')
TC_PORT = 8050
TC_HOST = '0.0.0.0'

gemeenteCoordinates = pd.DataFrame(pd.read_json(os.path.join(BASE_DIR, 'assets/zipcode-belgium.json')))

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Route to RGB tiles, first check RGB and then CIR
@server.route('/tiles/rgb/<int:z>/<int:x>/<int:y>.png')
def serve_rgb_tile(z, x, y):
    return serve_tile(z, x, y, TILES_DIR, CIR_TILES_DIR)

# Route to CIR tiles, first check CIR and then RGB
@server.route('/tiles/cir/<int:z>/<int:x>/<int:y>.png')
def serve_cir_tile(z, x, y):
    return serve_tile(z, x, y, CIR_TILES_DIR, TILES_DIR)

# Route to tree detection tiles, first check Processed_Tiles, then RGB
@server.route('/tiles/Processed_Tiles/<int:z>/<int:x>/<int:y>.png')
def serve_detected_tile(z, x, y):
    return serve_tile(z, x, y, TREE_DETECT_DIR, TILES_DIR)

# Route for Collor tiles, first check Collor_Tiles, then CIR
@server.route('/tiles/Collor_Tiles/<int:z>/<int:x>/<int:y>.png')
def serve_collor_tile(z, x, y):
    return serve_tile(z, x, y, COLLOR_TILES_DIR, CIR_TILES_DIR)

# Correcting tiles layout
def serve_tile(z, x, y, primary_dir, alternative_dir=None):
    inverted_y = y
    max_y_values = {
        9: 341, 10: 682, 11: 1364, 12: 2729,
        13: 5459, 14: 10918, 15: 21837,
        16: 43674, 17: 87348
    }
    min_y_values = {
        9: 340, 10: 681, 11: 1363, 12: 2726,
        13: 5452, 14: 10905, 15: 21810,
        16: 43620, 17: 87241
    }

    if z in max_y_values:
        max_y = max_y_values[z]
        min_y = min_y_values[z]
        inverted_y = max_y - (y - min_y)

    # Try first in the primary directory
    tile_path = os.path.join(primary_dir, f"{z}/{x}/{inverted_y}.png")
    if os.path.exists(tile_path):
        return send_from_directory(primary_dir, f"{z}/{x}/{inverted_y}.png")

    # If not found, try the alternative directory
    if alternative_dir:
        tile_path = os.path.join(alternative_dir, f"{z}/{x}/{inverted_y}.png")
        if os.path.exists(tile_path):
            return send_from_directory(alternative_dir, f"{z}/{x}/{inverted_y}.png")

    # If not found in either directory, return the default tile
    return send_from_directory(os.path.dirname(DEFAULT_TILE), os.path.basename(DEFAULT_TILE))

# Layout
app.layout = html.Div(children=[
    dcc.Dropdown(
    [{'label': f"{row['city']} - {row['zip']}", 'value': row['city']}
                 for _, row in gemeenteCoordinates.iterrows()],
    placeholder="Selecteer een gemeente", id="dropdown"
    ),
    dl.Map([
        dl.LayersControl(
            [
                dl.BaseLayer(
                    dl.TileLayer(url='http://localhost:8050/tiles/rgb/{z}/{x}/{y}.png', attribution='RGB Layer'),
                    name='RGB', checked=True
                ),
                dl.BaseLayer(
                    dl.TileLayer(url='http://localhost:8050/tiles/cir/{z}/{x}/{y}.png', attribution='CIR Layer'),
                    name='CIR'
                ),
                dl.BaseLayer(  
                    dl.TileLayer(url='http://localhost:8050/tiles/Processed_Tiles/{z}/{x}/{y}.png', attribution='Tree Detection Layer'),
                    name='Tree Detection'
                ),
                dl.BaseLayer(
                    dl.TileLayer(url='http://localhost:8050/tiles/Collor_Tiles/{z}/{x}/{y}.png', attribution='Collor Tiles Layer'),
                    name='Ongezonde bomen'
                )
            ],
            id='lc'
        )
    ], 
    center=[-51.15, 3.21], 
    zoom=17, 
    style={"width": "100%", "height": "800px"}, 
    id="map", 
    bounceAtZoomLimits=True,
    maxZoom=17,
    minZoom=9
    ),
    # De willekeurige staafgrafiek wordt hier toegevoegd
    html.Div(children=[
        dcc.Graph(id='random-bar-chart')
    ], style={"height": "300px", "width": "100%"}),
    html.Div(children=[
        html.Div(id="label")
    ], className="info")
], style={"display": "grid", "width": "100%", "height": "100vh"})

# Callbacks
@app.callback(Output("label", "children"), [Input("map", 'click_lat_lng')])
def update_label(click_lat_lng):
    if not click_lat_lng:
        return "-"
    return "{:.3f} {}".format(0.0, "units")

@app.callback(
    Output("map", "viewport"),
    Input("dropdown", "value"),
    prevent_initial_call=True
)
def update_map(selected_city):
    city_row = gemeenteCoordinates[gemeenteCoordinates['city'] == selected_city]
    lat, lng = city_row['lat'].values[0], city_row['lng'].values[0]

    return dict(center=(lat-102.351,lng), zoom=15, transition="flyTo")

@app.callback(
    Output("map", "zoom"),
    Input("lc", "activeBaseLayer"),
    prevent_initial_call=True
)
def update_zoom_level(active_layer):
    if active_layer == 'Tree Detection':
        return 17
    else:
        return 15  # Default zoom for other layers

# Callback voor de willekeurige staafgrafiek
@app.callback(
    Output('random-bar-chart', 'figure'),
    Input('dropdown', 'value')
)
def update_random_bar_chart(selected_city):
    # Willekeurige waarden genereren voor de staafgrafiek
    import random
    random_values = [random.randint(1, 100) for _ in range(5)]  # 5 willekeurige waarden tussen 1 en 100

    # Maak de staafgrafiek
    fig = go.Figure(
        data=[go.Bar(x=[f"Item {i+1}" for i in range(5)], y=random_values, name='Random Data')],
        layout=go.Layout(title="Willekeurige Staafgrafiek")
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(port=TC_PORT, host=TC_HOST, debug=True)
