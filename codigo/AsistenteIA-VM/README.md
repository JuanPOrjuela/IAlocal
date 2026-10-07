# AsistenteIA-VM

Proyecto final del Taller de Sistemas Operativos (Ubuntu VM + Ollama).
Asistente de ciberseguridad que corre 100 % local dentro de una máquina virtual Ubuntu.

## Entorno

| Elemento | Valor |
|---|---|
| Virtualizador | VirtualBox 7.2.16 sobre Windows 11 (i9-12900H, 16 GB) |
| VM | Ubuntu 24.04.5 LTS, kernel 7.0.0-34, 4 vCPU, 6 GB RAM, 40 GB disco, red NAT |
| Ollama | servicio systemd `ollama.service`, escucha en `127.0.0.1:11434`, modo CPU |
| Modelo base | `llama3.2:3b` (justificación en el informe, Ejercicio 8) |
| Modelo propio | `asistente-ciberseguridad` (creado con `Modelfile`) |

## Archivos

| Archivo | Qué es |
|---|---|
| `Modelfile` | Modelo base, `temperature 0.3`, `num_ctx 4096` y prompt de sistema de ciberseguridad |
| `index.html` | Interfaz web: consulta con `/api/chat` en streaming, historial de conversación, selector de modelo, tiempos y tokens/s, manejo de errores y límite por inactividad |
| `servir.sh` | Sirve la interfaz en `http://localhost:8080` (no `file://`) |
| `../scripts/` | Un script por ejercicio (`e01`…`e10`, `s02`…`s12`, `bench.py`, `temperaturas.py`) |
| `../reporte_sistema.sh` | Ejercicio 9 |

## Uso

```bash
# 1. Servicio activo
systemctl status ollama --no-pager

# 2. Crear el modelo personalizado (una sola vez)
ollama create asistente-ciberseguridad -f Modelfile

# 3. Levantar la interfaz y abrir http://localhost:8080 en Firefox dentro de la VM
./servir.sh
```

## Controles de seguridad

- Ollama escucha solo en loopback (`127.0.0.1:11434`); no se definió `OLLAMA_HOST=0.0.0.0` ni se abrió el puerto en el NAT.
- La interfaz también se sirve solo en `127.0.0.1:8080`.
- Override de systemd `limites.conf`: `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NUM_PARALLEL=1` para que la carga no congele la VM.
- No se envían credenciales ni datos personales al modelo; la captura de red es tráfico SSH propio del laboratorio.
- Las respuestas del modelo se contrastan con la salida real de los comandos (Ejercicio 10 y Reto, ver el informe).

## Limitaciones

- Sin GPU en la VM (VirtualBox no hace passthrough), toda la inferencia es en CPU.
- Modelos de 7B apenas caben en 6 GB y son lentos. Ver la tabla del Ejercicio 8.
- La interfaz usa streaming (NDJSON de /api/chat): el texto aparece mientras se genera y el límite de espera es por inactividad (90 s), no por tiempo total.
- Para uso real habría que poner un backend con autenticación delante de la API. Aquí no se expone a la red.
