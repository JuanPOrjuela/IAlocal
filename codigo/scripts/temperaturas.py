#!/usr/bin/env python3
"""Experimento seccion 06: tres versiones del asistente con temperature 0.1, 0.7 y 1.0.
Misma pregunta, dos corridas por version, para comparar determinismo y variedad."""
import difflib, json, subprocess, urllib.request

PREGUNTA = "¿Qué es un firewall? Responde en máximo 90 palabras."
BASE = "/home/cloud/taller-ollama/AsistenteIA-VM/Modelfile"
API = "http://127.0.0.1:11434/api/generate"

def generar(modelo):
    body = {"model": modelo, "prompt": PREGUNTA, "stream": False, "options": {"num_predict": 180, "num_thread": 3}}
    req = urllib.request.Request(API, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    return d["response"].strip(), d["eval_count"] / (d["eval_duration"] / 1e9)

base = open(BASE, encoding="utf-8").read()
print("Pregunta usada en todas las versiones:", PREGUNTA, "\n")
resumen = []
for t in ("0.1", "0.7", "1.0"):
    nombre = f"asistente-temp{t.replace('.', '')}"
    mf = base.replace("PARAMETER temperature 0.3", f"PARAMETER temperature {t}")
    ruta = f"/home/cloud/taller-ollama/AsistenteIA-VM/Modelfile.temp{t.replace('.', '')}"
    open(ruta, "w", encoding="utf-8").write(mf)
    print("=" * 70)
    print(f"$ ollama create {nombre} -f {ruta.split('/')[-1]}   (temperature {t})")
    print(subprocess.run(["ollama", "create", nombre, "-f", ruta], capture_output=True, text=True).stdout.strip().splitlines()[-1:])
    r1, v1 = generar(nombre)
    r2, v2 = generar(nombre)
    sim = difflib.SequenceMatcher(None, r1, r2).ratio()
    resumen.append((t, sim, len(r1.split()), len(r2.split()), (v1 + v2) / 2))
    print(f"--- Corrida 1 ({v1:.1f} tok/s) ---\n{r1}\n--- Corrida 2 ({v2:.1f} tok/s) ---\n{r2}")
    print(f">>> Similitud entre corridas: {sim:.0%}\n", flush=True)
    # liberar la RAM antes de cargar la siguiente variante (cada nombre se carga como modelo aparte)
    urllib.request.urlopen(urllib.request.Request(
        API, json.dumps({"model": nombre, "keep_alive": 0}).encode(),
        {"Content-Type": "application/json"}), timeout=60).read()

print("=" * 70)
print("RESUMEN")
print(f"{'temperature':<13}{'similitud c1 vs c2':<21}{'palabras c1/c2':<16}{'tok/s prom'}")
for t, s, p1, p2, v in resumen:
    print(f"{t:<13}{s:<21.0%}{f'{p1}/{p2}':<16}{v:.1f}")
