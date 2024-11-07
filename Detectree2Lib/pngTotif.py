import os
from PIL import Image

input_folder = "/Test"  
output_folder = "/Test"  

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):  
        input_path = os.path.join(input_folder, filename)

        with Image.open(input_path) as img:
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.tif")

            img.save(output_path, format="TIFF")

        print(f"Geconverteerd: {filename} naar {output_path}")
