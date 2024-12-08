import numpy as np
from PIL import Image, ImageEnhance
import cv2

def adjust_hue(image, hue_value):
    """
    Adjusts the hue of the image using HSV color space.
    """
    img_np = np.array(image)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    h = (h.astype(int) + hue_value) % 180  # Hue is cyclical in [0, 179]
    h = h.astype('uint8')
    hsv = cv2.merge([h, s, v])
    img_np = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return Image.fromarray(img_np)



def adjust_saturation(image, saturation_value):
    """
    Adjusts the saturation of the image using HSV color space.
    """
    img_np = np.array(image)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s.astype(int) + saturation_value, 0, 255).astype('uint8')
    hsv = cv2.merge([h, s, v])
    img_np = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return Image.fromarray(img_np)

def adjust_temperature(image, temperature_value):
    """
    Adjusts the image temperature by modifying blue and red channels.
    """
    img_np = np.array(image)
    b, g, r = cv2.split(img_np)
    r = np.clip(r.astype(int) - temperature_value, 0, 255).astype('uint8')
    b = np.clip(b.astype(int) + temperature_value, 0, 255).astype('uint8')
    img_np = cv2.merge([b, g, r])
    return Image.fromarray(img_np)

# Adjust Brightness
def adjust_brightness(image, brightness_value):
    scale = 1 + brightness_value / 100  # 0 => 1.0, 50 => 1.5, etc.
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(scale)


# Adjust Sharpness
def adjust_sharpness(image, sharpness_value):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(sharpness_value)