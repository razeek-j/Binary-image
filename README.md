# Image Binarization using Global and Local Adaptive Thresholding

This repository provides a Python implementation and scientific analysis of two fundamental image binarization techniques: **Global Adaptive Thresholding** and **Local Adaptive Thresholding**. The code uses the `OpenCV` and `NumPy` libraries to process a grayscale image and generate binary (black and white) versions, demonstrating the strengths and weaknesses of each approach.

---

## 🔬 Introduction to Image Binarization

Image binarization is a critical preprocessing step in many computer vision and image processing pipelines. The goal is to convert a grayscale image into a binary image, where each pixel is assigned one of two values, typically 0 (black) for the background and 255 (white) for the foreground.

This simplification is essential for tasks such as:
* **Object Segmentation:** Isolating objects of interest from the background.
* **Feature Extraction:** Simplifying images to make it easier to extract features like edges, corners, and shapes.
* **Optical Character Recognition (OCR):** Converting scanned text into machine-readable characters. 

The core of binarization is **thresholding**, where a threshold value, $`\tau`$, is used to make the decision. For a given pixel with intensity $`I(x, y)`$:

$$
\text{Output}(x, y) =
\begin{cases}
255 & \text{if } I(x, y) > \tau \\
0 & \text{if } I(x, y) \leq \tau
\end{cases}
$$

The challenge lies in choosing an optimal threshold $`\tau`$. The methods in this project explore two distinct strategies for finding it.

---

## ⚙️ Algorithms Implemented

### 1. Global Adaptive Thresholding (Isodata Algorithm)

The first method implemented is a global technique that determines a single, optimal threshold for the entire image. The specific algorithm used here is an iterative approach known as the **Isodata algorithm**, or **iterative intermeans**. It is "adaptive" in the sense that it adapts to the image's pixel distribution, but "global" because it applies one threshold universally.

#### Conceptual Basis

The algorithm iteratively refines a threshold by separating pixels into two groups (potential background and foreground) and calculating a new threshold that is the average of the mean intensities of these two groups. This process repeats until the threshold value stabilizes.

#### Mathematical Steps

1.  **Initialization:** An initial threshold $`\tau`$ is chosen. A good starting point is the median or mean intensity of the entire image.
2.  **Segmentation:** The image pixels are partitioned into two groups:
    * $`G_0 = \{I(x, y) \mid I(x, y) \leq \tau\}`$ (background)
    * $`G_1 = \{I(x, y) \mid I(x, y) > \tau\}`$ (foreground)
3.  **Mean Calculation:** The mean intensity for each group is calculated:
    * $`\mu_0 = \text{mean}(G_0)`$
    * $`\mu_1 = \text{mean}(G_1)`$
4.  **Threshold Update:** A new threshold, $`\tau_{\text{new}}`$, is computed as the average of the two means:
   
$$
\tau_{\text{new}} = \frac{\mu_0 + \mu_1}{2}
$$

5.  **Convergence Check:** The algorithm checks if the threshold has converged by comparing the old and new values against a small tolerance, $`\epsilon`$:

$$
|\tau - \tau_{\text{new}}| \leq \epsilon
$$

If the condition is met, the loop terminates. Otherwise, set $`\tau = \tau_{\text{new}}`$ and repeat from Step 2.

This method is simple and computationally efficient but assumes a bimodal histogram (clear foreground and background peaks) and uniform illumination across the image.

### 2. Local Adaptive Thresholding (Mean Adaptive Method)

The second method is a local technique that overcomes the primary limitation of global thresholding. Instead of a single threshold for the entire image, **local adaptive thresholding** calculates a unique threshold for each pixel based on the characteristics of its surrounding neighborhood. This makes it highly effective for images with varying illumination conditions (e.g., shadows or gradients).

#### Conceptual Basis

The algorithm slides a window over each pixel of the image. For each pixel, the threshold is calculated as the mean intensity of the pixels within its local neighborhood window.

#### Process

1.  **Neighborhood Definition:** For each pixel $`I(x, y)`$ in the image, a local neighborhood window of size $`w_w \times h_w`$ is defined, centered at $`(x, y)`$.
2.  **Local Threshold Calculation:** The threshold for the pixel $`I(x, y)`$ is calculated as the mean of the pixel intensities within this window:
   
$$
\tau_{xy} = \frac{1}{w_w \times h_w} \sum_{i=-\lfloor w_w/2 \rfloor}^{\lfloor w_w/2 \rfloor} \sum_{j=-\lfloor h_w/2 \rfloor}^{\lfloor h_w/2 \rfloor} I(x+i, y+j)
$$
    
3.  **Binarization:** The pixel $`I(x, y)`$ is then binarized using its personal threshold $`\tau_{xy}`$.

#### The Critical Role of Window Size ($`w_w, h_w`$)

The choice of window size is crucial for the performance of this algorithm:
* **If the window is too small,** it may not capture enough local context, leading to a noisy result where small variations in texture are incorrectly binarized.
* **If the window is too large,** the algorithm loses its "local" nature and begins to approximate a global threshold. It will fail to adapt to local illumination changes within the window.

The optimal window size must be large enough to cover representative samples of both foreground and background pixels but small enough to preserve local details.

---

## 📊 Comparison: Global vs. Local Thresholding

| Feature                 | Global Adaptive Thresholding (Isodata)                                | Local Adaptive Thresholding (Mean)                                         |
| ----------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Threshold Scope** | One threshold for the entire image.                                   | A different threshold for each pixel.                                      |
| **Illumination** | **Fails** with non-uniform lighting, shadows, and gradients.          | **Excellent** for images with varying illumination.                        |
| **Computational Cost** | Low. It is very fast and efficient.                                   | High. Requires calculations for every pixel based on its neighborhood.     |
| **Parameters** | Requires a convergence threshold ($`\epsilon`$).                     | Requires a window size ($`w_w, h_w`$), which can be tricky to tune. |
| **Use Case** | Ideal for documents or images with a clear, uniform background. | Best for complex scenes, natural images, and scans with uneven brightness. |

---

## 🖼️ Results and Visual Analysis

The following images demonstrate the application of both algorithms on a sample image of a chair, which features both solid areas and regions with subtle shadows and texture.

### Original Image

![Original Image](./assets/A%20chair.jpg)

### Global Adaptive Thresholding Result

The global method struggles with the subtle lighting variations on the chair and the floor. While it captures the main silhouette, it loses detail in shadowed areas and introduces noise where the background intensity is close to the single global threshold.

*(Replace the placeholder URL with the actual path to your global result image)*
![Global Binary Result](https://i.imgur.com/kS6LzT7.jpeg)

### Local Adaptive Thresholding Result

The local method performs significantly better. By adapting to the brightness of each pixel's neighborhood, it successfully preserves the edges and details of the chair, even in areas with shadows. It clearly separates the chair from the background across the entire image, demonstrating its robustness to non-uniform illumination.

*(Replace the placeholder URL with the actual path to your local result image)*
![Local Binary Result](https://i.imgur.com/OqG0c7P.jpeg)

---

## 🚀 How to Use

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Install dependencies:**
    Ensure you have Python installed, along with the required packages.
    ```bash
    pip install opencv-python numpy
    ```

3.  **Run the script:**
    Open the `main.py` file and modify the image path in the `main()` function:
    ```python
    input_image = cv2.imread('/path/to/your/image.jpg', cv2.IMREAD_GRAYSCALE)
    ```
    Then, execute the script from your terminal:
    ```bash
    python main.py
    ```

4.  **Check the output:**
    The script will generate two output files in the same directory: `global_binary.jpg` and `local_binary.jpg`.

### Parameters

You can adjust the following parameters in the `main()` function:
* `epsilon`: The convergence threshold for the global method. A smaller value means a more precise threshold but may take longer to compute.
* `w_w`, `h_w`: The width and height of the neighborhood window for the local method. These must be odd numbers. Experiment with these values to see their effect on the output.
