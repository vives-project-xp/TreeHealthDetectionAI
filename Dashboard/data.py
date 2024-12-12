import os
import json

geojson_base_folder = './Own_Tiles/'

def extract_ndvi_from_geojson(geojson_path):
    with open(geojson_path, 'r') as file:
        data = json.load(file)
    
    ndvi_list = []
    for feature in data.get('features', []):
        ndvi = feature.get('properties', {}).get('ndvi', None)
        if ndvi is not None:
            ndvi_list.append(ndvi)
    return ndvi_list

def collect_all_ndvi_values(base_folder):
    all_ndvi_values = []
    for root, dirs, files in os.walk(base_folder):
        if 'collor_predictions' in root: 
            for file in files:
                if file.endswith('.geojson'):
                    geojson_path = os.path.join(root, file)
                    all_ndvi_values.extend(extract_ndvi_from_geojson(geojson_path))
    return all_ndvi_values

def calculate_ndvi_intervals(ndvi_values):
    intervals = {f"{i/10:.1f}-{(i+1)/10:.1f}": 0 for i in range(10)}
    total_values = len(ndvi_values)
    if total_values == 0:
        return intervals

    for ndvi in ndvi_values:
        for i in range(10):
            if i / 10 <= ndvi < (i + 1) / 10:
                intervals[f"{i/10:.1f}-{(i+1)/10:.1f}"] += 1
                break

    for interval in intervals:
        intervals[interval] = (intervals[interval] / total_values) * 100
    return intervals

all_ndvi_values = collect_all_ndvi_values(geojson_base_folder)

ndvi_percentages = calculate_ndvi_intervals(all_ndvi_values)