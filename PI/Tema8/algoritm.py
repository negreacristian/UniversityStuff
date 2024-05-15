import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import filedialog
from scipy.ndimage import gaussian_filter
from scipy import ndimage


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

    global color_labeled 
    color_labeled = np.zeros((labeled_img.shape[0], labeled_img.shape[1], 3), dtype=np.uint8)
    for y in range(labeled_img.shape[0]):
        for x in range(labeled_img.shape[1]):
            label = labeled_img[y, x]
            if label != 0:
                color_labeled[y, x] = colors[label]
    cv2.imshow('Imagine procesată cu doua treceri cu clase de echivalente', color_labeled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   
def calculate_features():
    # Un dicționar pentru a stoca trăsăturile fiecărui obiect etichetat
    features = {}
    rows, cols = color_labeled.shape
    
    for label in np.unique(color_labeled):
        if label == 0:  # Ignorăm fundalul
            continue
        # Selectăm obiectul curent
        object_mask = color_labeled == label
        
        # Aria: Numărul total de pixeli în obiect
        area = np.sum(object_mask)
        
        # Perimetrul: Numărul de pixeli de la marginea obiectului
        # Considerăm un pixel ca fiind pe margine dacă este în obiect dar are un vecin care nu este
        perimeter = 0
        for i in range(rows):
            for j in range(cols):
                if object_mask[i, j]:
                    # Verificăm vecinii
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = i + di, j + dj
                        if ni < 0 or nj < 0 or ni >= rows or nj >= cols or not object_mask[ni, nj]:
                            perimeter += 1
                            break
        
        # Centrul de masă (centroidul)
        coordinates = np.argwhere(object_mask)
        centroid = coordinates.mean(axis=0)
        
        # Salvăm trăsăturile pentru obiectul curent
        features[color_labeled] = {'Area': area, 'Perimeter': perimeter, 'Centroid': centroid}
    
        print(features)
        
def calculeaza_coduri_inlantuite(contur):
   
    """
    Calculează codurile înlănțuite pentru un contur dat.
    Codurile înlănțuite reprezintă direcțiile relative între punctele consecutive ale conturului.
    """
    coduri = []
    directii = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    for i in range(1, len(contur)):
        punct_curent = contur[i][0]
        punct_anterior = contur[i-1][0]
        delta = (punct_curent[0] - punct_anterior[0], punct_curent[1] - punct_anterior[1])
        cod = directii.index(delta)
        coduri.append(cod)
    return coduri

def urmareste_si_extrage_coduri():
    if color_image is None:
        print("Nu a fost selectată nicio imagine.")
        return
    # Convertirea imaginii în imagine alb-negru și binarizarea acesteia
    imagine_grayscale = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    _, imagine_binarizata = cv2.threshold(imagine_grayscale, 127, 255, cv2.THRESH_BINARY)

    # Detectarea contururilor
    contururi, _ = cv2.findContours(imagine_binarizata, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # Crearea unei imagini noi, negre, pentru desenarea contururilor
    imagine_cu_contururi = np.zeros_like(color_image)
    
    # Desenarea contururilor pe imaginea nouă
    cv2.drawContours(imagine_cu_contururi, contururi, -1, (0, 255, 0), 2)
    
    # Calcularea și afișarea codurilor înlănțuite pentru fiecare contur
    for i, contur in enumerate(contururi):
        coduri = calculeaza_coduri_inlantuite(contur)
        print(f"Coduri înlănțuite pentru conturul {i+1}: {coduri}")
        
    cv2.imshow('Imagine Originala', color_image)
    cv2.imshow('Contururi Desenate', imagine_cu_contururi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def extragere_contur():
    # Convertirea imaginii în imagine alb-negru
    imagine_grayscale = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    
    # Eroziunea imaginii pentru a elimina detalii fine
    imagine_erodata = cv2.erode(imagine_grayscale, np.ones((3,3), np.uint8), iterations=1)
    
    # Dilatarea imaginii pentru a recupera conturul
    imagine_dilatata = cv2.dilate(imagine_erodata, np.ones((3,3), np.uint8), iterations=1)
    
    # Negarea imaginii pentru a obține conturul
    contur = cv2.subtract(imagine_dilatata, imagine_erodata)
    

    # Afișarea imaginilor rezultate
    cv2.imshow('Contur', contur)
   
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def umplere_regiuni():
    # Convertirea imaginii în imagine alb-negru
    imagine_grayscale = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    
    # Inversarea culorilor pentru a transforma fundalul în negru și obiectele în alb
    imagine_inversata = cv2.bitwise_not(imagine_grayscale)
    
    # Inițializarea imaginii pentru umplere
    imagine_umplere = np.zeros((color_image.shape[0] + 2, color_image.shape[1] + 2), dtype=np.uint8)
    
    # Identificarea punctului de pornire pentru umplere
    x_start, y_start = 0, 0
    
    # Umplerea regiunii
    cv2.floodFill(imagine_inversata, imagine_umplere, (x_start, y_start), 255)
    
    # Inversarea imaginii înapoi pentru a reveni la culorile originale
    imagine_umplere = cv2.bitwise_not(imagine_inversata)
    
    cv2.imshow('Umplere regiuni', imagine_umplere)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def binarizare_automata():
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    _, binimg=cv2.threshold(gray_image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('Binarizare automata', binimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def negare_imagine():
    NEG=255-color_image
    cv2.imshow('Negare imagine', NEG)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def modificare_contrast():
    newimg=cv2.convertScaleAbs(color_image,alpha=1.5)
    cv2.imshow('Modificare contrast', newimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def gamma_correction():
   # Correct the gamma value and create a lookup table
    inv_gamma = 1.0 / 2
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype('uint8')

    # Apply the lookup table to the image
    if len(color_image.shape) == 2 or color_image.shape[2] == 1:  # Grayscale image or single channel
        corrected_img = cv2.LUT(color_image, table)
    else:  # Color image, apply the table to each channel
        channels = cv2.split(color_image)
        corrected_channels = [cv2.LUT(c, table) for c in channels]
        corrected_img = cv2.merge(corrected_channels)

    cv2.imshow('Corectia Gama', corrected_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def modificare_luminozitate():
    new_img=cv2.convertScaleAbs(color_image, beta=50)
    cv2.imshow('Modificare luminozitate', new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def egalizare_histograma():
    newimg=cv2.cvtColor(color_image.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    newimg=cv2.equalizeHist(newimg)
    cv2.imshow('Egalizare Histograma', newimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def low_pass_filter():
    # Load sample image
    
    # Apply Gaussian blur, with a sigma that defines the amount of blur
    filtered_image = gaussian_filter(color_image, sigma=2)
    # Display original and filtered image
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(color_image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(filtered_image, cmap='gray')
    plt.title('Low Pass Filtered Image')
    plt.axis('off')
    plt.show()
    

# Function to perform high pass filtering (edge detection)
def high_pass_filter():
    # Load sample image

    # Define a high-pass filter (edge detection filter)
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    # Apply the high-pass filter
    filtered_image = ndimage.convolve(color_image, kernel)
    # Display original and filtered image
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(color_image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(filtered_image, cmap='gray')
    plt.title('High Pass Filtered Image')
    plt.axis('off')
    plt.show()
            
# Setarea interfeței grafice Tkinter
root = Tk()
root.title("Procesare imagine")

root.geometry("300x400")
# Buton pentru deschiderea imaginii
open_button = Button(root, text="Deschide Imagine", command=open_image)
open_button.pack( fill="x", expand=True, padx=10, pady=3)

# Extrager coduri inlantuite
color_histogram_button = Button(root, text="Imagine in binar ", command=convert_to_binary)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Extrager coduri inlantuite
color_histogram_button = Button(root, text="Urmarire contur, extragere coduri ", command=urmareste_si_extrage_coduri)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Extrage Contur
color_histogram_button = Button(root, text="Algoritmul de extragere a conturului", command=extragere_contur)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Umplere Regiuni
color_histogram_button = Button(root, text="Umplere regiuni ", command=umplere_regiuni)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Binarizare automata
color_histogram_button = Button(root, text="Binarizare automata ", command=binarizare_automata)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Imagine negata
color_histogram_button = Button(root, text="Imagine negata", command=negare_imagine)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Modifica contrast
color_histogram_button = Button(root, text="Contrast modificat ", command=modificare_contrast)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Gamma correction
color_histogram_button = Button(root, text="Corectia Gama ", command=gamma_correction)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Modifica luminozitatea
color_histogram_button = Button(root, text="Modifica luminozitatea", command=modificare_luminozitate)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)

# Egalizarea histograma
color_histogram_button = Button(root, text="egalizare histograma", command=egalizare_histograma)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)
root.mainloop()

#Low Pass
color_histogram_button = Button(root, text="Low Pass Filteer", command=low_pass_filter)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)
root.mainloop()

# High Pass
color_histogram_button = Button(root, text="Low Pass Filter", command=high_pass_filter)
color_histogram_button.pack( fill="x", expand=True,padx=10, pady=3)
root.mainloop()
