
# Makefile - Wordle
# Uso:
#   make terminal    → corre la versión en terminal
#   make interfaz    → corre la versión con interfaz gráfica
#   make clean       → limpia archivos generados
 
terminal:
	python3 main.py
 
interfaz:
	python3 wordle.py
 
clean:
	rm -f estadisticas.json
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
 