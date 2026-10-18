# Red de Hopfield para reconocer letras

Red neuronal de Hopfield discreta, hecha desde cero en Python, que reconoce letras dibujadas en una grilla de 10×10 píxeles en blanco y negro, incluso cuando la imagen llega con ruido. La desarrollamos con **Juana Ruiz Luque**.

## Qué hace

- Entrena la red con un conjunto de letras (A, O, L, E, I, H, T, Z) y genera la matriz de pesos.
- Reconoce las letras de entrenamiento y versiones parecidas pero no iguales (con píxeles cambiados).
- Muestra en cada paso la energía y los cambios, y dibuja la letra de salida.
- Permite cargar una imagen externa (PNG), reducirla a 10×10 y probar si la red la reconoce.
- Incluye `letras_ruido/`, con cada letra y versiones con 1, 3 y 5 píxeles alterados.

## Cómo funciona

Cada letra es un vector de 100 valores (+1 negro, −1 blanco). Los pesos se arman sumando el producto externo de cada patrón consigo mismo, con la diagonal en cero:

```
W = Σ (Eᵢ · Eᵢᵀ) − I
```

Al reconocer, las neuronas se actualizan de a una en orden aleatorio (asincrónico) hasta que la red deja de cambiar. La energía `E = −½ sᵀWs` baja en cada paso, y la red termina en un patrón guardado o en un estado espurio.

## Qué aprendimos al diseñar las letras

Empezamos con una grilla de 4×4, pero la capacidad era muy limitada. Pasamos a 10×10, que según la regla de capacidad (~0,14 × cantidad de neuronas) alcanza para unos 15 patrones.

Descubrimos que **la red depende mucho de cómo se dibujan las letras**:

- Necesitan diferenciarse entre sí en alrededor de un 30 % de los píxeles.
- La cantidad de píxeles negros (densidad) tiene que ser parecida entre letras, en nuestro caso entre 20 % y 36 %.
- Las letras simétricas (O, A, H, T, I) o que comparten filas y columnas generan estados espurios, donde la red mezcla dos letras.

Para dos o más patrones muy parecidos, las mejoras que identificamos son:

1. Diferencias estructurales claras entre letras.
2. Densidades balanceadas.
3. Evitar simetrías perfectas.
4. Agrandar la grilla.

## Cómo correrlo

```bash
pip install -r requirements.txt
python main.py
```

Se abre una ventana para entrenar la red, probar una letra, ver las letras entrenadas, ver su vector y cargar una imagen externa. `generar_imagenes_ruido.py` vuelve a generar las imágenes de `letras_ruido/`.

## Archivos

```
hopfield.py                 Entrenamiento, energía y recuerdo
patrones.py                 Letras de entrenamiento y lectura de imágenes
interfaz.py / main.py       Interfaz de escritorio (Tkinter)
mapa_energia.py             Gráfico de energía de estados con ruido
generar_imagenes_ruido.py   Genera las imágenes con ruido
letras_ruido/               Imágenes de prueba
```

## Autoría

Desarrollado junto con Juana Ruiz Luque.
