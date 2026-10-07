. ~/taller-ollama/lib.sh
hdr "Ejercicio 9 - Automatizacion con Bash"
cd ~/taller-ollama
echo "## Version de la guia: la linea de CPU no imprime nada porque el sistema esta en espanol"
run "LANG=es_ES.UTF-8 lscpu | grep \"Model name\""
run "lscpu | grep -i \"nombre del modelo\""
echo "## Script corregido (LC_ALL=C fuerza la salida en ingles solo para ese comando)"
run "diff reporte_sistema_original.sh reporte_sistema.sh"
run cat reporte_sistema.sh
run chmod +x reporte_sistema.sh
run ls -l reporte_sistema.sh
run "./reporte_sistema.sh | tee reporte.txt"
run ls -l reporte.txt
