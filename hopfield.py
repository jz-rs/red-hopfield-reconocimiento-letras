import numpy as np

W = None  # Matriz global de pesos


def entrenar(patrones):
    """Entrena la red Hopfield sumando los productos externos de los patrones (con centrado y escalado)."""
    global W
    cant_neuronas = len(next(iter(patrones.values())))
    W = np.zeros((cant_neuronas, cant_neuronas))

    for patron in patrones.values():
        # Asegura formato ±1 y centra el patrón para evitar sesgos
        p = np.where(patron > 0, 1, -1).astype(float)
        p = p - np.mean(p)  # centrado evita patrones dominantes
        W += np.outer(p, p)

    np.fill_diagonal(W, 0)
    W /= len(patrones)  # normaliza por cantidad de patrones (no por neuronas)
    print(f"✅ Red entrenada correctamente con {len(patrones)} patrones y {cant_neuronas} neuronas")
    return W


def energia(W, s):
    """Calcula la energía del sistema Hopfield clásico."""
    return -0.5 * s.T @ W @ s


def recordar(patron, max_sweeps=400, min_sweeps=3, patience=8, verbose=False, salida_texto=None):
    """
    Recordatorio Hopfield con actualización asincrónica.
    Cada 'sweep' actualiza todas las neuronas una vez en orden aleatorio.
    """
    global W
    x = patron.copy().astype(float)
    n = len(x)
    sin_cambios = 0

    def sign_keep_zero(u, prev):
        """Función de activación que mantiene el estado si u == 0."""
        return np.where(u > 0, 1, np.where(u < 0, -1, prev))

    for sweep in range(1, max_sweeps + 1):
        previo = x.copy()

        # Actualización asincrónica aleatoria
        for j in np.random.permutation(n):
            u = np.dot(W[j], x)
            if u > 0:
                x[j] = 1
            elif u < 0:
                x[j] = -1
            # si u == 0, mantiene valor anterior

        cambios = np.sum(x != previo)
        E = energia(W, x)

        if verbose:
            texto = (
                f"\nSweep {sweep}"
                f"\nCambios en este sweep: {cambios}"
                f"\nEnergía = {E:.3f}\n"
            )
            print(texto)
            if salida_texto:
                salida_texto.insert("end", texto)
                salida_texto.see("end")

        # Condiciones de parada
        if sweep >= min_sweeps:
            if cambios == 0:
                sin_cambios += 1
            else:
                sin_cambios = 0

            if sin_cambios >= patience:
                if verbose:
                    fin = f"\nConvergencia: sin cambios en {patience} sweeps consecutivos (total sweeps: {sweep}). Energía final = {E:.3f}\n"
                    print(fin)
                    if salida_texto:
                        salida_texto.insert("end", fin)
                        salida_texto.see("end")
                break

    return np.where(x > 0, 1, -1)
