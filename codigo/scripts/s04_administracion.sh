. ~/taller-ollama/lib.sh
hdr "Seccion 04 - Administracion de Ollama en Ubuntu"
echo "## Servicio"; run systemctl status ollama --no-pager
echo "cloud@ubuntu-ollama:~\$ sudo systemctl restart ollama"; S systemctl restart ollama; sleep 3; echo
run systemctl status ollama --no-pager
echo "cloud@ubuntu-ollama:~\$ journalctl -u ollama -n 100 --no-pager"; S journalctl -u ollama -n 100 --no-pager; echo
echo "## Puerto 11434"; echo "cloud@ubuntu-ollama:~\$ sudo ss -lntp | grep 11434"; S ss -lntp | grep 11434; echo
run curl -s http://127.0.0.1:11434/api/tags
echo "## Recursos (htop es interactivo: se usa top en modo batch como equivalente)"
run free -h; run "top -b -n1 | head -15"; run nvidia-smi
