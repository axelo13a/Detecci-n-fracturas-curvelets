import numpy as np
import matplotlib.pyplot as plt
from curvelets.numpy import SimpleUDCT

def curvelet_transform(img, level):
    """
    Aplica la transformada curvelet

    Inputs:
        img: imagen 2D (numpy array, float32)
        level: número de niveles de la transformada

    Outputs:
        coeffs: lista de listas con coeficientes curvelets de la forma coeffs[idir][irec][iang][row][col]
    """

    C = SimpleUDCT(shape=img.shape, nscales = level)
    coeffs = C.forward(img)

    return coeffs, C

def inverse_curvelet_Transform(coeffs, C):
    """
    Aplica la transformada curvelet

    Inputs:
        coeffs: lista de listas con coeficientes curvelets de la forma coeffs[idir][irec][iang][row][col]
        C: objeto SimpleUDCT de la transformada

    Outputs:
        img_rec: Imagen 2D reconstruida
    """
    img_rec = C.backward(coeffs)

    return img_rec
    
def threshold_coeffs(coeffs, t_min, t_max, mode='soft'):
    """
    Aplica un doble umbral (por debajo y por encima) a los coeficientes curvelets

    Inputs:
        coeffs: lista de listas de coeficientes wavelet por ángulo
        t_min: umbral inferior (valores < t_min se eliminan)
        t_max: umbral superior (valores > t_max se eliminan)
        mode: 'hard' o 'soft'

    Returns:
        coeffs_t: Lista de coeficientes umbralizados (igual estructura que entrada)
    """
    import copy

    coeffs_t = copy.deepcopy(coeffs)

    for ires in range(len(coeffs)):
        for idir in range(len(coeffs[ires])):
            for iang in range(len(coeffs[ires][idir])):
                for x in range(len(coeffs[ires][idir][iang])):
                    for y in range(len(coeffs[ires][idir][iang][x])):
                        z = coeffs[ires][idir][iang][x][y]
                        mag = abs(z)

                        if mode == 'hard':
                            coeffs_t[ires][idir][iang][x][y] = z if mag >= t_min and mag < t_max else 0.0
                        elif mode == 'soft':
                            if mag >= t_min:
                                factor = (mag - t_min) / mag
                                coeffs_t[ires][idir][iang][x][y] = z * factor
                            else:
                                coeffs_t[ires][idir][iang][x][y] = 0.0
                        else:
                            raise ValueError("El modo debe ser 'soft' o 'hard'.")

    return coeffs_t

def threshold_value(coeffs, percentil):
    """
    Calcula en base a percentiles un valor dentro de entre el módulo de 
    todos los coeficientes de curvelets. Se usara para definir un threshold

    Inputs:
        coeffs: lista de listas de coeficientes wavelet por ángulo
        percenctil: Numero que indica posicion (puede ser float)

    Returns:
        threshold: valor del coeficiente en el perfil pedido
    """
    values = list()

    for ires in range(len(coeffs)):
        for idir in range(len(coeffs[ires])):
            for iang in range(len(coeffs[ires][idir])):
                for x in range(len(coeffs[ires][idir][iang])):
                    for y in range(len(coeffs[ires][idir][iang][x])):
                        z = coeffs[ires][idir][iang][x][y]
                        mag = abs(z)
                        values.append(mag)

    values_ordenados = np.sort(values)
    #Se obtiene el decil 80
    threshold = np.percentile(values_ordenados, percentil) 

    return threshold
                        
