import os
import json
from PIL import Image, ImageDraw

input_base_folder = '../Detectree2Lib/Own_Tiles/'
output_base_folder = './tiles/Processed_Tiles/'

def geo_to_pixel(lon, lat, img_width, img_height):
    min_longitude, max_longitude = 0, 256
    min_latitude, max_latitude = -256, 0
    x_pixel = ((lon - min_longitude) / (max_longitude - min_longitude)) * img_width
    y_pixel = (1 - (lat - min_latitude) / (max_latitude - min_latitude)) * img_height
    return x_pixel, y_pixel

def process_image(image_path, geojson_path, output_image_path):
    img = Image.open(image_path)
    img_width, img_height = img.size

    with open(geojson_path) as f:
        geojson_data = json.load(f)

    draw = ImageDraw.Draw(img)

    for feature in geojson_data['features']:
        geometry = feature['geometry']
        
        if geometry['type'] == 'Point':
            lon, lat = geometry['coordinates']
            x, y = geo_to_pixel(lon, lat, img_width, img_height)
            radius = 2
            bbox = (x - radius, y - radius, x + radius, y + radius)
            draw.ellipse(bbox, outline="red", fill=None)

        elif geometry['type'] == 'LineString':
            coordinates = geometry['coordinates']
            pixel_coords = [geo_to_pixel(lon, lat, img_width, img_height) for lon, lat in coordinates]
            draw.line(pixel_coords, fill="red", width=1)

        elif geometry['type'] == 'Polygon':
            for ring in geometry['coordinates']:
                pixel_coords = [geo_to_pixel(lon, lat, img_width, img_height) for lon, lat in ring]
                draw.line(pixel_coords + [pixel_coords[0]], fill="red", width=1)

    img.save(output_image_path)
    print(f"Image saved with polygons and lines at: {output_image_path}")

for root, dirs, files in os.walk(input_base_folder):
    if 'predictions_geo' in dirs:
        geojson_folder = os.path.join(root, 'predictions_geo')
        
        relative_folder_path = os.path.relpath(root, input_base_folder)
        output_folder = os.path.join(output_base_folder, relative_folder_path)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for geojson_file in os.listdir(geojson_folder):
            if geojson_file.endswith('.geojson'):
                base_name = geojson_file.replace('Prediction_', '').replace('.geojson', '')

                image_files = [f for f in os.listdir(root) if f.endswith('.png') and base_name in f]

                for image_file in image_files:
                    image_path = os.path.join(root, image_file)
                    geojson_path = os.path.join(geojson_folder, geojson_file)
                    output_image_path = os.path.join(output_folder, f"{base_name}.png")

                    process_image(image_path, geojson_path, output_image_path)

                    print(f"Processed {image_file} with GeoJSON {geojson_file} and saved to {output_image_path}")
