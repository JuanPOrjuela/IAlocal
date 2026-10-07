P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'systemctl is-active ollama'
P 'sudo systemctl stop ollama'
P 'systemctl is-active ollama'
P 'curl -sS http://127.0.0.1:11434/api/tags'
P 'sudo systemctl start ollama'; sleep 3
P 'systemctl is-active ollama'
P 'curl -sS http://127.0.0.1:11434/api/version; echo'
P 'journalctl -u ollama -n 3 --no-pager -o cat | cut -c1-110'
P 'pgrep -a ollama'
PID=$(pgrep -x ollama)
P "ps -fp $PID"
P "systemctl show ollama -p MainPID -p KillSignal -p Restart"
exec bash
