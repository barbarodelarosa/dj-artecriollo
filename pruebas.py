casa = 23.05993946283003,-82.35179762951299

yosdel = 23.060521883368295,-82.36439328298835
from math import acos, cos, sin, radians

def distancia_puntos(punto_1, punto_2):
    punto_1 = (radians(punto_1[0]), radians(punto_1[1]))
    punto_2 = (radians(punto_2[0]), radians(punto_2[1]))

    distancia = acos(sin(punto_1[0])*sin(punto_2[0]) + cos(punto_1[0])*cos(punto_2[0])*cos(punto_1[1] - punto_2[1]))
    return distancia * 6371.01

if __name__ == "__main__":
    punto_1 = (23.05993946283003,-82.35179762951299)
    punto_2 = (23.060521883368295,-82.36439328298835)

    resultado = distancia_puntos(punto_1,punto_2)
    print(f"La distancia es {resultado}")