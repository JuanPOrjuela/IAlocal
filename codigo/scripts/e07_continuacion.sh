. ~/taller-ollama/lib.sh
hdr "Ejercicio 7 (continuacion) - tercer modelo y limpieza de la descarga interrumpida"
echo "La descarga de qwen2.5:7b (4.7 GB) se interrumpio dos veces al congelarse la VM (ver s02_vm_vs_anfitrion.txt)."
echo "Ollama deja los fragmentos como archivos *-partial en el directorio de blobs:"
echo "cloud@ubuntu-ollama:~\$ sudo ls -lh /usr/share/ollama/.ollama/models/blobs | grep partial"
S ls -lh /usr/share/ollama/.ollama/models/blobs | grep partial; echo
run df -h /
echo "cloud@ubuntu-ollama:~\$ sudo rm /usr/share/ollama/.ollama/models/blobs/*-partial*"
S bash -c 'rm -f /usr/share/ollama/.ollama/models/blobs/*-partial*'; echo
run df -h /
echo "Se reemplaza por un modelo de 1.5B que si es viable en esta VM:"
echo "################ Modelo: qwen2.5:1.5b ################"
run df -h /
echo "cloud@ubuntu-ollama:~\$ time ollama pull qwen2.5:1.5b"
s=$(date +%s); ollama pull qwen2.5:1.5b 2>&1 | tr '\r' '\n' | sed 's/\x1b\[[0-9;?]*[A-Za-z]//g' | grep -vE '^\s*$|pulling [0-9a-f]+:\s+[0-9]+%' | uniq; echo "tiempo de descarga: $(( $(date +%s)-s )) s"; echo
run df -h /
run ollama list
echo "cloud@ubuntu-ollama:~\$ sudo du -sh /usr/share/ollama/.ollama/models"; S du -sh /usr/share/ollama/.ollama/models; echo
echo "cloud@ubuntu-ollama:~\$ sudo ls -lhS /usr/share/ollama/.ollama/models/blobs | head"; S ls -lhS /usr/share/ollama/.ollama/models/blobs | head; echo
echo "Nota: asistente-ciberseguridad aparece con 2.0 GB pero reutiliza el blob de pesos de llama3.2:3b"
echo "(mismo sha256); solo agrega capas pequenas de parametros y prompt de sistema."
