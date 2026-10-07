. ~/taller-ollama/lib.sh
hdr "Ejercicio 7 - Almacenamiento de modelos"
run df -h /
run ollama list
for m in gemma3:1b llama3.2:3b qwen2.5:7b; do
  echo "################ Modelo: $m ################"
  run df -h /
  echo "cloud@ubuntu-ollama:~\$ time ollama pull $m"
  s=$(date +%s); ollama pull $m 2>&1 | tr '\r' '\n' | grep -vE '^\s*$|pulling [0-9a-f]+:\s+[0-9]+%' | uniq; echo "tiempo de descarga: $(( $(date +%s)-s )) s"; echo
  run df -h /
done
run ollama list
echo "cloud@ubuntu-ollama:~\$ sudo du -sh /usr/share/ollama/.ollama/models"; S du -sh /usr/share/ollama/.ollama/models; echo
echo "cloud@ubuntu-ollama:~\$ sudo ls -lhS /usr/share/ollama/.ollama/models/blobs | head"; S ls -lhS /usr/share/ollama/.ollama/models/blobs | head; echo
