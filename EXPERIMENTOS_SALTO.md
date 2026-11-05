# Experimentos: Neurito aprende a saltar

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
