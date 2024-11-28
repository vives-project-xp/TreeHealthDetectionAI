import numpy as np
import json
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union
from rasterio.features import geometry_mask, shapes
from rasterio.transform import from_bounds
from PIL import Image

geojson_path = '../Detectree2Lib/Own_Tiles/66706/predictions_geo/Prediction_87247.geojson'  
with open(geojson_path) as f:
    geojson_data = json.load(f)

image_path = '../Dashboard/tiles/cir/17/66706/87247.png' 
image = Image.open(image_path)
image = image.convert("RGB")
pixels = np.array(image)

height, width = pixels.shape[:2]

min_x, min_y = 100, -300  
max_x, max_y = 300, -50

transform = from_bounds(min_x, min_y, max_x, max_y, width, height)

mask = np.zeros((height, width), dtype=bool)

for feature in geojson_data['features']:
    if feature['geometry']['type'] == 'Polygon':
        polygon = shape(feature['geometry'])
        mask |= geometry_mask([polygon], out_shape=mask.shape, transform=transform, invert=True)

# Bereken de NDVI
infrarood = pixels[:, :, 2]  # Infrarood (bijvoorbeeld de derde band)
rood = pixels[:, :, 0]       # Rood (bijvoorbeeld de eerste band)

denominator = infrarood + rood
denominator[denominator == 0] = 1e-6  # Voorkom deling door nul

ndvi = (infrarood - rood) / denominator

# Drempelwaarde voor gezonde bomen (NDVI > 0.2)
ndvi_drempel = 0.2  
gezonde_masker = (ndvi > ndvi_drempel) & mask  

# Tel het aantal gezonde pixels
gezonde_pixels = np.sum(gezonde_masker)
totaal_pixels = np.sum(mask)

# Bereken het percentage van gezonde bomen
if totaal_pixels > 0:
    percentage_gezond = (gezonde_pixels / totaal_pixels) * 100
else:
    percentage_gezond = 0

print(f"Percentage gezonde bomen: {percentage_gezond:.2f}%")

# Nu de geometrieën van de gezonde bomen ophalen
gezonde_geom = []
for geom, value in shapes(gezonde_masker.astype(np.uint8), mask=gezonde_masker, transform=transform):
    if value == 1:
        poly = shape(geom)
        gezonde_geom.append(poly)

gezonde_union = unary_union(gezonde_geom)

# Maak het output GeoJSON bestand aan
output_geojson = {
    "type": "FeatureCollection",
    "features": []
}

if gezonde_union.is_empty:
    print("Geen gezonde bomen gevonden.")
else:
    if isinstance(gezonde_union, Polygon):
        polygons = [gezonde_union]
    elif isinstance(gezonde_union, MultiPolygon):
        polygons = list(gezonde_union.geoms)
    
    for polygon in polygons:
        feature = {
            "type": "Feature",
            "geometry": mapping(polygon),
            "properties": {"gezond": True}
        }
        output_geojson["features"].append(feature)

output_path = 'gezonde_bomen_layer.geojson'  
with open(output_path, 'w') as f:
    json.dump(output_geojson, f)

print(f"GeoJSON-laag met gezonde bomen opgeslagen als {output_path}")
