P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
P 'cat reporte_sistema.sh'
P 'chmod +x reporte_sistema.sh'
P './reporte_sistema.sh | tee reporte.txt'
P 'ls -l reporte.txt'
exec bash
