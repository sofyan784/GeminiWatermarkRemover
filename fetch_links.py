import urllib.request
import re

url = "https://github.com/allenk/GeminiWatermarkTool/releases/expanded_assets/v0.1.2"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        matches = re.findall(r'href=[\'"]?([^\'" >]*releases/download[^\'" >]*)', html)
        for match in matches:
            if "Windows" in match:
                print(f"https://github.com{match}")
except Exception as e:
    print(f"Error: {e}")
