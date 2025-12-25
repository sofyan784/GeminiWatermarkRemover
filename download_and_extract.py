import urllib.request
import zipfile
import os

url = "https://github.com/allenk/GeminiWatermarkTool/releases/download/v0.1.2/GeminiWatermarkTool-Windows-x64.zip"
zip_path = "GeminiWatermarkTool-Windows-x64.zip"

print(f"Downloading {url}...")
try:
    urllib.request.urlretrieve(url, zip_path)
    print("Download complete.")
    
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(".")
    print("Extraction complete.")
except Exception as e:
    print(f"Error: {e}")
