. ~/taller-ollama/lib.sh
hdr "Seccion 06 - Modelo personalizado con Modelfile"
cd ~/taller-ollama/AsistenteIA-VM
run cat Modelfile
run ollama create asistente-ciberseguridad -f Modelfile
run ollama list
run ollama show asistente-ciberseguridad
run ollama show --modelfile asistente-ciberseguridad
echo "cloud@ubuntu-ollama:~\$ ollama run --nowordwrap asistente-ciberseguridad '¿Qué es un ataque de fuerza bruta?'"
ollama run --nowordwrap asistente-ciberseguridad "¿Qué es un ataque de fuerza bruta? Responde en máximo 200 palabras." 2>/dev/null
echo
echo "cloud@ubuntu-ollama:~\$ ollama stop asistente-ciberseguridad"; ollama stop asistente-ciberseguridad; echo
