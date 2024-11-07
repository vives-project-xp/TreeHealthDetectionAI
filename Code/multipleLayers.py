import json
import dash
from dash import html
from dash import dcc
import dash_leaflet as dl
from dash.dependencies import Output, Input
from flask import Flask, send_from_directory
import os
import pandas as pd

# Configuration settings
# Change the path to the directory of your RGB tiles
TILES_DIR = '/home/vives/project-experience/tiles/rgb'
# Change the path to the directory of your CIR tiles
CIR_TILES_DIR = '/home/vives/project-experience/tiles/cir'
DEFAULT_TILE = '/home/vives/project-experience/tree_pattern.avif'
TC_PORT = 8050
TC_HOST = 'localhost'


gemeenteCoordinates = pd.DataFrame(pd.read_json('./TreeHealthDetectionAI/Code/src/zipcode-belgium.json'))

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Route to RGB tiles
@server.route('/tiles/rgb/<int:z>/<int:x>/<int:y>.png')
def serve_rgb_tile(z, x, y):
    return serve_tile(z, x, y, TILES_DIR)

# Route to CIR tiles
@server.route('/tiles/cir/<int:z>/<int:x>/<int:y>.png')
def serve_cir_tile(z, x, y):
    return serve_tile(z, x, y, CIR_TILES_DIR)

# Correcting tiles layout
def serve_tile(z, x, y, tiles_dir):
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

    tile_path = os.path.join(tiles_dir, f"{z}/{x}/{inverted_y}.png")

    if os.path.exists(tile_path):
        return send_from_directory(tiles_dir, f"{z}/{x}/{inverted_y}.png")
    else:
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
            ],
            id='lc'
        )
    ], center=[-51.15, 3.21], zoom=17, style={"width": "100%", "height": "800px"}, id="map"),
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

# Callback to go to selected city
@app.callback(
    Output("map", "viewport"),
    Input("dropdown", "value"),
    prevent_initial_call=True
)
def update_map(selected_city):
    city_row = gemeenteCoordinates[gemeenteCoordinates['city'] == selected_city]
    lat, lng = city_row['lat'].values[0], city_row['lng'].values[0]

    return dict(center=(-lat,lng),zoom =15, transition="flyTo")
if __name__ == '__main__':
    app.run_server(port=TC_PORT, host=TC_HOST)
