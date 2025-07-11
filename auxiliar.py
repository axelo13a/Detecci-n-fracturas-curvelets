import json
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

def read_json():
    """
    Lee JSON de FracAtlas"

    Outputs:
        data: base de datos de FracAtlas

    """
    path = os.path.join('FracAtlas', 'Annotations', 'COCO JSON', 'COCO_fracture_masks.json')
    with open(path) as f:
        data = json.load(f)

    return data

def obtain_data(filename, data):
    """
    Busca imagen especifica en base de datos de FracAtlas 
    y obtiene su archivo de imagen, mascara, box(mascara rectangular) y
    un recorte de la imagen en la cercanía de box

    Inputs:
        filename: nombre del archivo de imagen(string)
        data: base de datos FracAtlas leída con read_json

    Output:
        info: Diccionario que contiene el archivo de imagen, 
        mascara, box(mascara rectangular) y un recorte de 
        la imagen en la cercanía de box
    
    """

    #Buscar la imagen en el JSON
    path_image = os.path.join("FracAtlas","images","Fractured",filename)
    img = plt.imread(path_image)

    # Buscar el diccionario con ese nombre
    id, width, height = next((img['id'], img['width'], img['height']) for img in data["images"] if img['file_name'] == filename)

    #Crear mascara y Box
    mask = np.zeros((height, width), dtype=np.uint8)
    box = np.zeros((height, width), dtype=np.uint8)

    seg, bbox = next((img['segmentation'],img["bbox"]) for img in data["annotations"] if img['id'] == id)
    pts = np.array(seg, dtype=np.int32).reshape((-1, 2))
    cv2.fillPoly(mask, [pts], color=1)

    x, y, w, h = map(int, bbox)
    box[y:y+h, x:x+w] = 1

    #Imagen solo en box
    img_cut = img[y-10:y+h+10, x-10:x+w+10]

    info = {}
    info["img"] = img
    info["mask"] = mask
    info["box"] = box
    info["img_cut"] = img_cut

    return info


def img_cuadrada(img_info):
    """
    Transforma la imagen original a una cuadrada. Esto se hace
    para realizar transformada curvelet y ridgelet

    Inputs:
        img_info: Diccionario obtenido de obtain data
    Outputs
        info: Diccionario con igual estructura que img_info, 
        que contiene imagenes, mascara y box cuadrada
    """

    img = img_info["img"]
    mask = img_info["mask"]
    box = img_info["box"]

    img = img[:,:,0]
 
    #Se asigna tamaño cuadrado
    img = img[0:352,0:352]
    mask = mask[0:352,0:352]
    box = box[0:352,0:352]
    
    #Se retorna con igual estructura
    info = {}
    info["img"] = img
    info["mask"] = mask
    info["box"] = box

    return info

def threshold(img, percentil):
    """
    Aplica un threshold de mediana, idea es crear mascara
    en imagen reconstruida

    Inputs:
        img: imagen 2D
    Outputs:
        thresholded_img: mascara de imagen img
    """
    # Calculamos la mediana de la imagen
    value = np.percentile(img, percentil)
    
    # Aplicamos el umbral
    thresholded_img = (img > value).astype(int)
    
    return thresholded_img

def iou(mask1, mask2):
    """
    Compara dos máscaras binarias usando número de píxeles detectados e IoU (Intersection over Union).
    
    Inputs:
    - mask1: Primer máscara binaria (numpy array de 0s y 1s).
    - mask2: Segunda máscara binaria (numpy array de 0s y 1s). Esta debe ser la original
    
    Outputs:
    - num_pixels_mask1: Número de píxeles en la primera máscara.
    - num_pixels_mask2: Número de píxeles en la segunda máscara.
    - iou: Intersection over Union entre las dos máscaras.
    """
    # Calcular el número de píxeles detectados en cada máscara (conteo de valores 1)
    num_pixels_mask1 = np.sum(mask1)
    num_pixels_mask2 = np.sum(mask2)
    
    # Calcular la intersección (pixeles comunes en ambas máscaras)
    intersection = np.sum((mask1 == 1) & (mask2 == 1))
    
    # Calcular la unión (pixeles en al menos una de las dos máscaras)
    union = np.sum((mask1 == 1) | (mask2 == 1))
    
    # Calcular el IoU (Intersection over Union)
    iou = intersection / union

    # Falsos negativos: Píxeles en mask2 que son 1 pero no están en mask1 (deberían haber sido detectados)
    false_negatives = np.sum((mask2 == 1) & (mask1 == 0))
    
    # Falsos positivos: Píxeles en mask1 que son 1 pero no están en mask2 (falsos positivos)
    false_positives = np.sum((mask1 == 1) & (mask2 == 0))
    
    return iou, false_negatives, false_positives