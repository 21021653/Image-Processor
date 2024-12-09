import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

def histogram_equalization_color(input_path, output_path=None, display=True):
    """
    Apply histogram equalization to a color image and save/display the result.
    
    Parameters:
        input_path (str): Path to the input image.
        output_path (str, optional): Path to save the output image. Defaults to None.
        display (bool): Whether to display the input and output images. Defaults to True.
    """
    # Load the image in color (BGR format)
    img = cv2.imread(input_path)
    
    if img is None:
        print("Error: Unable to load image.")
        return
    
    # Convert the image from BGR to YCrCb (to apply equalization to intensity only)
    ycrcb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    
    # Equalize the Y (luminance) channel only
    ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])
    
    # Convert back to BGR
    equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)

    # Save the result
    if output_path:
        cv2.imwrite(output_path, equalized_img)

    # Display the original and equalized images side by side
    if display:
        # Convert to PIL for display
        original_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct colors
        equalized_pil = Image.fromarray(cv2.cvtColor(equalized_img, cv2.COLOR_BGR2RGB))

        # Show images using PIL
        original_pil.show(title="Original Image")
        equalized_pil.show(title="Equalized Image")

        # Display histograms
        plt.figure(figsize=(12, 12))
        
        # Original Image Histogram
        plt.subplot(2, 2, 1)
        plt.hist(img[:, :, 0].ravel(), bins=256, range=(0, 256), color='blue', alpha=0.6, label='Blue')
        plt.hist(img[:, :, 1].ravel(), bins=256, range=(0, 256), color='green', alpha=0.6, label='Green')
        plt.hist(img[:, :, 2].ravel(), bins=256, range=(0, 256), color='red', alpha=0.6, label='Red')
        plt.title('Original Image Histogram')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.legend()

        # Equalized Image Histogram
        plt.subplot(2, 2, 2)
        plt.hist(equalized_img[:, :, 0].ravel(), bins=256, range=(0, 256), color='blue', alpha=0.6, label='Blue')
        plt.hist(equalized_img[:, :, 1].ravel(), bins=256, range=(0, 256), color='green', alpha=0.6, label='Green')
        plt.hist(equalized_img[:, :, 2].ravel(), bins=256, range=(0, 256), color='red', alpha=0.6, label='Red')
        plt.title('Equalized Image Histogram')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.legend()

        plt.tight_layout()
        plt.show()

# Example usage
input_image = "C:/Users/vvu04/Downloads/iris.jpg"  # Replace with the path to your input image
output_image = "equalized_image.jpg"  # Optional: Replace with your desired output path

# Apply histogram equalization
histogram_equalization_color(input_image, output_image)
