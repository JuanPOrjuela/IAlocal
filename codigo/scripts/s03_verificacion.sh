. ~/taller-ollama/lib.sh
hdr "Seccion 03 - Pasos 4 a 7: verificacion de la instalacion"
echo "## Paso 4 - Verificar la instalacion"; run ollama -v; run which ollama
echo "## Paso 5 - Comprobar el servicio"; run systemctl status ollama --no-pager
echo "## Paso 6 - Habilitar e iniciar"; echo "cloud@ubuntu-ollama:~\$ sudo systemctl enable --now ollama"; S systemctl enable --now ollama 2>&1; echo; run systemctl is-enabled ollama; run systemctl status ollama --no-pager
echo "## Paso 7 - API local"; run curl -s http://127.0.0.1:11434/api/tags; run curl -s http://127.0.0.1:11434/api/version
