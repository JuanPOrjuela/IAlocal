. ~/taller-ollama/lib.sh
hdr "Ejercicio 4 - Administracion del servicio Ollama"
run systemctl status ollama --no-pager
echo "cloud@ubuntu-ollama:~\$ sudo systemctl stop ollama"; S systemctl stop ollama; echo
run systemctl is-active ollama
run curl -sS http://127.0.0.1:11434/api/tags
echo "cloud@ubuntu-ollama:~\$ sudo systemctl start ollama"; S systemctl start ollama; sleep 3; echo
run systemctl is-active ollama
run curl -sS http://127.0.0.1:11434/api/tags
echo "cloud@ubuntu-ollama:~\$ journalctl -u ollama -n 50 --no-pager"; S journalctl -u ollama -n 50 --no-pager; echo
