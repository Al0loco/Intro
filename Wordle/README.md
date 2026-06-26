# Wordle 🟩🟨⬜
**Alonso Campos Picado — C6D714**

Juego de Wordle implementado en Python, disponible en versión terminal y versión con interfaz gráfica.

---

## Archivos
| Archivo | Descripción |
|---|---|
| `main.py` | Versión en terminal |
| `wordle.py` | Versión con interfaz gráfica (tkinter) |
| `palabras.txt` | Lista de palabras válidas de 5 letras |
| `estadisticas.json` | Se crea automáticamente al jugar |

---

## Requisitos
- Python 3.x instalado
- `tkinter` (viene incluido con Python, no hay que instalar nada extra)

---

## Cómo correr el programa

### Opción 1 — Con Makefile (más fácil)

Primero entrá a la carpeta del proyecto:
```bash
cd Wordle
```

Versión terminal:
```bash
make terminal
```

Versión con interfaz gráfica:
```bash
make interfaz
```

Limpiar archivos generados:
```bash
make clean
```

---

### Opción 2 — Sin Makefile

Primero entrá a la carpeta del proyecto:
```bash
cd Wordle
```

Versión terminal:
```bash
python3 main.py
```

Versión con interfaz gráfica:
```bash
python3 wordle.py
```

---

## Cómo se juega
- Tenés **6 intentos** para adivinar una palabra de **5 letras**
- Después de cada intento se indica:
  - **V** / 🟩 Verde → letra correcta en posición correcta
  - **A** / 🟨 Amarillo → letra existe pero en posición incorrecta
  - **G** / ⬜ Gris → letra no existe en la palabra

---

## Funciona en
- macOS
- Windows