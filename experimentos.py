"""Experimentos de Neurito: mismo cerebro de main.py, sin ventana.

Ejecutar con: python experimentos.py
"""
import numpy as np

ACCIONES = ("COMER", "DORMIR", "JUGAR")


def relu(valores):
    return np.maximum(0, valores)


def softmax(valores):
    exp = np.exp(valores - np.max(valores, axis=1, keepdims=True))
    return exp / np.sum(exp, axis=1, keepdims=True)


def etiquetas(datos):
    # Gana la necesidad más alta; el cansancio es 1 - energía.
    return np.argmax(
        np.column_stack((datos[:, 0], 1 - datos[:, 1], datos[:, 2])), axis=1
    )


def entrenar(ocultas=6, epocas=1200, tasa=0.1):
    """Entrena la red y devuelve (pérdida, precisión de prueba, función predecir)."""
    np.random.seed(42)
    X = np.random.rand(3000, 3)
    y = etiquetas(X)
    W1 = np.random.randn(3, ocultas) * 0.5
    b1 = np.zeros((1, ocultas))
    W2 = np.random.randn(ocultas, 3) * 0.5
    b2 = np.zeros((1, 3))
    n = len(X)

    for _ in range(epocas):
        z1 = X @ W1 + b1
        oculta = relu(z1)
        prob = softmax(oculta @ W2 + b2)
        perdida = -np.mean(np.log(prob[np.arange(n), y] + 1e-10))
        d2 = prob.copy()
        d2[np.arange(n), y] -= 1
        d2 /= n
        d1 = (d2 @ W2.T) * (z1 > 0)
        W2 -= tasa * (oculta.T @ d2)
        b2 -= tasa * np.sum(d2, axis=0, keepdims=True)
        W1 -= tasa * (X.T @ d1)
        b1 -= tasa * np.sum(d1, axis=0, keepdims=True)

    def predecir(datos):
        return softmax(relu(datos @ W1 + b1) @ W2 + b2)

    prueba = np.random.rand(1000, 3)
    precision = np.mean(np.argmax(predecir(prueba), axis=1) == etiquetas(prueba))
    return perdida, precision, predecir


def mostrar(predecir, necesidades):
    p = predecir(np.array([necesidades]))[0]
    print(f"  {necesidades} -> {ACCIONES[int(np.argmax(p))]}  {np.round(p * 100, 1)}")


print("Experimento 1: cambia solo el hambre (energía 0.5, aburrimiento 0.3)")
_, _, predecir = entrenar()
for hambre in (0.1, 0.3, 0.5, 0.7, 0.9):
    mostrar(predecir, [hambre, 0.5, 0.3])

print("\nExperimento 2: prioridades casi iguales")
mostrar(predecir, [0.60, 0.40, 0.60])
mostrar(predecir, [0.61, 0.40, 0.60])

print("\nExperimento 3: neuronas ocultas")
for ocultas in (3, 6, 10, 20):
    perdida, precision, _ = entrenar(ocultas=ocultas)
    print(f"  {ocultas:>2} neuronas | pérdida {perdida:.3f} | precisión {precision:.1%}")

print("\nExperimento 4a: épocas")
for epocas in (100, 300, 1200, 5000):
    perdida, precision, _ = entrenar(epocas=epocas)
    print(f"  {epocas:>4} épocas | pérdida {perdida:.3f} | precisión {precision:.1%}")

print("\nExperimento 4b: tasa de aprendizaje")
for tasa in (0.001, 0.01, 0.1, 1, 5, 20):
    perdida, precision, _ = entrenar(tasa=tasa)
    print(f"  tasa {tasa:<6} | pérdida {perdida:.3f} | precisión {precision:.1%}")
