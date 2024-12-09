import cv2
import numpy as np
from matplotlib import pyplot as plt

def apply_filter(image, filter_type, kernel_strength):
    if isinstance(image, str):
        inp = cv2.imread(image)
    else:
        inp = image
    
    if kernel_strength == "3":
        kernel_size = 3
    elif kernel_strength == "5":
        kernel_size = 5
    elif kernel_strength == "7":
        kernel_size = 7
    elif kernel_strength == "9":
        kernel_size = 9
    elif kernel_strength == "11":
        kernel_size = 11
    elif kernel_strength == "13":
        kernel_size = 13
    elif kernel_strength == "15":
        kernel_size = 15

    if filter_type == "Median Filter":
        out = cv2.medianBlur(inp, kernel_size)
    elif filter_type == "Gaussian Filter":
        out = cv2.GaussianBlur(inp, (kernel_size, kernel_size), 0)
    elif filter_type == "Box Filter":
        out = cv2.blur(inp, (kernel_size, kernel_size))
    elif filter_type == "NL Means":
        out = cv2.fastNlMeansDenoisingColored(inp, None, kernel_size, kernel_size, 7, 21)
    
    return out

def add_noise(image_path, noise_type):
    inp = cv2.imread(image_path)
    
    if noise_type == "Salt and Pepper":
        out = add_salt_pepper_noise(inp, salt_prob=0.1,pepper_prob=0.1)
    elif noise_type == "Gaussian":
        out = add_gaussian_noise(inp, mean=0,std=35)
    return out

def add_gaussian_noise(image, mean=0, std=25):
    """
    Add Gaussian noise to an image.
    """
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 255).astype(np.uint8)

def add_salt_pepper_noise(image, salt_prob=0.02, pepper_prob=0.02):
    """
    Add salt-and-pepper noise to an image.
    """
    noisy_image = np.copy(image)
    total_pixels = image.size
    num_salt = int(salt_prob * total_pixels)
    num_pepper = int(pepper_prob * total_pixels)

    # Add salt noise
    coords_salt = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[tuple(coords_salt)] = 255

    # Add pepper noise
    coords_pepper = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[tuple(coords_pepper)] = 0

    return noisy_image

def psnr(original, filtered):
    """
    Calculate Peak Signal-to-Noise Ratio (PSNR).
    """
    mse = np.mean((original - filtered) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))

def plot_images(original, noisy, filtered, filter_name, psnr_value):
    """
    Plot the original, noisy, and filtered images.
    """
    plt.figure(figsize=(12, 6))
    
    # Original image
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")
    
    # Noisy image
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(noisy, cv2.COLOR_BGR2RGB))
    plt.title("Noisy Image")
    plt.axis("off")
    
    # Filtered image
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    plt.title(f"Filtered Image ({filter_name})\nPSNR: {psnr_value:.2f}")
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()