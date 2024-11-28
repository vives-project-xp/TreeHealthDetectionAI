import dash
from dash import html, dcc
import json
from PIL import Image

image_path = './assets/87266.png'
geojson_path = './assets/Prediction_87266.geojson'

img = Image.open(image_path)
img_width, img_height = img.size

min_longitude, max_longitude = 0, 260
min_latitude, max_latitude = -260, 0

with open(geojson_path) as f:
    geojson_data = json.load(f)

def geo_to_pixel(lon, lat):
    x_pixel = ((lon - min_longitude) / (max_longitude - min_longitude)) * img_width
    y_pixel = (1 - (lat - min_latitude) / (max_latitude - min_latitude)) * img_height
    return x_pixel, y_pixel

overlay_points = []
for feature in geojson_data['features']:
    geometry = feature['geometry']
    if geometry['type'] == 'Point':
        lon, lat = geometry['coordinates']
        x, y = geo_to_pixel(lon, lat)
        overlay_points.append((x, y))
    elif geometry['type'] == 'LineString':
        for lon, lat in geometry['coordinates']:
            x, y = geo_to_pixel(lon, lat)
            overlay_points.append((x, y))
    elif geometry['type'] == 'Polygon':
        for ring in geometry['coordinates']:
            for lon, lat in ring:
                x, y = geo_to_pixel(lon, lat)
                overlay_points.append((x, y))

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(style={"position": "relative", "display": "inline-block"}, children=[
        html.Img(
            src='/assets/87266.png',
            style={"width": "100%", "height": "auto"}
        ),
        html.Div(children=[
            html.Div(
                style={
                    "position": "absolute",
                    "top": f"{y}px",
                    "left": f"{x}px",
                    "width": "5px",
                    "height": "5px",
                    "background-color": "red",
                    "border-radius": "10%"
                }
            ) for x, y in overlay_points
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
