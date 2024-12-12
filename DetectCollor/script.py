import os
import numpy as np
import json
from shapely.geometry import shape, mapping
from rasterio.features import geometry_mask
from rasterio.transform import from_bounds
from PIL import Image

base_geojson_path = '../Detectree2Lib/Own_Tiles/'  # Basispath voor Own_Tiles
base_image_path = '../Dashboard/tiles/cir/17/'  # Basispath voor cir-afbeeldingen
output_base_path = '../Dashboard/tiles/Collor_Tiles'  # Basispath voor de output in Own_Tiles

# Functie om NDVI te berekenen
def calculate_average_pixel_value(polygon, pixels, transform):
    polygon_mask = geometry_mask([polygon], out_shape=pixels.shape[:2], transform=transform, invert=True)
    masked_pixels = pixels[polygon_mask]
    
    rood = masked_pixels[:, 0]
    infrarood = masked_pixels[:, 2]
    
    print("Rood:", rood)
    print("Infrarood:", infrarood)
    
    denominator = infrarood + rood
    denominator[denominator == 0] = 1e-6  # Vermijd deling door nul
    
    # Bereken de NDVI
    ndvi = (infrarood - rood) / denominator
    print("Gecorrigeerde NDVI:", ndvi)
    
    # Vervang NaN en infinity door 0
    ndvi = np.nan_to_num(ndvi, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Zorg ervoor dat de NDVI tussen -1 en 1 valt
    ndvi = np.clip(ndvi, -1, 1)  # Forceer NDVI tussen -1 en 1
    
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
                for feature in geojson_data['features']:
                    if feature['geometry']['type'] == 'Polygon':
                        polygon = shape(feature['geometry'])
                        avg_ndvi = calculate_average_pixel_value(polygon, pixels, transform)
                        
                        # Voeg de berekende NDVI toe aan de properties van het feature
                        feature['properties']['ndvi'] = avg_ndvi
                
                # Outputmap maken voor de specifieke afbeelding
                output_dir = os.path.join(base_geojson_path, parent_folder, 'collor_predictions')
                os.makedirs(output_dir, exist_ok=True)
                
                # Opslaan van de gewijzigde GeoJSON-bestanden met de NDVI-waarde
                output_path = os.path.join(output_dir, f'collor_{base_filename}.geojson')
                with open(output_path, 'w') as f:
                    json.dump(geojson_data, f)
                
                print(f"GeoJSON met NDVI-waarde opgeslagen als {output_path}")
