import numpy as np
import json
from shapely.geometry import shape, mapping
from rasterio.features import geometry_mask
from rasterio.transform import from_bounds
from PIL import Image

geojson_path = '../Detectree2Lib/Own_Tiles/66706/predictions_geo/Prediction_87247.geojson'
image_path = '../Dashboard/tiles/cir/17/66706/87247.png'

with open(geojson_path) as f:
    geojson_data = json.load(f)

image = Image.open(image_path)
image = image.convert("RGB")
pixels = np.array(image)

height, width = pixels.shape[:2]

min_x, min_y = 0, -256
max_x, max_y = 256, 0
transform = from_bounds(min_x, min_y, max_x, max_y, width, height)

mask = np.zeros((height, width), dtype=bool)

for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Polygon':
        polygon = shape(feature['geometry'])
        mask |= geometry_mask([polygon], out_shape=mask.shape, transform=transform, invert=True)

def calculate_average_pixel_value(polygon, pixels, transform):
    polygon_mask = geometry_mask([polygon], out_shape=pixels.shape[:2], transform=transform, invert=True)
    masked_pixels = pixels[polygon_mask]
    rood = masked_pixels[:, 0]
    infrarood = masked_pixels[:, 2]
    denominator = infrarood + rood
    denominator[denominator == 0] = 1e-6
    ndvi = (infrarood - rood) / denominator
    return np.mean(ndvi)

ndvi_drempel = 0.33

gezonde_bomen = []
ongezonde_bomen = []
for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Polygon':
        polygon = shape(feature['geometry'])
        avg_ndvi = calculate_average_pixel_value(polygon, pixels, transform)
        if avg_ndvi > ndvi_drempel:
            gezonde_bomen.append(polygon)
        else:
            ongezonde_bomen.append(polygon)

totaal_bomen = len(geojson_data['features'])
percentage_gezond = (len(gezonde_bomen) / totaal_bomen) * 100 if totaal_bomen > 0 else 0
print(f"Percentage gezonde bomen: {percentage_gezond:.2f}%")

if percentage_gezond < 100:
    output_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for polygon in ongezonde_bomen:
        feature = {
            "type": "Feature",
            "geometry": mapping(polygon),
            "properties": {"gezond": False}
        }
        output_geojson["features"].append(feature)

    output_path = 'ongezonde_bomen_layer.geojson'
    with open(output_path, 'w') as f:
        json.dump(output_geojson, f)

    print(f"GeoJSON-laag met ongezonde bomen opgeslagen als {output_path}")
else:
    print("Alle bomen zijn gezond, GeoJSON met ongezonde bomen wordt niet aangemaakt.")
