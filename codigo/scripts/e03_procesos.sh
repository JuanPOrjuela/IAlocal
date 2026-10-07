. ~/taller-ollama/lib.sh
M=${1:-asistente-ciberseguridad}
hdr "Ejercicio 3 - Procesos antes, durante y despues de la IA (modelo $M)"
snap(){ run free -h; run "ps aux --sort=-%cpu | head -6"; run "ps aux --sort=-%mem | head -6"; run "top -b -n1 | head -12"; run ollama ps; }
echo "############ ANTES (reposo) ############"; snap
echo "############ DURANTE la inferencia ############"
echo "cloud@ubuntu-ollama:~\$ ollama run --nowordwrap $M 'Escribe un ensayo detallado de 600 palabras sobre la planificacion de procesos en Linux (CFS, prioridades, nice)' &"
( ollama run --nowordwrap $M "Escribe un ensayo detallado de 600 palabras sobre la planificacion de procesos en Linux (CFS, prioridades, nice)" > /tmp/e03_respuesta.txt 2>/dev/null ) &
BG=$!
sleep 25; snap
run "pgrep -a ollama"
run "ps -o pid,ppid,user,%cpu,%mem,rss,nlwp,cmd -C ollama"
run "vmstat 1 5"
wait $BG
echo "############ DESPUES (modelo aun cargado en RAM, keep_alive 5 min) ############"; snap
echo "cloud@ubuntu-ollama:~\$ ollama stop $M"; ollama stop $M; sleep 2; echo
echo "############ DESPUES de ollama stop ############"; run free -h; run ollama ps
echo "--- Primeras lineas de la respuesta generada ---"; head -c 1200 /tmp/e03_respuesta.txt; echo
