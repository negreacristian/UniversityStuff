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
    if color_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # apply thresholding to convert grayscale to binary image
    ret, thresh = cv2.threshold(gray, 70, 255, 0)

  

    num_labels, labels_im = cv2.connectedComponents(thresh)


    label_hue = np.uint8(179 * labels_im / np.max(labels_im))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue == 0] = 0

    cv2.imshow('Imagine procesată cu bfs', labeled_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

   
    # Implement BFS labeling algorithm

def labeling_equivalence_classes():
    if binary_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
 
    # componentele conexe
    num_labels, labeled_img, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)

    # culorile
    colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)

    color_labeled = np.zeros((labeled_img.shape[0], labeled_img.shape[1], 3), dtype=np.uint8)
    for y in range(labeled_img.shape[0]):
        for x in range(labeled_img.shape[1]):
            label = labeled_img[y, x]
            if label != 0:
                color_labeled[y, x] = colors[label]
    cv2.imshow('Imagine procesată cu doua treceri cu clase de echivalente', color_labeled)
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
