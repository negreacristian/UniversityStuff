import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

# Încărcăm imaginea originală
image_path = 'vacanta.jpg'
image = cv2.imread(image_path)

# Define the process and display function
def process_and_display():
    if image is None:
        print("Imaginea nu a fost încărcată. Verifică calea.")
        return
    
    # Aplicăm un filtru "trece jos" (GaussianBlur pentru netezire)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Convertim imaginea pentru afișare în Tkinter
    blurred_image_for_tk = Image.fromarray(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB))
    
    # Aplicăm un filtru "trece sus" (Laplacian pentru evidențierea muchiilor)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_filter = cv2.Laplacian(gray_image, cv2.CV_64F)
    laplacian_image = cv2.convertScaleAbs(laplacian_filter)
    
    # Convertim imaginea pentru afișare în Tkinter
    laplacian_image_for_tk = Image.fromarray(laplacian_image)

    # Create the main window
    root = tk.Tk()
    root.title('Image Filters')

    # Create a frame for each image
    
    original_frame = tk.LabelFrame(root, text='Original Image')
    blurred_frame = tk.LabelFrame(root, text='Blurred Image (Trece Jos)')
    blurred_frame = tk.LabelFrame(root, text='Blurred Image (Trece Jos)')
    laplacian_frame = tk.LabelFrame(root, text='Laplacian Image (Trece Sus)')
    laplacian_frame = tk.LabelFrame(root, text='Laplacian Image (Trece Sus)')

    # Pack the frames into the main window
    original_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    blurred_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    laplacian_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH) 

    # Convert the images to a format that Tkinter can understand and display them
    original_image_for_tk = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
    tk.Label(original_frame, image=original_image_for_tk).pack()

    blurred_image_for_tk = ImageTk.PhotoImage(blurred_image_for_tk)
    tk.Label(blurred_frame, image=blurred_image_for_tk).pack()

    laplacian_image_for_tk = ImageTk.PhotoImage(laplacian_image_for_tk)
    tk.Label(laplacian_frame, image=laplacian_image_for_tk).pack()

    # Run the Tkinter event loop
    root.mainloop()

# Call the function to process the images and display them
process_and_display()
