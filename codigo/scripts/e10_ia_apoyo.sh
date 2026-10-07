. ~/taller-ollama/lib.sh
M=${1:-asistente-ciberseguridad}
hdr "Ejercicio 10 - IA como herramienta de apoyo del SO (modelo $M)"
# 1) Datos del sistema (no sensibles: no hay usuarios, IPs publicas ni secretos)
D=/tmp/e10_datos.txt
{
  echo "\$ free -h"; free -h; echo
  echo "\$ df -h /"; df -h /; echo
  echo "\$ systemctl status ollama --no-pager (primeras 9 lineas)"; systemctl status ollama --no-pager | head -9; echo
  echo "\$ ps aux --sort=-%mem | head -6"; ps aux --sort=-%mem | head -6 | cut -c1-150
} > $D
echo "############ 1. DATOS DE ENTRADA (copiados al modelo) ############"
cat $D
echo
echo "############ 2. PROMPT ############"
P="Eres apoyo para un estudiante de Sistemas Operativos. Interpreta estas salidas de una VM Ubuntu: cuánta RAM está realmente disponible, si el disco es un riesgo, si el servicio ollama está sano y qué procesos consumen más memoria. Sé concreto y usa los números. Máximo 250 palabras.

$(cat $D)"
echo "$P" | head -3; echo "(... seguido de los datos de entrada)"
echo
echo "############ 3. RESPUESTA DE LA IA ############"
python3 - "$M" "$P" <<'PY'
import json, sys, urllib.request
req = urllib.request.Request("http://localhost:11434/api/generate",
    json.dumps({"model": sys.argv[1], "prompt": sys.argv[2], "stream": False, "options": {"temperature": 0.2, "num_thread": 3}}).encode(),
    {"Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=900))
print(d["response"].strip())
print("\n[metricas] %.1f s, %s tokens" % (d["total_duration"]/1e9, d["eval_count"]))
PY
echo
echo "############ 4. VERIFICACION DIRECTA EN UBUNTU (para contrastar) ############"
run "free -m | awk '/Mem:/ {printf \"RAM total %d MB, usada %d MB, disponible %d MB (%.0f%% disponible)\n\", \$2, \$3, \$7, \$7*100/\$2}'"
run "df -h / | awk 'NR==2 {print \"Disco raiz: \" \$5 \" usado, \" \$4 \" libres\"}'"
run systemctl is-active ollama
run "systemctl show ollama -p NRestarts -p ActiveEnterTimestamp"
run "ps -o pid,user,rss,cmd --sort=-rss -e | head -4"
