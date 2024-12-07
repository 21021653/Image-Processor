import cv2

def apply_filter(image_path, filter_type, kernel_size):
    """Apply the selected filter to the image."""
    inp = cv2.imread(image_path)
    
    if filter_type == "Median Filter":
        out = cv2.medianBlur(inp, kernel_size)
    elif filter_type == "Gaussian Filter":
        out = cv2.GaussianBlur(inp, (kernel_size, kernel_size), 0)
    elif filter_type == "Box Filter":
        out = cv2.blur(inp, (kernel_size, kernel_size))
    elif filter_type == "NL Means":
        out = cv2.fastNlMeansDenoisingColored(inp, None, kernel_size, kernel_size, 7, 21)
    
    return out