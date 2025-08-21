import cv2
import numpy as np

def global_adaptive_thresholding(image, epsilon):
    """
    Perform global adaptive thresholding as per Section 2.7.1.
    Parameters:
        image: Grayscale input image
        epsilon: Convergence threshold
    Returns:
        Binarized image
    """
    # Initial threshold: median of pixel intensities
    tau = np.median(image)
    
    while True:
        # Divide pixels into two groups
        group_low = image[image <= tau]
        group_high = image[image > tau]
        
        # Calculate means of each group
        mu0 = np.mean(group_low) if group_low.size > 0 else 0
        mu1 = np.mean(group_high) if group_high.size > 0 else 0
        
        # New threshold
        tau_new = (mu0 + mu1) / 2
        
        # Check convergence
        if abs(tau - tau_new) <= epsilon:
            break
        tau = tau_new
    
    # Binarize the image
    binary_image = np.where(image > tau_new, 255, 0).astype(np.uint8)
    return binary_image

def local_adaptive_thresholding(image, w_w, h_w):
    """
    Perform local adaptive thresholding as per Section 2.7.2.
    Parameters:
        image: Grayscale input image
        w_w: Width of the local neighborhood
        h_w: Height of the local neighborhood
    Returns:
        Binarized image
    """
    h, w = image.shape
    binary_image = np.zeros_like(image, dtype=np.uint8)
    
    # Ensure odd dimensions for neighborhood
    w_w = w_w if w_w % 2 == 1 else w_w + 1
    h_w = h_w if h_w % 2 == 1 else h_w + 1
    
    # Pad image to handle boundaries
    pad_w = w_w // 2
    pad_h = h_w // 2
    padded_image = cv2.copyMakeBorder(image, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_REPLICATE)
    
    # Process each pixel
    for y in range(h):
        for x in range(w):
            # Define neighborhood bounds with padding offset
            x_start = x + pad_w
            x_end = x_start + w_w
            y_start = y + pad_h
            y_end = y_start + h_w
            
            # Extract neighborhood
            neighborhood = padded_image[y_start:y_end, x_start:x_end]
            tau_xy = np.mean(neighborhood)
            
            # Binarize pixel
            binary_image[y, x] = 255 if image[y, x] > tau_xy else 0
    
    return binary_image

def main():
    # Load image
    input_image = cv2.imread('/Users/razeek_j/Documents/SRH Docs/Semester 1/Block 3/Image Processing/Task 1/A chair.jpg', cv2.IMREAD_GRAYSCALE)
    if input_image is None:
        print("Error: Could not load image.")
        return
    
    # Parameters
    epsilon = 1.0  # Convergence threshold for global method
    w_w, h_w = 51, 51  # Neighborhood size for local method
    
    # Apply global adaptive thresholding
    global_binary = global_adaptive_thresholding(input_image, epsilon)
    cv2.imwrite('global_binary.jpg', global_binary)
    
    # Apply local adaptive thresholding
    local_binary = local_adaptive_thresholding(input_image, w_w, h_w)
    cv2.imwrite('local_binary.jpg', local_binary)
    
    print("Binarization complete. Check 'global_binary.jpg' and 'local_binary.jpg'.")

if __name__ == "__main__":
    main()