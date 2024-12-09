import cv2
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np


def histogram_equalization_color(input_path, output_path=None, display=True):
    """
    Apply histogram equalization to a color image and save/display the result.

    Parameters:
        input_path (str): Path to the input image.
        output_path (str, optional): Path to save the output image. Defaults to None.
        display (bool): Whether to display the input and output histograms. Defaults to True.

    Returns:
        PIL.Image: Equalized image in PIL format.
    """
    # Load the image in color (BGR format)
    img = cv2.imread(input_path)

    if img is None:
        print("Error: Unable to load image.")
        return None

    # Convert the image from BGR to YCrCb (apply equalization to luminance only)
    ycrcb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    # Equalize the Y (luminance) channel
    ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])

    # Convert back to BGR
    equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)

    # Save the result
    if output_path:
        cv2.imwrite(output_path, equalized_img)

    if display:
        # Display histograms
        plt.figure(figsize=(12, 12))

        # Original Image Histogram
        plt.subplot(2, 2, 1)
        plt.title("Original Histogram")
        plt.hist(img[:, :, 0].ravel(), bins=256, range=(0, 256), color="blue", alpha=0.6, label="Blue")
        plt.hist(img[:, :, 1].ravel(), bins=256, range=(0, 256), color="green", alpha=0.6, label="Green")
        plt.hist(img[:, :, 2].ravel(), bins=256, range=(0, 256), color="red", alpha=0.6, label="Red")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.legend()

        # Equalized Image Histogram
        plt.subplot(2, 2, 2)
        plt.title("Equalized Histogram")
        plt.hist(equalized_img[:, :, 0].ravel(), bins=256, range=(0, 256), color="blue", alpha=0.6, label="Blue")
        plt.hist(equalized_img[:, :, 1].ravel(), bins=256, range=(0, 256), color="green", alpha=0.6, label="Green")
        plt.hist(equalized_img[:, :, 2].ravel(), bins=256, range=(0, 256), color="red", alpha=0.6, label="Red")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.legend()

        plt.tight_layout()
        plt.show()

    return Image.fromarray(cv2.cvtColor(equalized_img, cv2.COLOR_BGR2RGB))