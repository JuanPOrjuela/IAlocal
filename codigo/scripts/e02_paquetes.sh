. ~/taller-ollama/lib.sh
hdr "Ejercicio 2 - Gestion de paquetes"
echo "cloud@ubuntu-ollama:~\$ sudo apt update"; S apt-get update 2>&1; echo
echo "cloud@ubuntu-ollama:~\$ sudo apt install -y htop curl git"; S apt-get install -y htop curl git 2>&1; echo
run apt policy htop curl git
run "apt list --upgradable 2>/dev/null | head"
