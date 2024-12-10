import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from scipy.ndimage import zoom

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
    elif filter_type == "Butterworth Filter":
        out = butterworth_filter(inp, cutoff=90, order=3, highpass=False)
    return out

def butterworth_filter(image, cutoff, order, highpass=False):
    if len(image.shape) == 3:
        b, g, r = cv2.split(image)
        
        # Áp dụng bộ lọc cho từng kênh màu
        r_filtered = butterworth_filter_single_channel(r, cutoff, order, highpass)
        g_filtered = butterworth_filter_single_channel(g, cutoff, order, highpass)
        b_filtered = butterworth_filter_single_channel(b, cutoff, order, highpass)
        
        # Hợp 3 kênh màu
        filtered_image = cv2.merge([b_filtered, g_filtered, r_filtered])
    else:
        # Áp dụng bộ lọc cho ảnh xám
        filtered_image = butterworth_filter_single_channel(image, cutoff, order, highpass)
    return filtered_image

def butterworth_filter_single_channel(image, cutoff, order, highpass=False):
    # Biến đổi fft
    dft = np.fft.fft2(image)
    dft_shift = np.fft.fftshift(dft) 
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2  
    x = np.arange(0, cols)
    y = np.arange(0, rows)
    x, y = np.meshgrid(x, y)
    d = np.sqrt((x - ccol)**2 + (y - crow)**2) 
    
    if highpass:
        # Highpass Butterworth filter
        butterworth_mask = 1 / (1 + (cutoff / d)**(2 * order))
    else:
        # Lowpass Butterworth filter
        butterworth_mask = 1 / (1 + (d / cutoff)**(2 * order))
    
    # Apply the filter
    filtered_dft = dft_shift * butterworth_mask
    
    # Inverse Fourier Transform
    filtered_dft_shift = np.fft.ifftshift(filtered_dft)
    filtered_image = np.fft.ifft2(filtered_dft_shift)
    filtered_image = np.abs(filtered_image)  # Get the real part

    # Normalize the result
    filtered_image = np.uint8(np.clip(filtered_image, 0, 255))
    
    return filtered_image

def add_noise(image_path, noise_type):
    inp = cv2.imread(image_path)
    
    if noise_type == "Salt and Pepper":
        out = add_salt_pepper_noise(inp, salt_prob=0.1,pepper_prob=0.13)
    elif noise_type == "Gaussian":
        out = add_gaussian_noise(inp, mean=0,std=40)
    elif noise_type == "Poisson":
        out = np.random.poisson(inp).astype(np.uint8)
    return out

def add_gaussian_noise(image, mean=0, std=25):
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 255).astype(np.uint8)

def add_salt_pepper_noise(image, salt_prob=0.09, pepper_prob=0.02):
    noisy_image = np.copy(image)
    total_pixels = image.size
    num_salt = int(salt_prob * total_pixels)
    num_pepper = int(pepper_prob * total_pixels)

    # Thêm nhiễu salt
    coords_salt = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[tuple(coords_salt)] = 255

    # Thêm nhiễu pepper
    coords_pepper = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[tuple(coords_pepper)] = 0

    return noisy_image

def psnr(original, filtered):
    if original.shape != filtered.shape:
        image_array = np.array(filtered)
        scale = original.shape[1]/filtered.shape[1]
        filtered_resized = zoom(image_array, (scale, scale, 1))
    else:
        filtered_resized = filtered

    mse = np.mean((original - filtered_resized) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse)), mse

def plot_images(original, noisy, filtered, filter_name, mse_value):
    plt.figure(figsize=(12, 6))
    
    # Ảnh gốc
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")
    plt.axis("off")
    
    # Ảnh nhiễu
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(noisy, cv2.COLOR_BGR2RGB))
    plt.title("Noisy Image")
    plt.axis("off")
    
    # Ảnh đã lọc
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    plt.title(f"Filtered Image ({filter_name})\nMSE: {mse_value:.2f}")
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()

