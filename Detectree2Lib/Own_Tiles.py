import os
import json
import rasterio
from rasterio.crs import CRS
from pathlib import Path
import numpy as np
from detectree2.models.outputs import polygon_from_mask,stitch_crowns, clean_crowns
from detectree2.models.predict import predict_on_data
from detectree2.models.train import setup_cfg
from detectron2.engine import DefaultPredictor
import pycocotools.mask as mask_util
from pngTotif import convert_png_to_tif

input_folder = "./Own_Tiles"
output_folder = "./Own_Tiles"

convert_png_to_tif(input_folder, output_folder)

def check_directory_exists_and_list_files(dir_path):
    if os.path.exists(dir_path):
        if os.path.isdir(dir_path):
            print(f"De map '{dir_path}' is gevonden.")
            files = os.listdir(dir_path)
            if files:
                print("Bestanden in de map:")
                for file in files:
                    print(f"- {file}")
            else:
                print("De map is leeg.")
        else:
            print(f"'{dir_path}' bestaat, maar het is geen map.")
    else:
        print(f"De map '{dir_path}' is niet gevonden.")

def assign_crs_if_missing(tif_path, crs="EPSG:4326"):
    """Controleer en ken een CRS toe aan een .tif-bestand indien het ontbreekt."""
    with rasterio.open(tif_path, 'r+') as dataset:
        if dataset.crs is None:
            print(f"CRS ontbreekt voor {tif_path}. CRS wordt ingesteld op {crs}.")
            dataset.crs = CRS.from_string(crs)
        else:
            print(f"CRS is aanwezig voor {tif_path}: {dataset.crs}")

def validate_crs(tif_path):
    """Controleer of het .tif-bestand een geldige CRS heeft."""
    with rasterio.open(tif_path) as dataset:
        if dataset.crs is None:
            raise ValueError(f"Het bestand {tif_path} heeft geen geldige CRS.")
        return dataset.crs

def project_to_geojson(tiles_path, pred_fold=None, output_fold=None, multi_class: bool = False):  # noqa:N803
    """Projects json predictions back in geographic space."""

    Path(output_fold).mkdir(parents=True, exist_ok=True)
    entries = list(Path(pred_fold) / file for file in os.listdir(pred_fold) if Path(file).suffix == ".json")
    total_files = len(entries)
    print(f"Projecting {total_files} files")

    for idx, filename in enumerate(entries, start=1):
        if idx % 50 == 0:
            print(f"Projecting file {idx} of {total_files}: {filename}")

        tifpath = Path(tiles_path) / Path(filename.name.replace("Prediction_", "")).with_suffix(".tif")
        
        assign_crs_if_missing(tifpath)

        try:
            crs = validate_crs(tifpath)
        except ValueError as e:
            print(e)
            continue  

        with rasterio.open(tifpath) as data:
            epsg = CRS.from_string(data.crs.wkt).to_epsg()
            raster_transform = data.transform

        geofile = {
            "type": "FeatureCollection",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::" + str(epsg)
                },
            },
            "features": [],
        }

        with open(filename, "r") as prediction_file:
            datajson = json.load(prediction_file)

        for crown_data in datajson:
            if multi_class:
                category = crown_data["category_id"]
            crown = crown_data["segmentation"]
            confidence_score = crown_data["score"]

            mask_of_coords = mask_util.decode(crown)
            crown_coords = polygon_from_mask(mask_of_coords)
            if crown_coords == 0:
                continue

            crown_coords_array = np.array(crown_coords).reshape(-1, 2)

            try:
                x_coords, y_coords = rasterio.transform.xy(
                    transform=raster_transform,
                    rows=crown_coords_array[:, 1],
                    cols=crown_coords_array[:, 0]
                )
            except Exception as e:
                print(f"Fout bij coördinatenomzetting voor {filename}: {e}")
                continue 

            moved_coords = list(zip(y_coords, x_coords))  
        
            moved_coords_rotated = [(y, -x) for x, y in moved_coords]

            feature = {
                "type": "Feature",
                "properties": {
                    "Confidence_score": confidence_score,
                    "category": category if multi_class else None,
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [moved_coords_rotated],
                },
            }

            geofile["features"].append(feature)

        output_geo_file = os.path.join(output_fold, filename.with_suffix(".geojson").name)

        with open(output_geo_file, "w") as dest:
            json.dump(geofile, dest)


def main():
    tiles_path = "/data/Own_Tiles/" 
    result_path = "/data/Own_Tiles/result/" 
    check_directory_exists_and_list_files(tiles_path)

    trained_model = "./230103_randresize_full.pth"
    cfg = setup_cfg(update_model=trained_model)
    cfg.MODEL.DEVICE='cpu'

    predict_on_data(tiles_path, predictor=DefaultPredictor(cfg))

    project_to_geojson(tiles_path, tiles_path + "predictions/", tiles_path + "predictions_geo/")

    crowns = stitch_crowns(tiles_path + "predictions_geo/", 1)
    clean = clean_crowns(crowns, 0.6, confidence=0) 

    clean = clean[clean["Confidence_score"] > 0.5]

    clean = clean.set_geometry(clean.simplify(0.3))

    clean.to_file(tiles_path + "/crowns_out.gpkg")

    print("Tis gelukt")

if __name__ == "__main__":
    main()