import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

# Funcția pentru aplicarea filtrului Gaussian
def gaussian_blur(image, kernel_size):
    start_time = time.time()
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    end_time = time.time()
    return blurred_image, end_time - start_time

# Funcția pentru aplicarea unui filtru generic bidimensional (convoluție)
def convolve_2d(image, kernel):
    start_time = time.time()
    convolved_image = cv2.filter2D(image, -1, kernel)
    end_time = time.time()
    return convolved_image, end_time - start_time

image_path = 'vacanta.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Imaginea nu a fost încărcată. Verifică calea.")
else:
    # Definim nucleul Gaussian
    gaussian_kernel_size = 5  # De exemplu, un nucleu de 5x5
    gaussian_blurred, gaussian_time = gaussian_blur(image, gaussian_kernel_size)

    # Definim un nucleu bidimensional (de exemplu, un box blur)
    box_kernel_size = 5
    box_kernel = np.ones((box_kernel_size, box_kernel_size), np.float32) / (box_kernel_size ** 2)
    box_blurred, box_time = convolve_2d(image, box_kernel)

    print(f"Timpul de procesare pentru Gaussian Blur: {gaussian_time} secunde")
    print(f"Timpul de procesare pentru Box Blur: {box_time} secunde")

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(gaussian_blurred, cmap='gray')
    plt.title('Gaussian Blurred')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(box_blurred, cmap='gray')
    plt.title('Box Blurred')
    plt.axis('off')

    plt.show()