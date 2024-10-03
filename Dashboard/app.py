import dash_leaflet as dl
from dash import Dash
import terracotta as tc


tc.get_settings().DEFAULT_DRIVER = 'local'
datasets = tc.get_datasets()
keys = list(datasets.keys())
driver = tc.get_driver()
with driver.connect(): 
    for keys, dataset in datasets.items():
        driver.insert(keys, dataset)

url = "localhost:5000/datasets/{z}/{x}/{y}.png"

# Create app.
app = Dash()
app.layout = dl.Map([
    dl.TileLayer(url=url, maxZoom=20)
], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run_server()