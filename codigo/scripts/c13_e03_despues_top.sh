P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'ollama ps'
P 'ollama stop asistente-ciberseguridad'
P 'ollama ps'
P 'free -h'
exec bash
