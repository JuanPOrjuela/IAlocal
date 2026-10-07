P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
C=evidencias/captura_ssh.pcapng
P "capinfos -c -d -u $C | tail -3"
P "tshark -r $C -q -z conv,tcp | sed -n 5,12p | cut -c1-118"
P "tshark -r $C -Y ssh.protocol -T fields -e ip.src -e ssh.protocol | head -2"
P "tshark -r $C -Y ssh.message_code -T fields -e frame.number -e ip.src -e ssh.message_code | head -5"
exec bash
