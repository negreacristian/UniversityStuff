import cv2
import numpy as np

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

def urmareste_si_extrage_coduri(imagine):
    # Convertirea imaginii în imagine alb-negru și binarizarea acesteia
    imagine_grayscale = cv2.cvtColor(imagine, cv2.COLOR_BGR2GRAY)
    _, imagine_binarizata = cv2.threshold(imagine_grayscale, 127, 255, cv2.THRESH_BINARY)

    # Detectarea contururilor
    contururi, _ = cv2.findContours(imagine_binarizata, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # Crearea unei imagini noi, negre, pentru desenarea contururilor
    imagine_cu_contururi = np.zeros_like(imagine)
    
    # Desenarea contururilor pe imaginea nouă
    cv2.drawContours(imagine_cu_contururi, contururi, -1, (0, 255, 0), 2)
    
    # Calcularea și afișarea codurilor înlănțuite pentru fiecare contur
    for i, contur in enumerate(contururi):
        coduri = calculeaza_coduri_inlantuite(contur)
        print(f"Coduri înlănțuite pentru conturul {i+1}: {coduri}")

    return imagine_cu_contururi

# Citirea imaginii
imagine = cv2.imread('images.png')

# Procesarea imaginii și extragerea codurilor înlănțuite
imagine_cu_contururi = urmareste_si_extrage_coduri(imagine)

# Afișarea imaginii originale și a celei cu contururile desenate
cv2.imshow('Imagine Originala', imagine)
cv2.imshow('Contururi Desenate', imagine_cu_contururi)
cv2.waitKey(0)
cv2.destroyAllWindows()
