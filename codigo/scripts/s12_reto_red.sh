. ~/taller-ollama/lib.sh
M=${1:-asistente-ciberseguridad}
hdr "Seccion 12 - Reto: IA + analisis de red (captura SSH propia del laboratorio)"
echo "Autorizacion: se captura unicamente el trafico SSH entre el anfitrion (Windows, NAT VirtualBox)"
echo "y esta VM, ambos del grupo. No se captura trafico de terceros."
echo
C=~/taller-ollama/evidencias/captura_ssh.pcapng
echo "## 1. Captura (tshark = Wireshark en linea de comandos)"
echo "cloud@ubuntu-ollama:~\$ sudo tshark -i enp0s3 -f 'tcp port 22' -a duration:25 -w captura_ssh.pcapng"
S rm -f /tmp/cap.pcapng
S tshark -i enp0s3 -f "tcp port 22" -a duration:25 -w /tmp/cap.pcapng -q 2>&1 | grep -v "^Running as" &
sleep 3
touch /tmp/trafico_generado   # la sesion SSH que genera trafico corre desde el anfitrion en paralelo
wait
S cp /tmp/cap.pcapng $C; S chown cloud:cloud $C
run ls -lh $C
echo "## 2. Extraccion de metadatos (solo lo necesario)"
run "capinfos -c -d -u -y -i $C"
run "tshark -r $C -q -z conv,tcp"
run "tshark -r $C -q -z io,phs"
run "tshark -r $C -Y ssh.protocol -T fields -e frame.number -e ip.src -e ip.dst -e ssh.protocol"
run "tshark -r $C -Y 'ssh.message_code' -T fields -e frame.number -e ip.src -e ssh.message_code | head -12"
run "tshark -r $C -Y ssh.kex_algorithms -T fields -e ssh.kex_algorithms | head -2 | cut -c1-200"
PKT=$(capinfos -c -M $C | awk -F: '/Number of packets/ {gsub(/ /,"",$2); print $2}')
DUR=$(capinfos -u -M $C | awk -F: '/Capture duration/ {gsub(/ seconds| /,"",$2); print $2}')
BYT=$(capinfos -d -M $C | awk -F: '/Data size/ {gsub(/ bytes| /,"",$2); print $2}')
PROTO=$(tshark -r $C -Y ssh.protocol -T fields -e ssh.protocol | head -2 | tr '\n' ' ')
echo "## 3. Interpretacion con IA (datos ya depurados)"
P="Se analizó una captura de tráfico de un laboratorio propio.
Protocolo: SSH
Puerto destino: 22
Origen: 10.0.2.2 (gateway NAT de VirtualBox que representa al anfitrión)
Destino: 10.0.2.15 (VM Ubuntu)
Paquetes: $PKT
Duración: $DUR s
Bytes: $BYT
Banners de versión: $PROTO
Ayúdame a interpretar técnicamente estos datos.
Distingue entre:
1. Información observable.
2. Información inferible.
3. Información que permanece protegida por cifrado.
4. Evidencias que debería validar nuevamente con Wireshark.
Máximo 300 palabras."
echo "--- Prompt enviado ---"; echo "$P"; echo
echo "--- Respuesta del modelo $M ---"
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
echo "## 4. Validacion: se contrasta en el informe con las salidas de tshark de arriba"
