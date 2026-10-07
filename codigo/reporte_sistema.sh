#!/bin/bash
echo "=== REPORTE DEL SISTEMA ==="
date
hostname
uname -a
echo "--- CPU ---"
nproc
LC_ALL=C lscpu | grep "Model name"   # LC_ALL=C: con Ubuntu en espanol lscpu imprime "Nombre del modelo"
echo "--- RAM ---"
free -h
echo "--- DISCO ---"
df -h /
echo "--- OLLAMA ---"
systemctl is-active ollama
