import os
import random
import numpy as np
import matplotlib.pyplot as plt
from patrones import patrones  # usa tus letras ya definidas (A, O, L, E, ...)

# === Crear carpeta de salida ===
os.makedirs("letras_ruido", exist_ok=True)

# === Función para guardar una letra como imagen ===
def guardar_letra(nombre, patron, carpeta="letras_ruido"):
    """Guarda una letra (patrón de ±1) como imagen PNG."""
    img = -patron.reshape(10, 10)  # <-- cambiado a 10x10
    plt.imshow(img, cmap="gray", vmin=-1, vmax=1)
    plt.axis("off")
    ruta = os.path.join(carpeta, f"{nombre}.png")
    plt.savefig(ruta, bbox_inches="tight", pad_inches=0)
    plt.close()
    return ruta

# === Función para agregar ruido (invertir píxeles aleatorios) ===
def agregar_ruido(patron, cantidad=5):
    """Invierte aleatoriamente 'cantidad' de píxeles en el patrón."""
    patron_ruido = patron.copy()
    indices = random.sample(range(len(patron)), cantidad)
    for idx in indices:
        patron_ruido[idx] *= -1
    return patron_ruido

# === Generar letras base y versiones con ruido ===
niveles_ruido = [1, 3, 5]  # cantidad de píxeles a invertir

for nombre, patron in patrones.items():
    # Guardar letra original
    ruta_original = guardar_letra(nombre, patron)
    print(f"✅ Guardado: {ruta_original}")

    # Generar versiones con ruido
    for n in niveles_ruido:
        patron_con_ruido = agregar_ruido(patron, cantidad=n)
        img = -patron_con_ruido.reshape(10, 10)  # <-- cambiado a 10x10
        plt.imshow(img, cmap="gray", vmin=-1, vmax=1)
        plt.axis("off")
        ruta = f"letras_ruido/{nombre}_ruido{n}.png"
        plt.savefig(ruta, bbox_inches="tight", pad_inches=0)
        plt.close()
        print(f"🌀 Generado con ruido ({n} píxeles): {ruta}")

print("\n🎯 Proceso completo. Imágenes guardadas en la carpeta 'letras_ruido/'")
