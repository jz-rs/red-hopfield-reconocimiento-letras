# interfaz.py
import tkinter as tk
from tkinter import messagebox, filedialog
from hopfield import entrenar, recordar
from patrones import patrones, mostrar_letra, imagen_a_vector
import numpy as np

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Red de Hopfield")
        self.root.geometry("580x600")
        self.root.resizable(False, False)

        # === TÍTULO ===
        tk.Label(
            root,
            text="Red de Hopfield",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # === SELECTOR DE LETRA ===
        frame_select = tk.Frame(root)
        frame_select.pack(pady=10)
        tk.Label(frame_select, text="Letra a probar:").pack(side=tk.LEFT, padx=5)
        self.var_letra = tk.StringVar(value="A")
        tk.OptionMenu(frame_select, self.var_letra, *patrones.keys()).pack(side=tk.LEFT)

        # === BOTONES PRINCIPALES ===
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=10)

        botones = [
            ("Entrenar Red", self.entrenar_red),
            ("Probar Reconocimiento", self.probar_letra),
            ("Ver letras entrenadas", self.mostrar_todas),
            ("Ver vector de la letra", self.ver_vector),
            ("Cargar imagen externa", self.cargar_imagen)
        ]
        for texto, comando in botones:
            tk.Button(frame_botones, text=texto, width=25, command=comando).pack(pady=4)

        # === ÁREA DE INFORMACIÓN ===
        frame_info = tk.Frame(root)
        frame_info.pack(pady=10)
        scrollbar = tk.Scrollbar(frame_info)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_info = tk.Text(frame_info, height=18, width=70, yscrollcommand=scrollbar.set)
        self.text_info.pack()
        scrollbar.config(command=self.text_info.yview)

        self.text_info.insert(tk.END, "💬 Bienvenido. Entrená la red para comenzar.\n\n")

    # === FUNCIONES ===
    def limpiar_texto(self):
        self.text_info.delete(1.0, tk.END)

    def separador(self, titulo):
        self.text_info.insert(tk.END, f"\n{'='*30}\n{titulo}\n{'='*30}\n", "titulo")
        self.text_info.see(tk.END)

    def entrenar_red(self):
        self.limpiar_texto()
        self.separador("🏋️‍♂️ ENTRENAMIENTO")
        entrenar(patrones)
        self.text_info.insert(tk.END, "✅ Red entrenada correctamente con las letras cargadas.\n\n")
        messagebox.showinfo("Entrenamiento", "La red fue entrenada correctamente.")

    def probar_letra(self):
        self.limpiar_texto()
        letra = self.var_letra.get()
        self.separador(f"🧠 PRUEBA DE LETRA: {letra}")
        resultado = recordar(patrones[letra], verbose=True, salida_texto=self.text_info)
        mostrar_letra(patrones[letra], f"Letra original: {letra}")
        mostrar_letra(resultado, "Letra reconocida por la red")
        self.text_info.insert(tk.END, f"✔️ Letra {letra} probada. Resultado mostrado.\n\n")
        self.text_info.see(tk.END)

    def ver_vector(self):
        letra = self.var_letra.get()
        self.separador(f"🔢 VECTOR DE {letra}")
        self.text_info.insert(tk.END, f"{patrones[letra]}\n\n")

    def mostrar_todas(self):
        self.separador("🖼️ PATRONES ENTRENADOS")
        for nombre, patron in patrones.items():
            mostrar_letra(patron, f"Letra {nombre}")
        self.text_info.insert(tk.END, "Se mostraron todas las letras entrenadas.\n\n")

    def cargar_imagen(self):
        self.limpiar_texto()
        ruta = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imagen PNG", "*.png"), ("Todos", "*.*")])
        if not ruta:
            return
        self.separador("🖼️ IMAGEN EXTERNA")
        vec = imagen_a_vector(ruta)
        self.text_info.insert(tk.END, f"Ruta cargada:\n{ruta}\n\nVector generado:\n{vec}\n\n")
        mostrar_letra(vec, "Imagen cargada")
        resultado = recordar(vec, verbose=True, salida_texto=self.text_info)
        mostrar_letra(resultado, "Reconocida por la red")
