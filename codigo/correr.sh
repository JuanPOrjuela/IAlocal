cd ~/taller-ollama; mkdir -p evidencias
for s in s02_preparacion_vm s03_verificacion s04_administracion e01_identificacion e02_paquetes e04_servicio e05_senales e06_red e09_bash; do
  bash -c "S(){ echo Cloud | sudo -S -p '' \"\$@\"; }; export -f S; LC_ALL=es_ES.UTF-8 bash scripts/$s.sh" > evidencias/$s.txt 2>&1; echo "$s: $(wc -l < evidencias/$s.txt) lineas"
done
