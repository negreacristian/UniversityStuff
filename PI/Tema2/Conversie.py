import cv2
import os
import tkinter as tk
from tkinter import filedialog

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        if image is None:
            print("Nu s-a putut deschide sau găsi imaginea.")
            return
        show_images(image)

def show_images(image):
    fName = 'vacanta.jpg'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, 0)
    hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cv2.imshow('Original image', image)
    cv2.imshow('Gray.jpg', gray)
    cv2.imshow('Binary.jpg', thresh)
    cv2.imshow('HSV.jpg', hsvImg)

    cv2.imwrite(fName, image)
    cv2.imwrite('Gray.jpg', gray)
    cv2.imwrite('Binary.jpg', thresh)
    cv2.imwrite('HSV.jpg', hsvImg)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=open_image)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()
