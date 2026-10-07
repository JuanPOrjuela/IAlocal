#!/bin/bash
echo "=== REPORTE DEL SISTEMA ==="
date
hostname
uname -a
echo "--- CPU ---"
nproc
lscpu | grep "Model name"
echo "--- RAM ---"
free -h
echo "--- DISCO ---"
df -h /
echo "--- OLLAMA ---"
systemctl is-active ollama
