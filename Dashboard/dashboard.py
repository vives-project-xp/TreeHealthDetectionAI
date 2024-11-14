import json
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl
from dash.dependencies import Output, Input
from flask import Flask, send_from_directory, abort
import os

# Configuration settings
TILES_DIR = '/home/vives/project-experience/tiles'
DEFAULT_TILE = '/home/vives/project-experience/notfound.jpg'
TC_PORT = 8050
TC_HOST = 'localhost'
keys = ["RGB", "CIR"]

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Define a route to serve the GDAL tiles
@server.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def serve_tile(z, x, y):
    inverted_y = y
    if z == 10:
        max_y = 682
        inverted_y = max_y - (y - 681)
    elif z == 11:
        max_y = 1364
        inverted_y = max_y - (y - 1363)
    elif z == 12:
        max_y = 2729
        inverted_y = max_y - (y - 2726)
    elif z == 13:
        max_y = 5459
        inverted_y = max_y - (y - 5452)
    elif z == 14:
        max_y = 10918
        inverted_y = max_y - (y - 10905)
    elif z == 15:
        max_y = 21837
        inverted_y = max_y - (y - 21810)
    elif z == 16:
        max_y = 43674
        inverted_y = max_y - (y - 43620)
    elif z == 17:
        max_y = 87348
        inverted_y = max_y - (y - 87241) 
    tile_path = os.path.join(TILES_DIR, f"{z}/{x}/{inverted_y}.png")

    if os.path.exists(tile_path):
        return send_from_directory(TILES_DIR, f"{z}/{x}/{inverted_y}.png")
    else:
        return send_from_directory(os.path.dirname(DEFAULT_TILE), os.path.basename(DEFAULT_TILE))

# Layout
app.layout = html.Div(children=[
    dl.Map(id="map", center=[-51.2, 3.6], zoom=17, children=[
        dl.TileLayer(url='http://localhost:8050/tiles/{z}/{x}/{y}.png'),
    ], style={"width": "100%", "height": "800px"}),
    html.Div(children=[
    ], className="info")
], style={"display": "grid", "width": "100%", "height": "100vh"})

# Callbacks (unchanged)
@app.callback(Output("label", "children"), [Input("map", 'click_lat_lng')])
def update_label(click_lat_lng):
    if not click_lat_lng:
        return "-"
    return "{:.3f} {}".format(0.0, "units")

if __name__ == '__main__':
    app.run_server(port=TC_PORT, host=TC_HOST)
