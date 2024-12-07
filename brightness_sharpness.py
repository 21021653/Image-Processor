from PIL import Image, ImageEnhance
import cv2

def adjust_sharpness(image_path, sharpness_value):
    """Adjust sharpness of an image."""
    inp = Image.open(image_path)
    enhancer = ImageEnhance.Sharpness(inp)
    out = enhancer.enhance(sharpness_value)
    return out

def adjust_brightness(image_path, brightness_value):
    """Adjust brightness of an image."""
    inp = cv2.imread(image_path)
    alpha = 1 + brightness_value / 100  # Scale factor for brightness
    beta = 0  # Bias
    out = cv2.convertScaleAbs(inp, alpha=alpha, beta=beta)
    return out