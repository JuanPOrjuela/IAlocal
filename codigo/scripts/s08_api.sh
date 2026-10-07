. ~/taller-ollama/lib.sh
M=${1:-asistente-ciberseguridad}
hdr "Seccion 08 - API REST de Ollama (modelo $M)"
fmt(){ python3 -c 'import json,sys; d=json.load(sys.stdin); r=d.get("response") or d["message"]["content"]; print(r.strip()); print("\n[metricas] modelo=%s total=%.1fs carga=%.1fs tokens=%s velocidad=%.1f tok/s" % (d["model"], d["total_duration"]/1e9, d["load_duration"]/1e9, d["eval_count"], d["eval_count"]/(d["eval_duration"]/1e9)))'; }

echo "## /api/generate (cURL)"
cat <<EOF
cloud@ubuntu-ollama:~\$ curl http://localhost:11434/api/generate \\
  -d '{
    "model": "$M",
    "prompt": "¿Qué es ciberseguridad?",
    "stream": false
  }'
EOF
curl -s http://localhost:11434/api/generate -d "{\"model\":\"$M\",\"prompt\":\"¿Qué es ciberseguridad? Responde en máximo 120 palabras.\",\"stream\":false}" | tee /tmp/gen.json | fmt
echo; echo "Campos que devuelve la API (JSON crudo, sin el texto):"
python3 -c 'import json; d=json.load(open("/tmp/gen.json")); d.pop("response"); d.pop("context",None); print(json.dumps(d, indent=2))'
echo

echo "## /api/chat (cURL)"
cat <<EOF
cloud@ubuntu-ollama:~\$ curl http://localhost:11434/api/chat \\
  -d '{
    "model": "$M",
    "messages": [
      {"role":"user","content":"¿Qué es un firewall?"}
    ],
    "stream": false
  }'
EOF
curl -s http://localhost:11434/api/chat -d "{\"model\":\"$M\",\"messages\":[{\"role\":\"user\",\"content\":\"¿Qué es un firewall? Responde en máximo 120 palabras.\"}],\"stream\":false}" | tee /tmp/chat1.json | fmt
echo

echo "## /api/chat con historial (segundo turno: la pregunta depende de la respuesta anterior)"
python3 - "$M" <<'PY'
import json, sys, urllib.request
m = sys.argv[1]
prev = json.load(open("/tmp/chat1.json"))["message"]
msgs = [{"role": "user", "content": "¿Qué es un firewall? Responde en máximo 120 palabras."}, prev,
        {"role": "user", "content": "¿Y cuál es la diferencia entre el tipo que mencionaste primero y un WAF? Máximo 100 palabras."}]
print("messages enviados:", json.dumps([{"role": x["role"], "content": x["content"][:60] + "..."} for x in msgs], ensure_ascii=False, indent=2))
req = urllib.request.Request("http://localhost:11434/api/chat", json.dumps({"model": m, "messages": msgs, "stream": False}).encode(), {"Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req, timeout=600))
print("\nRespuesta del segundo turno:\n" + d["message"]["content"].strip())
print("\n[metricas] total=%.1fs tokens=%s prompt_tokens=%s (crece porque se reenvia el historial)" % (d["total_duration"]/1e9, d["eval_count"], d.get("prompt_eval_count")))
PY
echo
echo "## Nota sobre el ejemplo de PowerShell de la guia"
echo "El bloque Invoke-RestMethod es sintaxis de PowerShell (anfitrion Windows). En este laboratorio Ollama"
echo "escucha solo en 127.0.0.1 dentro de la VM, por lo que desde el anfitrion no es alcanzable (ver Ejercicio 6)."
echo "Se deja asi a proposito: exponerlo requeriria OLLAMA_HOST=0.0.0.0 y aumenta la superficie de ataque."
