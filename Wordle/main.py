import json
import random
# para compilar en terminal: python3 main.py

# Cargar palabras desde un archivo de texto
def cargarPalabras():
    with open("palabras.txt", "r") as archivo:
        palabras = [line.strip() for line in archivo]
    return palabras

# Elegir una palabra aleatoria de la lista de palabras
def elegirPalabra(palabras):
    return random.choice(palabras)

# Crear matriz vacia de 6 filas y 5 columnas
def crearTablero():
    tablero = []           # lista principal vacía
    
    for i in range(6):     # 6 filas (intentos)
        fila = []
        for j in range(5): # 5 columnas (letras)
            fila.append("_")
        tablero.append(fila)
    
    return tablero

# mostrar matriz vacia que va a ser el tablero del juego
def mostrarTablero(tablero):  # se agrega tablero como parámetro
    print("\nWORDLE")
    for i in tablero:
        print(i)

# Validar la palabra ingresada
def validarEntrada(intentoUsuario):
    # Verificar que tenga exactamente 5 letras
    if len(intentoUsuario) != 5:
        print("La palabra debe tener exactamente 5 letras.")
        return False
    
    # Verificar que solo tenga letras del alfabeto
    for letra in intentoUsuario:
        if not letra.isalpha():
            print("La palabra solo puede contener letras.")
            return False
    
    return True

def compararIntento(intentoUsuario, palabraSecreta):
    resultado = []  # lista que guardará el estado de cada letra
    
    for i in range(5):
        if intentoUsuario[i] == palabraSecreta[i]:
            resultado.append("verde")        # letra correcta en posición correcta
        elif intentoUsuario[i] in palabraSecreta:
            resultado.append("amarillo")     # letra existe pero en posición incorrecta
        else:
            resultado.append("gris")         # letra no existe en la palabra
    
    return resultado

def colorearTableroTerminal(tablero, fila, intentoUsuario, resultado):  # version sin interfaz
    for i in range(5):
        letra = intentoUsuario[i].upper()  # se pone la letra ingresada en el tablero
        if resultado[i] == "verde":
            tablero[fila][i] = f"{letra}V"  # letra correcta en posición correcta
        elif resultado[i] == "amarillo":
            tablero[fila][i] = f"{letra}A"  # letra existe pero en posición incorrecta
        else:
            tablero[fila][i] = f"{letra}G"  # letra no existe en la palabra
 
def cargarEstadsJSON():
    try:
        with open("estadisticas.json", "r") as archivo:
            estadisticas = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        estadisticas = {"partidas_jugadas": 0, "partidas_ganadas": 0}
    return estadisticas

def guardarEstadsJSON(estadisticas):
    with open("estadisticas.json", "w") as archivo: #w es para escribir en el archivo
        json.dump(estadisticas, archivo)

def mostrarEstads(estadisticas):
    print("\nEstadísticas del juego:")
    print(f"Partidas jugadas: {estadisticas['partidas_jugadas']}")
    print(f"Partidas ganadas: {estadisticas['partidas_ganadas']}")

def jugar():
    palabras = cargarPalabras()
    palabraSecreta = elegirPalabra(palabras)
    tablero = crearTablero()
    estadisticas = cargarEstadsJSON()
    
    intentos = 0
    maxIntentos = 6
    juegoGanado = False
    
    while intentos < maxIntentos and not juegoGanado: # mientras el numero de intentos sea menor a 6 y el juego no se haya ganado
        mostrarTablero(tablero)
        intentoUsuario = input("Ingresa una palabra de 5 letras: ").lower()
        
        if not validarEntrada(intentoUsuario): # si la palabra ingresada no es valida, se le pide al usuario que ingrese otra palabra
            continue
        
        resultado = compararIntento(intentoUsuario, palabraSecreta)
        colorearTableroTerminal(tablero, intentos, intentoUsuario, resultado)  # se pasa intentoUsuario
        
        if intentoUsuario == palabraSecreta:
            juegoGanado = True
            mostrarTablero(tablero)
            print("¡Felicidades! Has adivinado la palabra.")
        
        intentos += 1
    
    if not juegoGanado:
        print(f"Lo siento, has agotado tus intentos. La palabra del día era: {palabraSecreta}")
    
    estadisticas["partidas_jugadas"] += 1
    if juegoGanado:
        estadisticas["partidas_ganadas"] += 1
    
    guardarEstadsJSON(estadisticas)
    mostrarEstads(estadisticas)

jugar()