import cv2


# Citirea unei imagini din fișier
image = cv2.imread("D:\Facultate\F3S2\PI\img.jpg")  # Înlocuiește "img.jpg" cu numele fișierului tău de imagine

if image is None:
    print("Nu s-a putut deschide sau găsi imaginea.")
    exit()

# Afișarea imaginii
cv2.namedWindow("Imagine", cv2.WINDOW_NORMAL)  # Crearea unei ferestre cu numele "Imagine"
cv2.imshow("Imagine", image)  # Afișarea imaginii în fereastra creată

# Salvarea imaginii pe disc
cv2.imwrite("imagine.jpg", image)  # Salvează imaginea cu numele "img.jpg" în același director cu scriptul

cv2.waitKey(0)  # Așteaptă ca utilizatorul să apese o tastă

cv2.destroyAllWindows()  # Închide toate ferestrele deschise