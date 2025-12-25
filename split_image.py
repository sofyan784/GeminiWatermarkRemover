from PIL import Image
import os

img_path = "artworks/comparison.png"
if os.path.exists(img_path):
    with Image.open(img_path) as img:
        width, height = img.size
        
        # Split Left/Right
        left = img.crop((0, 0, width // 2, height))
        right = img.crop((width // 2, 0, width, height))
        
        left.save("sample_left.png")
        right.save("sample_right.png")
        print("Saved sample_left.png and sample_right.png")
else:
    print("File not found.")
