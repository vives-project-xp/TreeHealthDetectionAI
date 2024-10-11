from detectree2.preprocessing.tiling import tile_data
from detectree2.models.outputs import project_to_geojson, stitch_crowns, clean_crowns
from detectree2.models.predict import predict_on_data
from detectree2.models.train import setup_cfg
from detectron2.engine import DefaultPredictor
import rasterio

img_path = "data/OMZRGB21VL_13.jp2"
tiles_path = "data/TreePredictions/"

buffer = 30
tile_width = 40
tile_height = 40
tile_data(img_path, tiles_path, buffer, tile_width, tile_height, dtype_bool = True)

trained_model = "./230103_randresize_full.pth"
cfg = setup_cfg(update_model=trained_model)

cfg.MODEL.DEVICE='cpu'

predict_on_data(tiles_path, predictor=DefaultPredictor(cfg))