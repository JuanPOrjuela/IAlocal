P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'lsb_release -a 2>/dev/null'
P 'uname -a'
P 'nproc; lscpu | grep -E "Nombre del modelo|hipervisor|virtualización"'
P 'free -h'
P 'lsblk -e7'
P 'df -h /'
P 'du -sh ~'
exec bash
