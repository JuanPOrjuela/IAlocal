P(){ printf '\e[01;32mcloud@ubuntu-ollama\e[00m:\e[01;34m~/taller-ollama\e[00m$ %s\n' "$*"; eval "$@"; }
cd ~/taller-ollama; clear
P 'echo "Angel Arcos - Sebastian Coral - Juan Orjuela - Javier Rosero"'
P date
read -r -d '' C1 <<'X'
curl -s http://localhost:11434/api/chat -d '{"model":"asistente-ciberseguridad","stream":false,"messages":[{"role":"user","content":"¿Qué es un firewall? Máximo 40 palabras."}]}' | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d["message"]["content"]); print("--- tokens:", d["eval_count"], "| tiempo total: %.1f s | %.1f tok/s" % (d["total_duration"]/1e9, d["eval_count"]/(d["eval_duration"]/1e9)))'
X
P 'curl -s http://localhost:11434/api/ps | python3 -m json.tool | grep -E "\"(name|size)\""'
P "$C1"
exec bash
