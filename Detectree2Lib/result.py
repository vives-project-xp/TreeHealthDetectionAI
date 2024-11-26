import os
from pngTotif import convert_png_to_tif
from Own_Tiles import process_tiles

input_folder = "./Own_Tiles"
output_folder = "./Own_Tiles"
tiles_path = "/data/Own_Tiles/"
trained_model = "./urban_trees_Cambridge_20230630.pth"


#Iterate through items in the input folder
for item in os.listdir(input_folder):
    item_path = os.path.join(input_folder, item)
    if os.path.isdir(item_path):
        item_path_output = item_path
        item_path_tiles = item_path + "/"

        # Convert PNG images to TIF format
        convert_png_to_tif(item_path, item_path_output)

        print(item_path_tiles)

        # Process the tiles using the trained model
        process_tiles(item_path_tiles, trained_model)