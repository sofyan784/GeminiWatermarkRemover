import cv2
import numpy as np
import os

# Path to alpha maps
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
BG_48_PATH = os.path.join(ASSETS_DIR, "bg_48.bin")
BG_96_PATH = os.path.join(ASSETS_DIR, "bg_96.bin")

def load_alpha_map(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        bytes_data = f.read()
    nparr = np.frombuffer(bytes_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return None
    # Use max of RGB channels (Gemini watermark is white/gray)
    gray = np.max(img, axis=2)
    alpha_map = gray.astype(np.float32) / 255.0
    return alpha_map

class WatermarkEngine:
    def __init__(self):
        self.alpha_48 = load_alpha_map(BG_48_PATH)
        self.alpha_96 = load_alpha_map(BG_96_PATH)
        
        # Fallback if assets are missing
        if self.alpha_48 is None:
            self.alpha_48 = np.zeros((48, 48), dtype=np.float32)
        if self.alpha_96 is None:
            self.alpha_96 = cv2.resize(self.alpha_48, (96, 96), interpolation=cv2.INTER_LINEAR)
            
        self.logo_value = 255.0

    def remove_watermark(self, image, force_size=None):
        h, w = image.shape[:2]
        
        # Gemini's rules:
        # - Large (96x96, 64px margin): BOTH width AND height > 1024
        # - Small (48x48, 32px margin): Otherwise
        if force_size == "large" or (force_size is None and (w > 1024 and h > 1024)):
            alpha_map = self.alpha_96
            margin = 64
            size = 96
        else:
            alpha_map = self.alpha_48
            margin = 32
            size = 48
            
        # Position is bottom-right
        pos_x = w - margin - size
        pos_y = h - margin - size
        
        return self._apply_reverse_blend(image, alpha_map, (pos_x, pos_y))

    def _apply_reverse_blend(self, image, alpha_map, position):
        x, y = position
        ah, aw = alpha_map.shape
        ih, iw = image.shape[:2]
        
        # ROI coordinates
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(iw, x + aw), min(ih, y + ah)
        
        if x1 >= x2 or y1 >= y2:
            return image
            
        # Get ROIs
        alpha_roi = alpha_map[y1-y:y2-y, x1-x:x2-x]
        img_roi = image[y1:y2, x1:x2].astype(np.float32)
        
        # Reverse blending formula:
        # watermarked = alpha * logo + (1 - alpha) * original
        # original = (watermarked - alpha * logo) / (1 - alpha)
        
        alpha_threshold = 0.002
        max_alpha = 0.99
        
        alpha = np.minimum(alpha_roi, max_alpha)
        one_minus_alpha = 1.0 - alpha
        
        # Expand for broadcasting
        alpha_3d = alpha[:, :, np.newaxis]
        one_minus_alpha_3d = one_minus_alpha[:, :, np.newaxis]
        
        # Apply only where alpha is significant
        mask = alpha_roi >= alpha_threshold
        if np.any(mask):
            img_roi[mask] = (img_roi[mask] - alpha_3d[mask] * self.logo_value) / one_minus_alpha_3d[mask]
            img_roi = np.clip(img_roi, 0, 255)
        
        image[y1:y2, x1:x2] = img_roi.astype(np.uint8)
        return image

def process_image(input_path, output_path):
    try:
        engine = WatermarkEngine()
        img = cv2.imread(input_path)
        if img is None:
            return False
        
        # Ensure BGR
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
        img = engine.remove_watermark(img)
        
        # Save with high quality
        ext = os.path.splitext(output_path)[1].lower()
        params = []
        if ext in [".jpg", ".jpeg"]:
            params = [cv2.IMWRITE_JPEG_QUALITY, 100]
        elif ext == ".png":
            params = [cv2.IMWRITE_PNG_COMPRESSION, 6]
            
        return cv2.imwrite(output_path, img, params)
    except Exception:
        return False
