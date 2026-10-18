import numpy as np
import matplotlib.pyplot as plt
from hopfield import energia
from patrones import patrones

# --- Configuración ---
num_muestras = 300   # cuántos puntos aleatorios probar
ruido_max = 0.3      # porcentaje máximo de bits alterados
np.random.seed(0)    # reproducibilidad

# Convertimos patrones a matriz binaria
patrones_bin = {k: np.where(v > 0, 1, -1) for k, v in patrones.items()}
keys = list(patrones_bin.keys())
n = len(next(iter(patrones_bin.values())))

energias = []
coincidencias = []
letras_cercanas = []

for _ in range(num_muestras):
    # Elegir una letra base
    letra_ref = np.random.choice(keys)
    p = patrones_bin[letra_ref].copy()

    # Aplicar ruido (cambiar bits)
    mask = np.random.rand(n) < ruido_max
    p_ruidoso = np.where(mask, -p, p)

    # Calcular energía del estado inicial
    E = energia(W, p_ruidoso)
    energias.append(E)

    # Determinar a qué letra se parece más tras converger
    # (esto simula el "pozo" donde cayó)
    mejor_letra = None
    mejor_similitud = -1
    for letra, patron in patrones_bin.items():
        sim = np.mean(p_ruidoso == patron)
        if sim > mejor_similitud:
            mejor_similitud = sim
            mejor_letra = letra

    letras_cercanas.append(mejor_letra)
    coincidencias.append(mejor_similitud)

# --- Gráfico de energía por letra ---
plt.figure(figsize=(8, 5))
plt.scatter(range(num_muestras), energias, c=[keys.index(l) for l in letras_cercanas],
            cmap="tab10", alpha=0.7)
plt.colorbar(ticks=range(len(keys)), label="Letra dominante")
plt.clim(-0.5, len(keys)-0.5)
plt.title("Mapa simplificado de energía Hopfield")
plt.xlabel("Muestras (estados iniciales con ruido)")
plt.ylabel("Energía inicial E = -0.5·sᵀWs")
plt.show()

# --- Estadísticas resumidas ---
print("Promedio de energía por letra:")
for letra in keys:
    E_med = np.mean([e for e, l in zip(energias, letras_cercanas) if l == letra])
    print(f"{letra}: {E_med:.2f}")
