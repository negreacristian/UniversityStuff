import cv2
import numpy as np

image_path = 'imagine.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Nu s-a putut incarca imaginea.")
    exit()

# Inversarea imaginii pentru a avea obiectele în negru
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image)

print("Numarul total de obiecte:", num_labels - 1)

output_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

for label in range(1, num_labels):
    #obtain the area of the object
    area = stats[label, cv2.CC_STAT_AREA]
    #obtain the centroid of the object
    centroid = centroids[label]
    #create mask to find the conturs
    mask = labels == label
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #calculates permieter based on the contur
    perimeter = cv2.arcLength(contours[0], True)
    #draw contur 
    cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)
    cv2.circle(output_image, (int(centroid[0]), int(centroid[1])), 5, (255, 0, 0), -1)

    print(f"Obiectul {label}: Aria = {area}, Centrul de masa = {centroid}, Perimetrul = {perimeter}")

cv2.imshow('Centre de masa si contururi', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
