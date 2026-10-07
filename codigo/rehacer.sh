#!/bin/bash
# Vuelve a generar las evidencias (una a la vez) con el echo de los integrantes.
cd ~/taller-ollama
S(){ echo Cloud | sudo -S -p "" "$@"; }; export -f S
. ./lib.sh
export LC_ALL=es_ES.UTF-8
E=evidencias; L=~/taller-ollama/rehacer.log; : > $L
paso(){ echo "$(date +%T) inicio $1" >> $L; sync; }
for s in s02_preparacion_vm s03_verificacion s04_administracion e01_identificacion e02_paquetes e04_servicio e05_senales e06_red e09_bash; do
  paso $s; bash scripts/$s.sh > $E/$s.txt 2>&1; sync
done
paso s06;  bash scripts/s06_modelfile.sh > $E/s06_modelfile.txt 2>&1; sync
paso temp; { hdr "Seccion 06 - Experimento de temperatura (0.1 / 0.7 / 1.0)"; python3 -u scripts/temperaturas.py; } > $E/s06_experimento_temperatura.txt 2>&1; sync
paso e08;  { hdr "Ejercicio 8 - Rendimiento y seleccion del modelo"; python3 -u scripts/bench.py; } > $E/e08_rendimiento.txt 2>&1; sync
paso e03;  bash scripts/e03_procesos.sh > $E/e03_procesos.txt 2>&1; sync
paso s08;  bash scripts/s08_api.sh > $E/s08_api.txt 2>&1; sync
paso e10;  bash scripts/e10_ia_apoyo.sh > $E/e10_ia_apoyo.txt 2>&1; sync
echo "$(date +%T) FIN" >> $L; sync
