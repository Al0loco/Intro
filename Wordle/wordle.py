# version optimizada con interfaz
import json
import random
import tkinter as tk
from tkinter import messagebox
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)

# ─── Colores y fuentes ────────────────────────────────────────────────────────
COLOR_FONDO        = "#F5F0E8"   # crema
COLOR_TITULO       = "#3B2A1A"   # café oscuro
COLOR_SUBTITULO    = "#C6D714"   # amarillo lima (Alonso)
COLOR_BOTON        = "#C4A882"   # café claro
COLOR_BOTON_TEXTO  = "#3B2A1A"
COLOR_BOTON_HOVER  = "#A8845A"
COLOR_CUADRO       = "#E8DFD0"   # cuadro vacío
COLOR_BORDE        = "#B8A898"
COLOR_VERDE        = "#6AAA64"
COLOR_AMARILLO     = "#C9B458"
COLOR_GRIS         = "#787C7E"
COLOR_TEXTO_CUADRO = "#FFFFFF"

FUENTE_TITULO    = ("Georgia", 42, "bold")
FUENTE_SUBTITULO = ("Georgia", 14, "italic")
FUENTE_BOTON     = ("Helvetica", 14, "bold")
FUENTE_LETRA     = ("Helvetica", 22, "bold")
FUENTE_STATS     = ("Helvetica", 13)

# ─── Cargar palabras desde un archivo de texto ────────────────────────────────
def cargarPalabras():
    try:
        with open("palabras.txt", "r") as archivo:
            palabras = [line.strip().lower() for line in archivo if len(line.strip()) == 5]
        if not palabras:
            raise ValueError
    except:
        # palabras de respaldo si no existe el archivo
        palabras = ["gatos", "perro", "clave", "cielo", "playa", "mundo", "verde",
                    "canto", "libro", "juego", "fuego", "noche", "tarde", "nueva",
                    "pared", "campo", "torre", "danza", "entre", "bello"]
    return palabras

# ─── Elegir una palabra aleatoria ────────────────────────────────────────────
def elegirPalabra(palabras):
    return random.choice(palabras)

# ─── Validar la palabra ingresada ────────────────────────────────────────────
def validarEntrada(intentoUsuario):
    if len(intentoUsuario) != 5:
        return False, "La palabra debe tener exactamente 5 letras."
    for letra in intentoUsuario:
        if not letra.isalpha():
            return False, "La palabra solo puede contener letras."
    return True, ""

# ─── Comparar intento con la palabra secreta ─────────────────────────────────
def compararIntento(intentoUsuario, palabraSecreta):
    resultado = ["gris"] * 5

    # Primero marcar los verdes
    for i in range(5):
        if intentoUsuario[i] == palabraSecreta[i]:
            resultado[i] = "verde"

    # Contar cuántas veces aparece cada letra en la secreta
    # sin contar las que ya quedaron en verde
    conteo = {}
    for i in range(5):
        if resultado[i] != "verde":  # solo contar las que no son verdes
            letra = palabraSecreta[i]
            if letra in conteo:
                conteo[letra] += 1
            else:
                conteo[letra] = 1

    # Luego marcar amarillos usando el conteo
    for i in range(5):
        if resultado[i] == "verde":
            continue
        letra = intentoUsuario[i]
        if letra in conteo and conteo[letra] > 0:
            resultado[i] = "amarillo"
            conteo[letra] -= 1  # consumir una ocurrencia

    return resultado

# ─── Cargar estadísticas desde JSON ──────────────────────────────────────────
def cargarEstadsJSON():
    try:
        with open("estadisticas.json", "r") as archivo:
            estadisticas = json.load(archivo)
    except FileNotFoundError:
        estadisticas = {"partidas_jugadas": 0, "partidas_ganadas": 0}
    return estadisticas

# ─── Guardar estadísticas en JSON ────────────────────────────────────────────
def guardarEstadsJSON(estadisticas):
    with open("estadisticas.json", "w") as archivo:
        json.dump(estadisticas, archivo)

# ─── Confeti ──────────────────────────────────────────────────────────────────
class Confeti:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.particulas = []
        self.corriendo = False

    def crear_particulas(self):
        colores = ["#E63946", "#F4A261", "#2A9D8F", "#E9C46A", "#264653",
                   "#C6D714", "#6AAA64", "#C9B458", "#A8DADC", "#F1FAEE"]
        for _ in range(120):
            x = random.randint(0, self.width)
            y = random.randint(-self.height, 0)
            color = random.choice(colores)
            size = random.randint(7, 14)
            speed = random.uniform(3, 7)
            swing = random.uniform(-2, 2)
            forma = random.choice(["rect", "oval"])
            id_ = self.canvas.create_rectangle(x, y, x+size, y+size, fill=color, outline="") \
                  if forma == "rect" else \
                  self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            self.particulas.append({"id": id_, "speed": speed, "swing": swing, "x": x, "y": y, "size": size})

    def animar(self):
        if not self.corriendo:
            return
        for p in self.particulas:
            p["x"] += p["swing"]
            p["y"] += p["speed"]
            self.canvas.move(p["id"], p["swing"], p["speed"])
            if p["y"] > self.height:
                p["y"] = -p["size"]
                p["x"] = random.randint(0, self.width)
                self.canvas.coords(p["id"], p["x"], p["y"], p["x"]+p["size"], p["y"]+p["size"])
        self.canvas.after(30, self.animar)

    def iniciar(self):
        self.corriendo = True
        self.crear_particulas()
        self.animar()

    def detener(self):
        self.corriendo = False
        for p in self.particulas:
            self.canvas.delete(p["id"])
        self.particulas = []

# ─── Aplicación principal ─────────────────────────────────────────────────────
class WordleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        # centrar ventana
        ancho, alto = 520, 600
        x = (self.root.winfo_screenwidth() - ancho) // 2
        y = (self.root.winfo_screenheight() - alto) // 2
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.palabras = cargarPalabras()
        self.mostrarMenu()

    # ── Limpiar ventana ──────────────────────────────────────────────────────
    def limpiar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ── Efecto hover en botones ───────────────────────────────────────────────
    def agregarHover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg=COLOR_BOTON_HOVER))
        boton.bind("<Leave>", lambda e: boton.config(bg=COLOR_BOTON))

    # ════════════════════════════════════════════════════════════════════════════
    # PANTALLA MENÚ PRINCIPAL
    # ════════════════════════════════════════════════════════════════════════════
    def mostrarMenu(self):
        self.limpiar()
        self.root.geometry("520x600")

        marco = tk.Frame(self.root, bg=COLOR_FONDO)
        marco.pack(expand=True)

        # título
        tk.Label(marco, text="WORDLE", font=FUENTE_TITULO,
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=(60, 4))

        # subtítulo
        tk.Label(marco, text="Alonso Campos Picado — C6D714",
                 font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_SUBTITULO).pack(pady=(0, 50))

        # línea decorativa
        tk.Frame(marco, bg=COLOR_BORDE, height=2, width=260).pack(pady=(0, 40))

        # botones
        for texto, comando in [("Jugar", self.mostrarJuego),
                                 ("Estadísticas", self.mostrarEstadisticas),
                                 ("Salir", self.confirmarSalir)]:
            b = tk.Button(marco, text=texto, font=FUENTE_BOTON,
                          bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO,
                          width=18, pady=10, bd=0, relief="flat",
                          cursor="hand2", command=comando)
            b.pack(pady=8)
            self.agregarHover(b)

    # ════════════════════════════════════════════════════════════════════════════
    # PANTALLA DE JUEGO
    # ════════════════════════════════════════════════════════════════════════════
    def mostrarJuego(self):
        self.limpiar()
        self.root.geometry("520x700")

        self.palabraSecreta = elegirPalabra(self.palabras)
        self.intentoActual  = 0
        self.maxIntentos    = 6
        self.juegoTerminado = False
        self.letraActual    = 0
        self.letrasIngresadas = [["" for _ in range(5)] for _ in range(6)]

        # encabezado
        encabezado = tk.Frame(self.root, bg=COLOR_FONDO)
        encabezado.pack(fill="x", padx=20, pady=(18, 0))
        tk.Button(encabezado, text="← Menú", font=("Helvetica", 11),
                  bg=COLOR_FONDO, fg=COLOR_TITULO, bd=0, cursor="hand2",
                  command=self.mostrarMenu).pack(side="left")
        tk.Label(encabezado, text="WORDLE", font=("Georgia", 22, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(side="left", expand=True)

        # tablero 6×5
        self.celdas = []
        marco_tablero = tk.Frame(self.root, bg=COLOR_FONDO)
        marco_tablero.pack(pady=18)

        for fila in range(6):
            fila_celdas = []
            for col in range(5):
                celda = tk.Label(marco_tablero, text="", width=3, height=1,
                                 font=FUENTE_LETRA, bg=COLOR_CUADRO,
                                 fg=COLOR_TEXTO_CUADRO, relief="flat",
                                 bd=0, highlightthickness=2,
                                 highlightbackground=COLOR_BORDE,
                                 highlightcolor=COLOR_BORDE)
                celda.grid(row=fila, column=col, padx=4, pady=4, ipadx=10, ipady=10)
                fila_celdas.append(celda)
            self.celdas.append(fila_celdas)

        # mensaje de estado
        self.lblMensaje = tk.Label(self.root, text="", font=("Helvetica", 12),
                                   bg=COLOR_FONDO, fg=COLOR_TITULO)
        self.lblMensaje.pack(pady=4)

        # teclado en pantalla
        self.dibujarTeclado()

        # capturar teclas físicas
        self.root.bind("<Key>", self.teclaPresionada)
        self.root.bind("<BackSpace>", self.borrarLetra)
        self.root.bind("<Return>", self.enviarIntento)
        self.root.focus_set()

    def dibujarTeclado(self):
        marco = tk.Frame(self.root, bg=COLOR_FONDO)
        marco.pack(pady=10)

        filas_teclado = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        self.botones_teclado = {}

        for fila_letras in filas_teclado:
            fila_frame = tk.Frame(marco, bg=COLOR_FONDO)
            fila_frame.pack(pady=3)

            if fila_letras == "ZXCVBNM":
                # botón ENTER
                b_enter = tk.Button(fila_frame, text="↵", font=("Helvetica", 11, "bold"),
                                    bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO,
                                    width=4, pady=6, bd=0, relief="flat", cursor="hand2",
                                    command=lambda: self.enviarIntento(None))
                b_enter.pack(side="left", padx=2)

            for letra in fila_letras:
                b = tk.Button(fila_frame, text=letra, font=("Helvetica", 11, "bold"),
                              bg=COLOR_CUADRO, fg=COLOR_TITULO,
                              width=3, pady=6, bd=0, relief="flat", cursor="hand2",
                              command=lambda l=letra: self.ingresarLetra(l))
                b.pack(side="left", padx=2)
                self.botones_teclado[letra] = b

            if fila_letras == "ZXCVBNM":
                # botón BORRAR
                b_del = tk.Button(fila_frame, text="⌫", font=("Helvetica", 11, "bold"),
                                  bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO,
                                  width=4, pady=6, bd=0, relief="flat", cursor="hand2",
                                  command=lambda: self.borrarLetra(None))
                b_del.pack(side="left", padx=2)

    def teclaPresionada(self, evento):
        if self.juegoTerminado:
            return
        if evento.char and evento.char.isalpha() and len(evento.char) == 1:
            self.ingresarLetra(evento.char.upper())

    def ingresarLetra(self, letra):
        if self.juegoTerminado or self.letraActual >= 5:
            return
        if letra == " ":  # bloquear espacios
            return
        self.letrasIngresadas[self.intentoActual][self.letraActual] = letra.lower()
        self.celdas[self.intentoActual][self.letraActual].config(
            text=letra.upper(), bg="#DDD5C5", highlightbackground="#8C8C8C")
        self.letraActual += 1

    def borrarLetra(self, evento):
        if self.juegoTerminado or self.letraActual <= 0:
            return
        self.letraActual -= 1
        self.letrasIngresadas[self.intentoActual][self.letraActual] = ""
        self.celdas[self.intentoActual][self.letraActual].config(
            text="", bg=COLOR_CUADRO, highlightbackground=COLOR_BORDE)

    def enviarIntento(self, evento):
        if self.juegoTerminado:
            return
        if self.letraActual < 5:  # no dejar enviar si no hay 5 letras
            self.lblMensaje.config(text="Debes ingresar 5 letras.", fg="#E63946")
            return
        intento = "".join(self.letrasIngresadas[self.intentoActual])
        valido, msg = validarEntrada(intento)
        if not valido:
            self.lblMensaje.config(text=msg, fg="#E63946")
            return

        resultado = compararIntento(intento, self.palabraSecreta)

        # colorear celdas con animación
        for col in range(5):
            color = COLOR_VERDE if resultado[col] == "verde" else \
                    COLOR_AMARILLO if resultado[col] == "amarillo" else COLOR_GRIS
            self.root.after(col * 120, lambda c=col, clr=color, l=intento[col]:
                self.celdas[self.intentoActual][c].config(bg=clr, fg="white",
                    text=l.upper(), highlightbackground=clr))

            # actualizar color del teclado
            letra_upper = intento[col].upper()
            if letra_upper in self.botones_teclado:
                btn = self.botones_teclado[letra_upper]
                color_actual = btn.cget("bg")
                if color_actual != COLOR_VERDE:
                    if resultado[col] == "verde":
                        btn.config(bg=COLOR_VERDE, fg="white")
                    elif resultado[col] == "amarillo" and color_actual != COLOR_AMARILLO:
                        btn.config(bg=COLOR_AMARILLO, fg="white")
                    elif resultado[col] == "gris" and color_actual == COLOR_CUADRO:
                        btn.config(bg=COLOR_GRIS, fg="white")

        self.root.after(5 * 120 + 100, lambda: self.procesarResultado(intento, resultado))

    def procesarResultado(self, intento, resultado):
        if intento == self.palabraSecreta:
            self.juegoTerminado = True
            self.lblMensaje.config(text="¡Felicidades! 🎉", fg=COLOR_VERDE,
                                   font=("Helvetica", 15, "bold"))
            estadisticas = cargarEstadsJSON()
            estadisticas["partidas_jugadas"] += 1
            estadisticas["partidas_ganadas"] += 1
            guardarEstadsJSON(estadisticas)
            self.root.after(500, self.mostrarConfeti)
        else:
            self.intentoActual += 1
            self.letraActual = 0
            if self.intentoActual >= self.maxIntentos:
                self.juegoTerminado = True
                self.lblMensaje.config(
                    text=f"La palabra era: {self.palabraSecreta.upper()}",
                    fg="#E63946", font=("Helvetica", 12, "bold"))
                estadisticas = cargarEstadsJSON()
                estadisticas["partidas_jugadas"] += 1
                guardarEstadsJSON(estadisticas)
            else:
                self.lblMensaje.config(text="", fg=COLOR_TITULO)

    def mostrarConfeti(self):
        # ventana de confeti encima
        ventana = tk.Toplevel(self.root)
        ventana.title("")
        ventana.geometry("520x500")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        canvas = tk.Canvas(ventana, width=520, height=500,
                           bg=COLOR_FONDO, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        confeti = Confeti(canvas, 520, 500)
        confeti.iniciar()

        tk.Label(canvas, text="¡Felicidades!", font=("Georgia", 34, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).place(relx=0.5, rely=0.38, anchor="center")
        tk.Label(canvas, text="¡Adivinaste la palabra! 🎊", font=("Helvetica", 14),
                 bg=COLOR_FONDO, fg=COLOR_SUBTITULO).place(relx=0.5, rely=0.50, anchor="center")

        tk.Button(canvas, text="Volver al menú", font=FUENTE_BOTON,
                  bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO, bd=0, relief="flat",
                  cursor="hand2", padx=20, pady=8,
                  command=lambda: [confeti.detener(), ventana.destroy(), self.mostrarMenu()]
                  ).place(relx=0.5, rely=0.65, anchor="center")

        ventana.after(6000, lambda: [confeti.detener(), ventana.destroy()] if ventana.winfo_exists() else None)

    # ════════════════════════════════════════════════════════════════════════════
    # PANTALLA DE ESTADÍSTICAS
    # ════════════════════════════════════════════════════════════════════════════
    def mostrarEstadisticas(self):
        self.limpiar()
        self.root.geometry("520x440")

        estadisticas = cargarEstadsJSON()
        jugadas = estadisticas["partidas_jugadas"]
        ganadas = estadisticas["partidas_ganadas"]
        porcentaje = round((ganadas / jugadas) * 100) if jugadas > 0 else 0

        marco = tk.Frame(self.root, bg=COLOR_FONDO)
        marco.pack(expand=True, fill="both", padx=40, pady=30)

        tk.Label(marco, text="Estadísticas", font=("Georgia", 28, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_TITULO).pack(pady=(10, 4))
        tk.Frame(marco, bg=COLOR_BORDE, height=2, width=260).pack(pady=(0, 30))

        # tarjetas de stats
        tarjetas_frame = tk.Frame(marco, bg=COLOR_FONDO)
        tarjetas_frame.pack(pady=10)

        datos = [
            (str(jugadas), "Partidas\njugadas"),
            (str(ganadas), "Partidas\nganadas"),
            (f"{porcentaje}%", "Porcentaje\nde victorias"),
        ]

        for valor, etiqueta in datos:
            card = tk.Frame(tarjetas_frame, bg=COLOR_BOTON, padx=18, pady=14)
            card.pack(side="left", padx=10)
            tk.Label(card, text=valor, font=("Georgia", 30, "bold"),
                     bg=COLOR_BOTON, fg=COLOR_TITULO).pack()
            tk.Label(card, text=etiqueta, font=("Helvetica", 10),
                     bg=COLOR_BOTON, fg=COLOR_TITULO, justify="center").pack()

        # botón volver
        tk.Frame(marco, bg=COLOR_BORDE, height=2, width=260).pack(pady=(30, 20))
        b = tk.Button(marco, text="← Volver al menú", font=FUENTE_BOTON,
                      bg=COLOR_BOTON, fg=COLOR_BOTON_TEXTO,
                      width=18, pady=10, bd=0, relief="flat",
                      cursor="hand2", command=self.mostrarMenu)
        b.pack()
        self.agregarHover(b)

    # ════════════════════════════════════════════════════════════════════════════
    # CONFIRMAR SALIDA
    # ════════════════════════════════════════════════════════════════════════════
    def confirmarSalir(self):
        respuesta = messagebox.askyesno(
        "Salir",
        "¿Estás seguro de que querés salir del juego?",
        icon="question"
    )
    if respuesta:
        guardarEstadsJSON({"partidas_jugadas": 0, "partidas_ganadas": 0})
        self.root.destroy()


# Punto de entrada 
if __name__ == "__main__":
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()