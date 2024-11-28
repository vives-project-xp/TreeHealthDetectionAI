import os
import cv2
import json
import rasterio
from rasterio.crs import CRS
from pathlib import Path
import numpy as np
from detectree2.models.outputs import polygon_from_mask
from detectree2.models.train import setup_cfg
from detectron2.evaluation.coco_evaluation import instances_to_coco_json
from detectron2.engine import DefaultPredictor
from detectree2.models.train import get_filenames, get_tree_dicts
import pycocotools.mask as mask_util


def check_and_load_image(image_path):
    """Check if image exists and can be loaded."""
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist.")
        return None
    img = cv2.imread(image_path)
    if img is None:
        print(f"Warning: Unable to load image at {image_path}. Skipping.")
        return None
    return img


def is_valid_image(file_path):
    """Check if a file is a valid image."""
    if not os.path.isfile(file_path):
        return False
    valid_extensions = (".png", ".jpg", ".jpeg", ".tif")
    return file_path.lower().endswith(valid_extensions)


def process_tiles(tiles_path, trained_model, crs="EPSG:4326", multi_class=False):
    def assign_crs_if_missing(tif_path, crs="EPSG:4326"):
        """Check and assign CRS to .tif file if missing."""
        with rasterio.open(tif_path, 'r+') as dataset:
            if dataset.crs is None:
                print(f"CRS missing for {tif_path}. Setting CRS to {crs}.")
                dataset.crs = CRS.from_string(crs)
            else:
                print(f"CRS present for {tif_path}: {dataset.crs}")

    def validate_crs(tif_path):
        """Validate CRS of .tif file."""
        with rasterio.open(tif_path) as dataset:
            if dataset.crs is None:
                raise ValueError(f"The file {tif_path} has no valid CRS.")
            return dataset.crs

    def project_to_geojson(tiles_path, pred_fold=None, output_fold=None, multi_class=False):
        """Project JSON predictions back into geographical space."""
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
                    print(f"Error during coordinate conversion for {filename}: {e}")
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

    def predict_on_data(
        directory: str = "./",
        out_folder: str = "predictions",
        predictor=DefaultPredictor,
        eval=False,
        save: bool = True,
        num_predictions=0,
    ):
        """Make predictions on tiled data.

        Predicts crowns for all png images present in a directory and outputs masks as jsons.
        """

        pred_dir = os.path.join(directory, out_folder)
        Path(pred_dir).mkdir(parents=True, exist_ok=True)

        # Alternatieve implementatie
        dataset_dicts = []

        # Zoek naar bestanden afhankelijk van eval
        if eval:
            # Zoek PNG-bestanden in de directory en subdirectories
            files = Path(directory).rglob("*.png")
        else:
            # Zoek PNG-bestanden alleen in de hoofddirectory
            files = Path(directory).glob("*.png")

        # Bouw de dataset op
        for file in files:
            dataset_dicts.append({"file_name": str(file.resolve())})

        # Debugging: Laat zien wat er in dataset_dicts zit
        print(f"Dataset dicts: {dataset_dicts}")

        total_files = len(dataset_dicts)

        # Works out if all items in folder should be predicted on
        if num_predictions == 0:
            num_to_pred = len(dataset_dicts)
        else:
            num_to_pred = num_predictions

        print(f"Predicting {num_to_pred} files")

        for i, d in enumerate(dataset_dicts[:num_to_pred], start=1):
            print("----------------------------------------------------------------------------------")
            img_path = d["file_name"]
            print(img_path)

            # Check if the image exists before trying to load it
            if not os.path.exists(img_path):
                print(f"Warning: Image file {img_path} not found, skipping.")
                continue

            # Load image and handle errors
            img = cv2.imread(img_path)
            if img is None:
                print(f"Warning: Unable to load image {img_path}, skipping.")
                continue

            try:
                # Perform prediction
                outputs = predictor(img)

                # Create the output file name
                file_name = os.path.basename(img_path)
                file_name = file_name.replace("png", "json")  # Change extension to .json
                output_file = os.path.join(pred_dir, f"Prediction_{file_name}")

                if save:
                    # Convert the predictions to JSON and save them
                    evaluations = instances_to_coco_json(outputs["instances"].to("cpu"), img_path)
                    with open(output_file, "w") as dest:
                        json.dump(evaluations, dest)

            except Exception as e:
                print(f"Error during prediction for {img_path}: {e}")

            if i % 50 == 0:
                print(f"Predicted {i} files of {total_files}")

    cfg = setup_cfg(update_model=trained_model)
    cfg.MODEL.DEVICE = 'cpu'

    # Initialiseer de predictor één keer
    predictor = DefaultPredictor(cfg)

    # Gebruik predict_on_data om voorspellingen uit te voeren
    # Geef de map op waar de afbeeldingen zijn opgeslagen, de outputmap voor de voorspellingen
    # en de andere vereiste parameters door.
    predict_on_data(directory=tiles_path, out_folder="predictions", predictor=predictor, eval=False, save=True)

    # Projecteer de voorspellingen naar GeoJSON
    project_to_geojson(tiles_path, tiles_path + "predictions/", tiles_path + "predictions_geo/")

    # Schoonmaken
    try:
        os.rmdir('/data/train_outputs')
    except Exception as e:
        print(f"Could not remove directory '/data/train_outputs': {e}")
