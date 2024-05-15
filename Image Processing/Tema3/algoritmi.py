import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import filedialog

def open_image():
    global gray_image, color_image
    file_path = filedialog.askopenfilename()
    gray_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    color_image = cv2.imread(file_path)

def convert_to_grayscale():
    if color_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    global gray_image
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Imagine în tonuri de gri', gray_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def convert_to_binary():
    global binary_image
    if gray_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    ret, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('Imagine binară', binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def convert_to_hsv():
    if color_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
    cv2.imshow('Imagine în spațiul de culoare HSV', hsv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_gray_histogram():
    if gray_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    plt.figure()
    plt.title("Histograma imaginii în tonuri de gri")
    plt.xlabel("Valori intensitate")
    plt.ylabel("Număr pixeli")
    plt.plot(histogram)
    plt.xlim([0, 256])
    plt.show()

def apply_otsu_threshold():
    if gray_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print(f"Valoarea pragului determinată de Otsu: {ret}")
    cv2.imshow('Imagine segmentată', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def apply_floyd_steinberg():
    if gray_image is None:
        print("Nu a fost selectată nicio imagine.")
        return

    # Apply Floyd-Steinberg dithering
    dithered_image = gray_image.copy()
    height, width = dithered_image.shape
    for y in range(height - 1):
        for x in range(1, width - 1):
            old_pixel = dithered_image[y][x]
            new_pixel = 255 if old_pixel > 127 else 0
            dithered_image[y][x] = new_pixel
            quant_error = old_pixel - new_pixel
            dithered_image[y][x + 1] += quant_error * 7 / 16
            dithered_image[y + 1][x - 1] += quant_error * 3 / 16
            dithered_image[y + 1][x] += quant_error * 5 / 16
            dithered_image[y + 1][x + 1] += quant_error * 1 / 16

    cv2.imshow('Imagine procesată cu Floyd-Steinberg', dithered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def show_color_histogram():
    if color_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    colors = ('b', 'g', 'r')
    for i, color in enumerate(colors):
        histogram = cv2.calcHist([color_image], [i], None, [256], [0, 256])
        plt.plot(histogram, color=color)
        plt.xlim([0, 256])
    plt.title("Histograma imaginii color")
    plt.xlabel("Valori intensitate")
    plt.ylabel("Număr pixeli")
    plt.show()

def labeling_bfs():
    if binary_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    
    labeled_image = np.zeros_like(binary_image)
    label = 1
    rows, cols = binary_image.shape
    visited = np.zeros_like(binary_image) 
    for i in range(rows):
        for j in range(cols):
            if binary_image[i, j] == 0 and labeled_image[i, j] == 0:
                queue = [(i, j)]
                while queue:
                    x, y = queue.pop(0)
                    labeled_image[x, y] = label
                    
                    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                    for nx, ny in neighbors:
                        if 0 <= nx < rows and 0 <= ny < cols and binary_image[nx, ny] == 0 and labeled_image[nx, ny] == 0:
                            queue.append((nx, ny))
                label += 1
    cv2.imshow('Imagine procesată cu bfs', labeled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
    # Implement BFS labeling algorithm

def labeling_equivalence_classes():
    if binary_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    
    labeled_image = np.zeros_like(binary_image)
    label = 1
    equivalence = {}

    rows, cols = binary_image.shape

    for i in range(rows):
        for j in range(cols):
            if binary_image[i, j] == 0:
                neighbors = []
                if i > 0 and binary_image[i-1, j] == 0:
                    neighbors.append(labeled_image[i-1, j])
                if j > 0 and binary_image[i, j-1] == 0:
                    neighbors.append(labeled_image[i, j-1])

                if not neighbors:
                    labeled_image[i, j] = label
                    label += 1
                else:
                    neighbors = sorted(neighbors)
                    labeled_image[i, j] = neighbors[0]
                    for neighbor in neighbors[1:]:
                        if neighbor != neighbors[0]:
                            equivalence[neighbor] = neighbors[0]

    # A doua trecere
    for i in range(rows):
        for j in range(cols):
            if labeled_image[i, j] in equivalence:
                labeled_image[i, j] = equivalence[labeled_image[i, j]]
                
    cv2.imshow('Imagine procesată cu doua treceri cu clase de echivalente', labeled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   


# Setarea interfeței grafice Tkinter
root = Tk()
root.title("Procesare imagine")

root.geometry("300x400")
# Buton pentru deschiderea imaginii
open_button = Button(root, text="Deschide Imagine", command=open_image)
open_button.pack( fill="x", expand=True, padx=10, pady=3)

grayscale_button = Button(root, text="Conversie la Tonuri de Gri", command=convert_to_grayscale)
grayscale_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru conversia unei imagini în tonuri de gri în imagine binară
binary_button = Button(root, text="Conversie la Binare", command=convert_to_binary)
binary_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru conversia unei imagini din spațiul de culoare RGB în spațiul de culoare HSV
hsv_button = Button(root, text="Conversie la HSV", command=convert_to_hsv)
hsv_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru afișarea histogramei imaginii în tonuri de gri
histogram_button = Button(root, text="Afișează Histograma Gri", command=show_gray_histogram)
histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru aplicarea pragului Otsu
otsu_button = Button(root, text="Aplică Prag Otsu", command=apply_otsu_threshold)
otsu_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru aplicarea algoritmului Floyd-Steinberg
floyd_button = Button(root, text="Aplică Floyd-Steinberg", command=apply_floyd_steinberg)
floyd_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru afișarea histogramei imaginii color
color_histogram_button = Button(root, text="Afișează Histograma Color", command=show_color_histogram)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru aplicarea algoritmului Floyd-Steinberg
floyd_button = Button(root, text="Aplică Traversare in lățime", command=labeling_bfs)
floyd_button.pack( fill="x", expand=True,padx=10, pady=3)

# Buton pentru afișarea histogramei imaginii color
color_histogram_button = Button(root, text="Aplică două treceri cu clase de echivalențe", command=labeling_equivalence_classes)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)
root.mainloop()
