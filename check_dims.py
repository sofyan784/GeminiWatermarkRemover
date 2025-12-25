from PIL import Image
import os

img_path = "artworks/comparison.png"
if os.path.exists(img_path):
    with Image.open(img_path) as img:
        print(f"Dimensions: {img.size}")
else:
    print("File not found.")
