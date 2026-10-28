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
