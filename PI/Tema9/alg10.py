import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

# Încărcăm imaginea originală și o convertim la grayscale
image_path = 'vacanta.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Verificăm dacă imaginea a fost încărcată corect
if image is None:
    print("Imaginea nu a fost încărcată. Verifică calea.")
else:
    # Transformata Fourier a imaginii
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)

    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2

    # Creăm o mască cu valori 1 într-un cerc la centru pentru filtrul "trece jos"
    low_pass_mask = np.zeros((rows, cols), np.uint8)
    low_radius = 30  # Radiusul pentru filtrul trece jos
    cv2.circle(low_pass_mask, (ccol, crow), low_radius, 1, thickness=-1)

    # Creăm o mască cu valori 1 în afara unui cerc la centru pentru filtrul "trece sus"
    high_pass_mask = np.ones((rows, cols), np.uint8)
    high_radius = 15  # Radiusul pentru filtrul trece sus
    cv2.circle(high_pass_mask, (ccol, crow), high_radius, 0, thickness=-1)

    # Aplicăm mastile și calculăm Transformata Fourier Inversă
    fshift_low = fshift * low_pass_mask
    f_ishift_low = np.fft.ifftshift(fshift_low)
    image_low_pass = np.fft.ifft2(f_ishift_low)
    image_low_pass = np.abs(image_low_pass)

    fshift_high = fshift * high_pass_mask
    f_ishift_high = np.fft.ifftshift(fshift_high)
    image_high_pass = np.fft.ifft2(f_ishift_high)
    image_high_pass = np.abs(image_high_pass)

 
    # Create the main window
    root = tk.Tk()
    root.title('Frequency Domain Filtering')

       # Convertim imaginile pentru afișare în Tkinter
    original_image_for_tk = ImageTk.PhotoImage(image=Image.fromarray(image))
    low_pass_image_for_tk = ImageTk.PhotoImage(image=Image.fromarray(image_low_pass))
    high_pass_image_for_tk = ImageTk.PhotoImage(image=Image.fromarray(image_high_pass))

    # Create a frame for each image
    original_frame = tk.LabelFrame(root, text='Original Image')
    low_pass_frame = tk.LabelFrame(root, text='Low Pass Filter Image')
    high_pass_frame = tk.LabelFrame(root, text='High Pass Filter Image')

    # Pack the frames into the main window
    original_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    low_pass_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    high_pass_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Place the images in their respective frames
    tk.Label(original_frame, image=original_image_for_tk).pack()
    tk.Label(low_pass_frame, image=low_pass_image_for_tk).pack()
    tk.Label(high_pass_frame, image=high_pass_image_for_tk).pack()

    # Run the Tkinter event loop
    root.mainloop()
