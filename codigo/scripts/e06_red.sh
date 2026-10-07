. ~/taller-ollama/lib.sh
hdr "Ejercicio 6 - Red y puerto de Ollama"
echo "cloud@ubuntu-ollama:~\$ sudo ss -lntp | grep 11434"; S ss -lntp | grep 11434; echo
run curl -s http://127.0.0.1:11434/api/tags
run ip addr
IP=$(hostname -I | awk '{print $1}')
echo "## Prueba: la API NO responde por la IP de la interfaz ($IP), solo por loopback"
run curl -sS -m 3 http://$IP:11434/api/tags
run "systemctl show ollama -p Environment"
