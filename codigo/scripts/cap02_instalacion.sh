P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'grep -a -E "^>>>|WARNING" evidencias/03_paso3_instalar_ollama.txt'
P ollama -v
P which ollama
P id ollama
P 'systemctl is-enabled ollama; systemctl is-active ollama'
P 'curl -s http://127.0.0.1:11434/api/version; echo'
P 'curl -s http://127.0.0.1:11434/api/tags | python3 -m json.tool | grep "\"name\""'
exec bash
