# run: imprime el comando como en la terminal y lo ejecuta
run(){ echo "cloud@ubuntu-ollama:~\$ $*"; eval "$@" 2>&1; echo; }
# hdr: titulo + echo con los integrantes del grupo, fecha y equipo
hdr(){ echo "=================================================================="; echo "$*"; echo "=================================================================="; echo; run 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'; run "date; hostname"; }
