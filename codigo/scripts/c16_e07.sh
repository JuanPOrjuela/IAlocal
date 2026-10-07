P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'df -BM / | tail -1'
P 'ollama list'
P 'ollama pull smollm2:135m 2>&1 | tail -1'
P 'df -BM / | tail -1'
P 'ollama cp smollm2:135m prueba-alias'
P 'ollama list | grep -E "NAME|smollm|prueba"'
P 'ollama rm prueba-alias smollm2:135m'
P 'df -BM / | tail -1'
exec bash
