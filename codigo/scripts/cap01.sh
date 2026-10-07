P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P ollama -v
P 'systemctl status ollama --no-pager -n 0'
P 'ss -lntp | grep -E "11434|8080"'
P ollama list
P ollama ps
exec bash
