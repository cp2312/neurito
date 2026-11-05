"""Experimentos de Neurito 2.0 (salto), sin ventana de Pygame.

Ejecutar con: python -X utf8 experimentos_salto.py
"""
import numpy as np

from salto_juego import JuegoSalto
from salto_modelo import RedSalto

FOTOGRAMAS = 9000  # unos 5 minutos de juego a 30 fps


def jugar(red, fotogramas=FOTOGRAMAS):
    """Deja que la red juegue sola y cuenta esquivados y choques."""
    juego = JuegoSalto()
    for _ in range(fotogramas):
        if red.probabilidad(juego.distancia, juego.velocidad) >= 0.5 and juego.en_suelo:
            juego.saltar()
        juego.actualizar()
    return juego.esquivados, juego.choques


def entrenar(red, epocas):
    X, y = red.generar_datos(5000)
    for _ in range(epocas):
        red.entrenar_epoca(X, y)
    X_test, y_test = red.generar_datos(1500)
    return red.historial[-1], red.precision(X_test, y_test)


def resumen(nombre, red, epocas):
    perdida, precision = entrenar(red, epocas)
    esq, cho = jugar(red)
    print(f"  {nombre:<14} | pérdida {perdida:.3f} | precisión {precision:.1%} "
          f"| esquivados {esq:>3} | choques {cho:>3}")


print("Experimento 1: sin entrenar")
red = RedSalto()
esq, cho = jugar(red)
print(f"  esquivados {esq} | choques {cho}")

print("\nExperimento 2: entrenar de 100 en 100 épocas")
red = RedSalto()
X, y = red.generar_datos(5000)
X_test, y_test = red.generar_datos(1500)
for _ in range(10):
    for _ in range(100):
        red.entrenar_epoca(X, y)
    esq, cho = jugar(red)
    print(f"  {red.epocas:>4} épocas | pérdida {red.historial[-1]:.3f} "
          f"| precisión {red.precision(X_test, y_test):.1%} "
          f"| esquivados {esq:>3} | choques {cho:>3}")

print("\nExperimento 3: neuronas ocultas (1000 épocas)")
for ocultas in (3, 12, 24):
    resumen(f"{ocultas} neuronas", RedSalto(ocultas=ocultas), 1000)

print("\nExperimento 4: tasa de aprendizaje (1000 épocas)")
for tasa in (0.01, 0.8, 1.2):
    resumen(f"tasa {tasa}", RedSalto(tasa=tasa), 1000)


def red_con_ventana(minimo, maximo):
    """Red igual a la original, pero con otra ventana de etiquetas."""
    class RedVentana(RedSalto):
        @staticmethod
        def etiqueta(distancia, velocidad):
            ttc = np.asarray(distancia) / np.maximum(np.asarray(velocidad), 0.001)
            return ((ttc >= minimo) & (ttc <= maximo)).astype(float).reshape(-1, 1)

        def generar_datos(self, n=5000):
            v = self.rng.uniform(4.5, 8.5, n)
            n_pos = n // 2
            ttc = np.concatenate((
                self.rng.uniform(minimo + 0.5, maximo - 0.5, n_pos),
                self.rng.uniform(0, 60, n - n_pos),
            ))
            self.rng.shuffle(ttc)
            d = v * ttc
            return self.preparar_entradas(d, v), self.etiqueta(d, v)

    return RedVentana()


print("\nExperimento 5: ventana de etiquetas (1000 épocas)")
for minimo, maximo in ((7, 13), (2, 5), (15, 25), (30, 40)):
    resumen(f"{minimo} a {maximo}", red_con_ventana(minimo, maximo), 1000)
