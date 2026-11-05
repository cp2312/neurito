# Experimentos: Neurito en el laberinto

Neurito debe llegar a la comida. Probé 716 retos que la red nunca vio al entrenar. "Completa" significa llegar a la comida en 45 movimientos o menos.

## Experimentos

1. Sin entrenar: se atasca porque sus pesos son al azar y casi siempre elige la misma dirección, aunque haya una pared. Solo completa el 3 % de los retos.
2. Entrenar 100, 200 y 400 épocas:

   | Épocas | Pérdida | Exactitud | Completa (red pura) |
   |---|---|---|---|
   | 100 | 0.135 | 84.9 % | 51 % |
   | 200 | 0.038 | 90.1 % | 81 % |
   | 400 | 0.011 | 91.5 % | 83 % |

   Mejora rápido al principio y luego casi se queda igual.
3. Red pura frente a asistido: la red pura completa el 83 %; el modo asistido completa el 100 %. El modelo aporta la dirección que prefiere. Las reglas aportan lo demás: no chocar con paredes y no repetir casillas. Por eso el asistido funciona hasta sin entrenar (88 %), y no demuestra que la red aprendió.
4. Neuronas ocultas (la red pura completa): 16 → 74 %, 32 → 78 %, 96 → 83 %, 128 → 85 %. Más neuronas ayudan un poco.
5. Tasa de aprendizaje (la red pura completa): 0.01 → 20 %, 0.1 → 60 %, 0.45 → 83 %, 1.0 → 85 %, 3.0 → 88 %. Con 0.01 es muy lenta. Con 0.45 sí converge, y subirla hasta 3.0 también funciona aquí.
6. Cambiar de mapa (red pura): mapa 1 → 86 %, mapa 2 → 78 %, mapa 3 → 84 %. Funciona en los tres, y el mapa 2 es el más difícil. Los mapas sí entraron al entrenamiento; lo nuevo son las combinaciones de inicio y comida.
7. Cambiar quién pone las etiquetas:

   | Experto | Exactitud | Completa (pura) | Completa (asistida) |
   |---|---|---|---|
   | BFS (original) | 91.5 % | 83 % | 100 % |
   | A* | 92.6 % | 86 % | 100 % |
   | DFS | 94.8 % | 11 % | 59 % |

   A* queda casi igual que BFS, porque los dos encuentran caminos cortos. DFS empeora mucho: sus caminos dan vueltas y no son consistentes, y la red aprende rutas malas.

## Conclusión

La exactitud no es lo mismo que completar el laberinto. Con DFS la exactitud es la más alta (94.8 %), pero la red pura solo llega a la comida en el 11 % de los retos. También el modo asistido puede esconder una red que no aprendió.
