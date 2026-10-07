# Implementacion de IA local en VM con Ollama.

- Angel Arcos
- Sebastian Coral
- Juan Orjuela
- Javier Rosero

---

## 1. Definición de Inteligencia Artificial (IA)

Una **Inteligencia Artificial (IA)** es un software diseñado para procesar información y resolver tareas que requerían de la intervencion humana, como entender del lenguaje natural, el razonamiento lógico, el reconocimiento de patrones y la toma de decisiones basada en datos.

A diferencia de un software convencional, donde el programador establece manualmente reglas mediante sentencias condicionales como `if o else`, una IA  opera mediante **Machine Learning** y redes neuronales (*Deep Learning*). En lugar de seguir una lógica rígida preprogramada, el sistema identifica patrones a partir del análisis de datos, ajustando su comportamiento para resolver requests de manera autónoma.

En el caso específico de los **modelos de lenguaje locales (LLMs)**, la IA es una red neuronal preentrenada que almacena parámetros ponderados (pesos matemáticos). Al recibir una instrucción de entrada (*prompt*), el sistema evalúa la secuencia de términos previa y calcula, de forma probabilística y matricial, cuál es la siguiente palabra más adecuada para construir una respuesta estructurada y coherente.

---

## 2. Comparativa: IA Local vs. IA en la Nube

El despliegue de soluciones de inteligencia artificial varía significativamente según el entorno de ejecución, especialmente cuando se aísla en una **Máquina Virtual (VM)**:

| Criterio | IA en la Nube | IA Local en Máquina Virtual (*VM*) |
| :--- | :--- | :--- |
| **Entorno de ejecución** | Servidores externos y granjas de cómputo distribuidas (OpenAI, Google, AWS). | Entorno virtualizado y aislado (*sandbox*) dentro del equipo del usuario. |
| **Privacidad y confidencialidad** | Las consultas viajan por la red y dependen a políticas de privacidad del proveedor. | Ningún dato sale de la máquina virtual ni del equipo anfitrión. |
| **Dependencia de red** | Requiere conexión continua y estable a internet. | **Operación autónoma y fuera de línea (*offline*)**. |
| **Capacidad de cómputo** | Prácticamente ilimitada con modelos con cientos de miles de millones de parámetros. | **Acotada al hardware asignado:** Debe compartir memoria RAM con el sistema. |
| **Costos operativos** | Dependen del consumo de tokens (APIs). | **Costo cero por consulta**, requiriendo únicamente la descarga inicial de los pesos. |

---

## 3. Cinco Modelos de IA Viables

En un entorno virtualizado configurado entre 6 GB y 8 GB de RAM asignada, se priorizan modelos compactos como:

### 1. Llama 3.2 (3B) — Meta
* **Consumo de memoria estimado:** ~2.8 GB de RAM.
* **Propósito:** Modelo de lenguaje balanceado para tareas generales de redacción, síntesis documental, traducción y asistencia conversacional. Presenta un rendimiento sobresaliente en relación con su baja huella de memoria.

### 2. Phi-3.5 Mini (3.8B) — Microsoft
* **Consumo de memoria estimado:** ~3.2 GB de RAM.
* **Propósito:** Diseñado con énfasis en razonamiento lógico, análisis matemático y seguimiento de instrucciones estructuradas paso a paso, compitiendo favorablemente con modelos de mayor tamaño.

### 3. Qwen 2.5 Coder (3B) — Alibaba Cloud
* **Consumo de memoria estimado:** ~2.5 GB de RAM.
* **Propósito:** Especializado en ingeniería de software. Optimizado para análisis estático, depuración de sintaxis, generación de funciones y asistencia en lenguajes como Python, C++, Bash y JavaScript.

### 4. Gemma 2 (2B) — Google
* **Consumo de memoria estimado:** ~2.2 GB de RAM.
* **Propósito:** Modelo ultra compacto diseñado para procesamiento eficiente en CPU. Permite inferencias estables sin saturar los recursos de la máquina virtual, dejando margen para otros procesos del sistema.

### 5. Mistral 7B Instruct (v0.3, Cuantización Q4) — Mistral AI
* **Consumo de memoria estimado:** ~5.5 GB a 6.0 GB de RAM.
* **Propósito:** Estándar de referencia en la escala de 7 mil millones de parámetros. Ofrece capacidades superiores de redacción y comprensión analítica en tareas complejas dentro del límite operativo de una VM con 8 GB de RAM.

---

## 4. Tipos de IA Local y posibles con nuestro Hardware

### Especificaciones del Sistema y Entorno de Pruebas
* **Hardware del equipo anfitrión:** Intel Core i9-12900H (14 núcleos físicos / 20 hilos) y 16 GB de RAM física.
  * **vCPUs asignados:** 4 a 6 núcleos virtuales.
  * **Memoria RAM asignada:** 8 GB de RAM (garantizando 8 GB de reserva para la estabilidad del sistema anfitrión Windows).

### Viabilidad de implementaciones

| Categoría de IA Local | Estado de Viabilidad | Diagnóstico y Consideraciones Técnicas |
| :--- | :---: | :--- |
| **Modelos de Lenguaje Ligeros (1B a 4B)** | **viable** | Alta tasa de generación (*tokens/segundo*) ejecutándose directamente en CPU. |
| **Modelos de Lenguaje Medianos (7B a 8B Q4)** | **Viable con tasa moderada** | Funcionan con fluidez adecuada para lectura e interacción continua (~6–10 tokens/s). |
| **Reconocimiento de Voz (*Speech-to-Text*)** | **viable** | Implementaciones ligeras de OpenAI Whisper (`tiny`, `base`, `small`) transcriben audio. |
| **Modelos Masivos (14B o superiores)** | **No viable** | Exceden la memoria RAM asignada a la máquina virtual, generando errores de desbordamiento de memoria (*OOM*). |
| **Generación de Imágenes (*Diffusion Models*)** | **No recomendado** | La inferencia de modelos como Stable Diffusion mediante CPU en una máquina virtual resulta impráctica debido a tiempos excesivos de cálculo por imagen. |

---

## 5. Estructura del Repositorio y Entregables del Taller

Este repositorio contiene los archivos de configuración, código fuente, registros técnicos, capturas de pantalla y el informe formal desarrollado para el laboratorio de Sistemas Operativos:

```text
├── Informe_Taller_IA_Local_Sistemas_Operativos.pdf  # Informe técnico completo de 16 páginas
├── Modelfiles/                                      # Archivos Modelfile de personalización de IA
│   ├── Modelfile                                    # Asistente académico de ciberseguridad
│   ├── Modelfile.t01                                # Variante Temperatura 0.1 (Determinista)
│   ├── Modelfile.t07                                # Variante Temperatura 0.7 (Balanceada)
│   └── Modelfile.t10                                # Variante Temperatura 1.0 (Creativa)
├── Screenshots/                                     # Evidencias visuales de la VM y terminal
│   ├── 01_Ubuntu_Hardware_Audit.png
│   ├── 02_Base_Tools_Install.png
│   ├── 03_Ollama_Install_Official.png
│   ├── 04_Ollama_Version_Which.png
│   ├── 05_Ollama_Service_Status.png
│   ├── 06_API_Tags_Local.png
│   ├── 07_Ollama_Restart_Logs.png
│   ├── 08_Network_Port_11434.png
│   ├── 09_Memory_Baseline_Idle.png
│   ├── 10_Model_SmolLM2_Pull_Run.png
│   ├── 11_Model_Qwen25_Pull_Run.png
│   ├── 12_Model_TinyLlama_Pull_Run.png
│   ├── 13_Model_Benchmarking_Summary.png
│   ├── 14_Model_Admin_Show_Cp.png
│   ├── 15_Model_Admin_Stop_Rm.png
│   └── vm_desktop_gui.png                           # Entorno gráfico Xubuntu (XFCE) en ejecución
├── Scripts/                                         # Scripts de generación de informes y pruebas
│   ├── generate_pdf_report.py
│   ├── run_section02_hardware.py
│   ├── run_section03_install.py
│   ├── run_section04_admin.py
│   └── run_section05_models.py
└── Logs/                                            # Salidas crudas de comandos del sistema
    ├── Sec02_Hardware_Audit.txt
    ├── Sec03_Install_Verification.txt
    ├── Sec04_Service_Management.txt
    ├── Sec05_Models_Execution.txt
    └── Sec06_Modelfile_Output.txt
```

---

## 6. Estado Actual de Avance del Laboratorio

| Fase / Sección | Estado | Descripción técnica |
| :--- | :---: | :--- |
| **00 · Preparación y Snapshot** | **Completado** | VM Ubuntu 24.04 LTS configurada en VirtualBox con 4 vCPUs, 8 GB RAM, 50 GB VDI y snapshot pre-Ollama. |
| **01 · Entorno Gráfico (GUI)** | **Completado** | Instalación de `xubuntu-core`, `lightdm`, autologin y VirtualBox Guest Additions. |
| **02 · Auditoría de Hardware** | **Completado** | Inspección de CPU (`lscpu`), RAM (`free -h`), disco (`lsblk`, `df -h`) y kernel (`uname -a`). |
| **03 · Instalación de Ollama** | **Completado** | Instalación con script oficial, integración con `systemd`, puerto 11434 y verificación de `/api/tags`. |
| **04 · Administración de Servicio** | **Completado** | Control con `systemctl`, inspección de sockets con `ss -lntp` y logs con `journalctl`. |
| **05 · Modelos y Benchmarking** | **Completado** | Despliegue de `smollm2:135m`, `qwen2.5:0.5b` y `tinyllama:latest`. Pruebas de inferencia y administración (`show`, `cp`, `stop`, `rm`). |
| **06 · Modelfile Personalizado** | **Completado** | Construcción de `asistente-ciberseguridad` y variantes de temperatura (`0.1`, `0.7`, `1.0`). |
| **07 · Ejercicios Prácticos (1-10)** | *Pendiente* | 10 ejercicios de procesos, señales, red, scripts Bash e interpretación con IA. |
| **08-15 · API, Web UI, Seguridad** | *Pendiente* | Endpoints REST, interfaz web HTML/JS, análisis de capturas Wireshark y proyecto final. |

---

*Estudiantes: ANDRÉS SEBASTIÁN CORAL VALLEJO, JUAN ORJUELA, JAVIER ROSERO, ANGEL ARCOS*
*Universidad Sergio Arboleda — Sistemas Operativos*
