"""Experimentos de Neurito 3.0 (laberinto), sin ventana de Pygame.

Ejecutar con: python -X utf8 experimentos_laberinto.py
"""
import heapq
from types import SimpleNamespace

import numpy as np

from laberinto_mundo import (
    DIRECCIONES, MAPAS, accion_experta, distancias_bfs, elegir_accion, libres,
    valido, vecino,
)
from laberinto_red import RedLaberinto, codificar

INTENTOS_MAX = 45  # igual que en laberinto.py


# ---------- Expertos que ponen las etiquetas ----------

def etiqueta_bfs(mapa, origen, meta, dist):
    return accion_experta(mapa, origen, dist)


def primer_paso(padres, origen, meta):
    actual = meta
    while padres[actual] != origen:
        actual = padres[actual]
    return DIRECCIONES.index((actual[0] - origen[0], actual[1] - origen[1]))


def etiqueta_dfs(mapa, origen, meta, dist):
    """Primer paso de un camino cualquiera que encuentra DFS (no el más corto)."""
    padres = {origen: None}
    pila = [origen]
    while pila:
        actual = pila.pop()
        if actual == meta:
            return primer_paso(padres, origen, meta)
        for a in reversed(range(4)):
            sig = vecino(actual, a)
            if valido(mapa, sig) and sig not in padres:
                padres[sig] = actual
                pila.append(sig)


def etiqueta_astar(mapa, origen, meta, dist):
    """Primer paso del camino que encuentra A* con distancia Manhattan."""
    def h(p):
        return abs(p[0] - meta[0]) + abs(p[1] - meta[1])
    padres = {origen: None}
    costo = {origen: 0}
    cola = [(h(origen), 0, origen)]
    while cola:
        _, g, actual = heapq.heappop(cola)
        if actual == meta:
            return primer_paso(padres, origen, meta)
        for a in range(4):
            sig = vecino(actual, a)
            if valido(mapa, sig) and g + 1 < costo.get(sig, 10**9):
                costo[sig] = g + 1
                padres[sig] = actual
                heapq.heappush(cola, (g + 1 + h(sig), g + 1, sig))


# ---------- Datos ----------

def generar(experto=etiqueta_bfs, semilla=42):
    """Mismos pares y misma división 80/20 que laberinto_red.generar_datos."""
    muestras = []
    for indice, mapa in enumerate(MAPAS):
        celdas = libres(mapa)
        for meta in celdas:
            dist = distancias_bfs(mapa, meta)
            for pos in celdas:
                if pos == meta or pos not in dist:
                    continue
                muestras.append((indice, pos, meta, experto(mapa, pos, meta, dist)))
    rng = np.random.default_rng(semilla)
    rng.shuffle(muestras)
    corte = int(len(muestras) * 0.8)

    def arrays(filas):
        X = np.stack([codificar(i, p, m) for i, p, m, _ in filas])
        y = np.asarray([a for *_, a in filas], dtype=np.int64)
        return X, y

    return arrays(muestras[:corte]), arrays(muestras[corte:]), muestras[corte:]


# ---------- Evaluación jugando ----------

def completar(red, filas, asistido):
    """Porcentaje de retos de prueba resueltos y pasos extra sobre el camino más corto."""
    exitos, extra = 0, []
    for indice, pos, meta, _ in filas:
        mapa = MAPAS[indice]
        mundo = SimpleNamespace(indice=indice, mapa=mapa, meta=meta, posicion=pos)
        visitas = {pos: 1}
        minimo = distancias_bfs(mapa, meta)[pos]
        for intento in range(1, INTENTOS_MAX + 1):
            mundo.posicion_actual = mundo.posicion
            accion, _ = elegir_accion(red, mundo, visitas, asistido)
            nuevo = vecino(mundo.posicion, accion)
            if valido(mapa, nuevo):
                mundo.posicion = nuevo
                visitas[nuevo] = visitas.get(nuevo, 0) + 1
                if nuevo == meta:
                    exitos += 1
                    extra.append(intento - minimo)
                    break
    return exitos / len(filas), (np.mean(extra) if extra else float("nan"))


def entrenar(epocas, datos, **kwargs):
    (X, y), (Xt, yt), prueba = datos
    red = RedLaberinto(**kwargs)
    for _ in range(epocas):
        red.entrenar_epoca(X, y)
    return red, Xt, yt, prueba


def linea(nombre, red, Xt, yt, prueba):
    perdida = f"{red.historial[-1]:.3f}" if red.historial else "  -  "
    pura, _ = completar(red, prueba, asistido=False)
    asist, _ = completar(red, prueba, asistido=True)
    print(f"  {nombre:<16} | pérdida {perdida} | exactitud {red.exactitud(Xt, yt):.1%} "
          f"| completa pura {pura:.0%} | asistida {asist:.0%}")


datos = generar()
_, _, prueba = datos
print(f"Retos de prueba: {len(prueba)}")

print("\nExperimento 1: sin entrenar")
red, Xt, yt, prueba = entrenar(0, datos)
linea("0 épocas", red, Xt, yt, prueba)

print("\nExperimento 2: 100, 200 y 400 épocas")
for epocas in (100, 200, 400):
    red, Xt, yt, prueba = entrenar(epocas, datos)
    linea(f"{epocas} épocas", red, Xt, yt, prueba)

print("\nExperimento 4: neuronas ocultas (400 épocas)")
for ocultas in (16, 32, 96, 128):
    red, Xt, yt, prueba = entrenar(400, datos, ocultas=ocultas)
    linea(f"{ocultas} neuronas", red, Xt, yt, prueba)

print("\nExperimento 5: tasa de aprendizaje (400 épocas)")
for tasa in (0.01, 0.1, 0.45, 1.0, 3.0):
    red, Xt, yt, prueba = entrenar(400, datos, tasa=tasa)
    linea(f"tasa {tasa}", red, Xt, yt, prueba)

print("\nExperimento 6: resultado por mapa (400 épocas, red pura)")
red, Xt, yt, prueba = entrenar(400, datos)
for indice in range(len(MAPAS)):
    filas = [f for f in prueba if f[0] == indice]
    pura, _ = completar(red, filas, asistido=False)
    asist, _ = completar(red, filas, asistido=True)
    print(f"  mapa {indice + 1}: {len(filas)} retos | pura {pura:.0%} | asistida {asist:.0%}")

print("\nExperimento 7: quién pone las etiquetas (400 épocas)")
for nombre, experto in (("BFS", etiqueta_bfs), ("DFS", etiqueta_dfs), ("A*", etiqueta_astar)):
    d = generar(experto)
    red, Xt, yt, _ = entrenar(400, d)
    # Todos se evalúan con los mismos retos de prueba de BFS.
    pura, extra_p = completar(red, prueba, asistido=False)
    asist, extra_a = completar(red, prueba, asistido=True)
    print(f"  {nombre:<4} | exactitud {red.exactitud(Xt, yt):.1%} | pura {pura:.0%} "
          f"(+{extra_p:.1f} pasos) | asistida {asist:.0%} (+{extra_a:.1f} pasos)")
