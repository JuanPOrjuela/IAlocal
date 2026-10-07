#!/bin/bash
# Sirve la interfaz por HTTP (no file://) para que el navegador permita la peticion a Ollama.
# Ollama acepta por defecto origenes http://localhost y http://127.0.0.1 (OLLAMA_ORIGINS).
cd "$(dirname "$0")"
echo "Abrir en el navegador de la VM: http://localhost:8080"
exec python3 -m http.server 8080 --bind 127.0.0.1
