# Experimentos de Neurito

Neurito mira hambre, energía y aburrimiento, y elige: comer, dormir o jugar. Gana la necesidad más alta.

## Experimentos

1. Cambiar una necesidad: con energía 0.5 y aburrimiento 0.3, sube el hambre. Con hambre baja duerme; pasando de 0.5 come. Ahí hay empate porque el cansancio (1 - 0.5) también es 0.5.
2. Prioridades casi iguales: Softmax reparte casi parejo (35 %, 33 %, 31 %). Elige, pero con poca seguridad.
3. Neuronas ocultas: con 3 la precisión es 96.3 %, con 6 es 99.4 %, con 10 es 99.3 % y con 20 es 98.8 %. Con 3 se queda corta; desde 6 ya aprende bien y más neuronas no ayudan.
4. Épocas y tasa de aprendizaje:
   - Más épocas mejoran, pero cada vez menos (100 épocas: 77 %, 1200: 99 %).
   - Tasa muy chica (0.001): casi no aprende (42 %).
   - Tasa muy grande (5 o más): se vuelve inestable (34 %).
   - La original (0.1) es la buena.
5. Cuarta acción (ej. bañarse): hace falta una necesidad nueva, una regla para etiquetar, ejemplos de esa acción y una neurona más en la salida.

## Explica tus resultados

- Pesos vs. sesgos: el peso dice cuánto importa cada entrada; el sesgo es un empujón fijo que ajusta cuándo se activa la neurona.
- Por qué 1 - energía: más energía es menos cansancio. Así las tres necesidades quedan igual: número alto = urgente.
- ReLU: deja pasar lo positivo y pone en 0 lo negativo; permite aprender reglas que no son rectas.
- Softmax: convierte la salida en porcentajes que suman 100 %.
- Precisión engañosa: el 99 % es contra una regla inventada, y los pocos errores están justo en los empates, que son los casos difíciles.

# Experimentos: Neurito aprende a saltar- TALLER 2

Neurito aprende cuándo saltar un obstáculo. Cada prueba duró unos 5 minutos de juego.

## Experimentos

1. Sin entrenar: no salta nunca. Chocó 59 veces y esquivó 0.
2. Entrenar de 100 en 100 épocas: la pérdida baja (0.26 → 0.06) y la precisión sube (91 % → 98 %). Con 300 épocas ya no choca.
3. Neuronas ocultas:
   - 3 neuronas: 93 % de precisión, no chocó.
   - 12 neuronas (original): 98 %, no chocó.
   - 24 neuronas: 98 %, igual que 12. No ayuda tener más.
4. Tasa de aprendizaje:
   - 0.01: muy lenta, no aprendió a saltar.
   - 0.8 (original): funciona bien.
   - 1.2: también funciona.
5. Ventana de entrenamiento (cuándo "toca saltar"):
   - 7 a 13 fotogramas antes (original): no choca.
   - 2 a 5: tampoco choca.
   - 15 a 25 o 30 a 40: choca siempre, aunque la precisión es de 98 %.

## Pregunta central

¿Por qué una red puede clasificar bien y aun así chocar?

Porque la precisión solo mide si la red repite las etiquetas que le dimos, no si el salto sirve en el juego. En la prueba 5, la ventana de 15 a 25 hizo que Neurito saltara demasiado pronto: caía antes de que llegara el obstáculo y chocaba. La red aprendió bien una regla que estaba mal.

## Taller neurito en el laberinto
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