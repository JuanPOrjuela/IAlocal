P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'cat AsistenteIA-VM/Modelfile'
P 'ollama show --modelfile asistente-ciberseguridad | grep -E "^PARAMETER (temperature|num_ctx|num_thread)"'
P 'ollama run --nowordwrap asistente-ciberseguridad "¿Qué es un ataque de fuerza bruta? Responde en máximo 40 palabras."'
exec bash
