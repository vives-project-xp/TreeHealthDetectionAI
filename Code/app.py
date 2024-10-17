import os
import dash
from dash import html
import dash_leaflet as dl
from flask import send_from_directory, abort
from flask_cors import CORS
import logging

app = dash.Dash(__name__)
CORS(app.server)

logging.basicConfig(level=logging.DEBUG)

BASEDIR = os.path.dirname(os.path.abspath(__file__))  
TILE_DIR = os.path.join(BASEDIR, 'tiles')  

@app.server.route('/tiles/<int:z>/<int:x>/<int:y>.png')
def servetile(z, x, y): 
    tile_path = os.path.join(TILE_DIR, f'{z}/{x}/{y}.png')
    logging.debug(f"Requesting tile at: {tile_path}")
        
    if os.path.isfile(tile_path):
        return send_from_directory(os.path.join(TILE_DIR, f'{z}'), f'{x}/{y}.png')
    else:
        logging.error(f"Tile not found: {tile_path}")
        abort(404)

tile_url = "http://localhost:8050/tiles/{z}/{x}/{y}.png"

app.layout = html.Div([
    dl.Map(center=[0, 0], zoom=17, children=[
        dl.TileLayer(url=tile_url, attribution="Custom Tiles"),
        dl.LayerGroup(id="layer")
    ], style={'width': '100%', 'height': '500px'}),
])

if __name__ == "__main__":
    app.run_server(debug=True)
