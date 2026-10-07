. ~/taller-ollama/lib.sh
hdr "Ejercicio 5 - Procesos, senales y servicios"
run pgrep -a ollama
P=$(pgrep -f "ollama serve" | head -1)
run ps -fp $P
run "ps -o pid,ppid,user,stat,etime,nlwp,rss,cmd -p $P"
run "systemctl show ollama -p MainPID -p KillSignal -p KillMode -p Restart -p RestartUSec -p TimeoutStopUSec"
run "cat /proc/$P/status | grep -E 'Name|State|PPid|Threads|VmRSS'"
run "kill -l | head -4"
run systemctl status ollama --no-pager
