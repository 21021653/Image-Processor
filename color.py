import numpy as np
from PIL import Image, ImageEnhance
import cv2

def adjust_hue(image_path, hue_shift):
    """
    Adjust the hue of an image by shifting the hue channel in the HSV color space.
    :param image_path: Path to the input image.
    :param hue_shift: Hue shift in degrees (-180 to 180).
    :return: Hue-adjusted image (PIL Image).
    """
    image = Image.open(image_path)
    img_hsv = image.convert("HSV")
    h, s, v = img_hsv.split()

    # Convert the hue channel to a NumPy array
    h = np.array(h, dtype=np.int32)
    
    # Apply hue shift, ensuring the hue is within the correct range (0-255)
    h = (h + hue_shift) % 256

    # Convert back to PIL Image
    h = Image.fromarray(h.astype(np.uint8), mode="L")
    return Image.merge("HSV", (h, s, v)).convert("RGB")


def adjust_saturation(image_path, saturation_factor):
    """
    Adjust the saturation of the image.
    :param image_path: Path to the input image.
    :param saturation_factor: Saturation factor (1.0 means no change, <1.0 reduces saturation, >1.0 increases saturation).
    :return: Saturation-adjusted image (PIL Image).
    """
    image = Image.open(image_path)
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(saturation_factor)


def adjust_temperature(image_path, temperature_factor):
    """
    Adjust the color temperature of the image (adds warm or cool filter).
    :param image_path: Path to the input image.
    :param temperature_factor: Temperature adjustment factor (positive for warm, negative for cool).
    :return: Temperature-adjusted image (PIL Image).
    """
    image = Image.open(image_path)
    img_np = np.array(image)

    # Apply temperature shift (increase red for warmth, increase blue for coolness)
    temp_img = img_np.copy()

    if temperature_factor > 0:
        temp_img[..., 2] = np.clip(temp_img[..., 2] + temperature_factor, 0, 255)  # R for warmth
    else:
        temp_img[..., 0] = np.clip(temp_img[..., 0] - temperature_factor, 0, 255)  # B for coolness

    return Image.fromarray(temp_img)
