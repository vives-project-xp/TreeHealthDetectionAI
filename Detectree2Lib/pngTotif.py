from PIL import Image
import os

def convert_png_to_tif(input_folder, output_folder):
    """
    Converteert alle PNG-bestanden in de opgegeven input_folder naar TIFF en slaat ze op in output_folder.
    """
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            with Image.open(input_path) as img:
                output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.tif")
                img.save(output_path, format="TIFF")
            print(f"Geconverteerd: {filename} naar {output_path}")
