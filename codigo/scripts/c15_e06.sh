P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'ss -lntp | grep 11434'
P 'curl -s http://127.0.0.1:11434/api/version; echo'
P 'ip -br addr'
P 'curl -sS -m 3 http://10.0.2.15:11434/api/version'
P 'systemctl show ollama -p Environment'
exec bash
