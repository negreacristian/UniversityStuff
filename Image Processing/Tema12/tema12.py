import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

def canny_edge_detection(image, low_threshold, high_threshold):
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def lab12():
    img = cv2.imread("vacanta.jpg", cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Error: Image not found")
        return

    low_threshold = 50
    high_threshold = 150

    canny_edges = canny_edge_detection(img, low_threshold, high_threshold)

    img_resized = resize_image(img, 60)
    cv2.imshow("Imagine originala", img_resized)
    img_resized = resize_image(canny_edges, 60)
    cv2.imshow("Muchii detectate Canny", img_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

lab12()
