import os
import numpy as np
import json
from shapely.geometry import shape, mapping
from rasterio.features import geometry_mask
from rasterio.transform import from_bounds
from PIL import Image

base_geojson_path = '../Detectree2Lib/Own_Tiles/'  # Basispath voor Own_Tiles
base_image_path = '../Dashboard/tiles/cir/17/'  # Basispath voor cir-afbeeldingen
output_base_path = 'Own_Tiles'  # Basispath voor de output in Own_Tiles

ndvi_drempel = 0.33  # NDVI-drempelwaarde

# Functie om NDVI te berekenen
def calculate_average_pixel_value(polygon, pixels, transform):
    polygon_mask = geometry_mask([polygon], out_shape=pixels.shape[:2], transform=transform, invert=True)
    masked_pixels = pixels[polygon_mask]
    rood = masked_pixels[:, 0]
    infrarood = masked_pixels[:, 2]
    denominator = infrarood + rood
    denominator[denominator <= 0] = 1e-6  # Vermijd nulwaarden
    ndvi = (infrarood - rood) / denominator
    ndvi = np.nan_to_num(ndvi, nan=0.0)  # Vervang NaN door 0
    return np.mean(ndvi)

# Itereer door alle submappen in Own_Tiles
for root, dirs, files in os.walk(base_geojson_path):
    if root.endswith('predictions_geo'):  # Alleen mappen met de naam 'predictions_geo'
        geojson_dir = root  # Dit is de huidige predictions_geo-map
        parent_folder = os.path.basename(os.path.dirname(geojson_dir))  # Naam van de bovenliggende map (bijv. '66801')
        image_dir = os.path.join(base_image_path, parent_folder)  # Bijbehorende afbeelding-map
        
        # Verwerk alle GeoJSON-bestanden in de predictions_geo-map
        for geojson_file in os.listdir(geojson_dir):
            if geojson_file.endswith('.geojson'):
                geojson_path = os.path.join(geojson_dir, geojson_file)
                
                # Verbind bijbehorende afbeelding
                base_filename = os.path.splitext(geojson_file)[0].replace('Prediction_', '')  # Haal "Prediction_" weg
                image_file = base_filename + '.png'  # Afbeelding met numerieke naam
                image_path = os.path.join(image_dir, image_file)
                
                if not os.path.exists(image_path):
                    print(f"Afbeelding niet gevonden: {image_path}")
                    continue
                
                # Open GeoJSON en afbeelding
                with open(geojson_path) as f:
                    geojson_data = json.load(f)
                
                image = Image.open(image_path)
                image = image.convert("RGB")
                pixels = np.array(image)
                
                # Bereken transform
                height, width = pixels.shape[:2]
                min_x, min_y = 0, -256
                max_x, max_y = 256, 0
                transform = from_bounds(min_x, min_y, max_x, max_y, width, height)
                
                # Analyseer polygonen in GeoJSON
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
                
                # Samenvatting van de resultaten
                totaal_bomen = len(geojson_data['features'])
                percentage_gezond = (len(gezonde_bomen) / totaal_bomen) * 100 if totaal_bomen > 0 else 0
                print(f"Map: {parent_folder}, GeoJSON: {geojson_file}, Percentage gezonde bomen: {percentage_gezond:.2f}%")
                
                # Outputmap maken voor de specifieke afbeelding
                output_dir = os.path.join(base_geojson_path, parent_folder, 'collor_predictions')
                os.makedirs(output_dir, exist_ok=True)
                
                # Opslaan van ongezonde bomen in een nieuw GeoJSON-bestand
                output_path = os.path.join(output_dir, f'collor_{base_filename}.geojson')
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
                    
                    with open(output_path, 'w') as f:
                        json.dump(output_geojson, f)
                    
                    print(f"GeoJSON-laag met ongezonde bomen opgeslagen als {output_path}")
                else:
                    print("Alle bomen zijn gezond, GeoJSON met ongezonde bomen wordt niet aangemaakt.")
