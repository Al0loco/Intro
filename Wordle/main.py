import json
import random

# Cargar palabras desde un archivo de texto
def cargarPalabras():
    with open("palabras.txt", "r") as archivo:
        palabras = [line.strip() for line in archivo]
    return palabras

# Elegir una palabra aleatoria de la lista de palabras
def elegirPalabra(palabras):
    return random.choice(palabras)

#Crear matriz vacia de 6 filas y 5 columnas
def crearTablero():
    tablero = []           # lista principal vacía
    
    for i in range(6):     # 6 filas (intentos)
        fila = []
        for j in range(5): # 5 columnas (letras)
            fila.append("_")
        tablero.append(fila)
    
    return tablero


# mostrar matriz vacia que va a ser el tablero del juego 
def mostrarTablero():
    print("WORDLE")
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
    
