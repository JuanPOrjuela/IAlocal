#!/usr/bin/env python3
"""Ejercicio 8: misma consulta a cada modelo via API REST; mide tiempos, tokens/s y RAM."""
import json, subprocess, sys, time, urllib.request

MODELOS = sys.argv[1:] or ["gemma3:1b", "qwen2.5:1.5b", "llama3.2:3b"]
PROMPT = ("Explica en maximo 120 palabras que es un proceso en un sistema operativo "
          "y en que se diferencia de un hilo. Da un ejemplo.")
API = "http://127.0.0.1:11434"

def post(path, body):
    req = urllib.request.Request(API + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)

def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

def ram_runner_mb():
    # RSS del proceso que carga el modelo (Ollama lo lanza como llama-server u "ollama runner")
    out = sh("ps -eo rss=,args= | grep -E 'llama-server|ollama runner' | grep -v grep | awk '{s+=$1} END {print s+0}'")
    return round(int(out or 0) / 1024)

filas = []
for m in MODELOS:
    tam = sh(f"ollama list | awk '$1==\"{m}\" {{print $3\" \"$4}}'")
    libre_antes = sh("free -m | awk '/Mem:/ {print $3}'")
    t0 = time.time()
    r = post("/api/generate", {"model": m, "prompt": PROMPT, "stream": False,
                                "options": {"temperature": 0.2, "seed": 42, "num_thread": 3}})
    pared = time.time() - t0
    rss = ram_runner_mb()
    usada_despues = sh("free -m | awk '/Mem:/ {print $3}'")
    ps = sh("ollama ps")
    ps_size = sh(f"ollama ps | awk '$1==\"{m}\" {{print $3\" \"$4}}'")
    ns = 1e9
    tps = r["eval_count"] / (r["eval_duration"] / ns)
    fila = dict(modelo=m, tamano=tam, rss_runner_mb=rss, ollama_ps_size=ps_size,
                ram_usada_mb_antes=int(libre_antes), ram_usada_mb_despues=int(usada_despues),
                tiempo_total_s=round(pared, 1), carga_s=round(r["load_duration"] / ns, 1),
                prompt_tokens=r.get("prompt_eval_count"), tokens_generados=r["eval_count"],
                tokens_por_s=round(tps, 2))
    filas.append(fila)
    print("=" * 70)
    print(f"MODELO: {m}  ({tam})")
    print(f"$ curl {API}/api/generate -d '{{\"model\":\"{m}\",\"prompt\":\"...\",\"stream\":false}}'")
    print("ollama ps durante la carga:\n" + ps)
    print(json.dumps(fila, ensure_ascii=False, indent=2))
    print("RESPUESTA:\n" + r["response"].strip() + "\n")
    # descargar el modelo de RAM antes del siguiente para medir limpio
    post("/api/generate", {"model": m, "keep_alive": 0})
    time.sleep(3)

print("=" * 70)
print("TABLA COMPARATIVA (Ejercicio 8)")
print(f"{'Modelo':<14}{'Tamano':<10}{'RSS runner':<12}{'ollama ps':<11}{'Carga s':<9}{'Total s':<9}{'Tokens':<8}{'Tok/s':<7}")
for f in filas:
    print(f"{f['modelo']:<14}{f['tamano']:<10}{str(f['rss_runner_mb'])+' MB':<12}{f['ollama_ps_size']:<11}{f['carga_s']:<9}{f['tiempo_total_s']:<9}{f['tokens_generados']:<8}{f['tokens_por_s']:<7}")
json.dump(filas, open("/home/cloud/taller-ollama/evidencias/e08_resultados.json", "w"), ensure_ascii=False, indent=2)
