import os
import sys
import time
import subprocess
import paramiko

VBOXMANAGE = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
BASE_DIR = r"c:\Users\Sebas\OneDrive\Documents\Sergio Arboleda\Trabajos\Sistemas operativos\Taller - IA nube e IA local - Sistemas Operativos"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "Screenshots")
LOGS_DIR = os.path.join(BASE_DIR, "Logs")
KEY_PATH = r"C:\Users\Sebas\.ssh\id_ed25519"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

STUDENTS = "Estudiantes: ANDRÉS SEBASTIÁN CORAL VALLEJO, JUAN ORJUELA, JAVIER ROSERO, ANGEL ARCOS"

def execute_step(title, commands, screenshot_filename, sleep_delay=1.5, timeout=600):
    print(f"\n=======================================================")
    print(f">>> INICIANDO: {title}")
    print(STUDENTS)
    print(f"=======================================================")
    
    script_lines = [
        "#!/bin/bash",
        "export TERM=linux",
        "OUT=/tmp/screen_output.txt",
        'echo -e "\\033[2J\\033[H" > $OUT',
        f'echo "{STUDENTS}" >> $OUT',
        'echo "--------------------------------------------------------------------------------" >> $OUT'
    ]
    
    for cmd in commands:
        script_lines.append(f'echo "ubuntu@ubuntu-vm:~$ {cmd}" >> $OUT')
        script_lines.append(f'{cmd} >> $OUT 2>&1')
        script_lines.append('echo "" >> $OUT')
        
    script_lines.append('echo "--------------------------------------------------------------------------------" >> $OUT')
    script_lines.append(f'echo "{STUDENTS}" >> $OUT')
    script_lines.append('sudo cp $OUT /dev/tty1')
    script_lines.append('cat $OUT')
    
    script_content = "\n".join(script_lines) + "\n"
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("127.0.0.1", port=2222, username="ubuntu", key_filename=KEY_PATH, timeout=20)
    
    sftp = client.open_sftp()
    with sftp.file('/tmp/task_sec05_robust.sh', 'w') as f:
        f.write(script_content)
    sftp.close()
    
    exec_cmd = 'chmod +x /tmp/task_sec05_robust.sh && /tmp/task_sec05_robust.sh'
    stdin, stdout, stderr = client.exec_command(exec_cmd, timeout=timeout)
    output = stdout.read().decode('utf-8', errors='replace')
    err_output = stderr.read().decode('utf-8', errors='replace')
    client.close()
    
    log_path = os.path.join(LOGS_DIR, f"{screenshot_filename}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(output)
        if err_output:
            f.write("\n--- STDERR ---\n" + err_output)
            
    time.sleep(sleep_delay)
    
    shot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)
    subprocess.run([VBOXMANAGE, "controlvm", "Ubuntu-SO", "screenshotpng", shot_path], check=True)
    print(f"Captura guardada: {shot_path}")
    print(f">>> FINALIZADO: {title}")
    print(STUDENTS)
    print(f"=======================================================\n")
    return output

if __name__ == "__main__":
    print(STUDENTS)
    
    # 05.1 Descarga de Modelo 1 (smollm2:135m)
    execute_step(
        "Seccion 05 - Descarga de Modelo 1 (smollm2:135m)",
        [
            "ollama pull smollm2:135m",
            "ollama list"
        ],
        "Sec05_01_Pull_SmolLM2.png",
        timeout=180
    )

    # 05.2 Ejecucion e inferencia de smollm2:135m
    execute_step(
        "Seccion 05 - Ejecucion e inferencia de smollm2:135m",
        [
            'curl -s http://127.0.0.1:11434/api/generate -d \'{"model": "smollm2:135m", "prompt": "¿Que es un sistema operativo? Responde en una sola linea.", "stream": false}\' | grep -o \'"response":"[^"]*"\' | head -n 1',
            "ollama ps",
            "free -h"
        ],
        "Sec05_02_Run_SmolLM2_PS.png",
        timeout=120
    )

    # 05.3 Descarga de Modelo 2 (qwen2.5:0.5b)
    execute_step(
        "Seccion 05 - Descarga de Modelo 2 (qwen2.5:0.5b)",
        [
            "ollama pull qwen2.5:0.5b",
            "ollama list"
        ],
        "Sec05_03_Pull_Qwen.png",
        timeout=300
    )

    # 05.4 Ejecucion e inferencia de qwen2.5:0.5b
    execute_step(
        "Seccion 05 - Ejecucion e inferencia de qwen2.5:0.5b",
        [
            'curl -s http://127.0.0.1:11434/api/generate -d \'{"model": "qwen2.5:0.5b", "prompt": "¿Que es un sistema operativo? Responde en una sola linea.", "stream": false}\' | grep -o \'"response":"[^"]*"\' | head -n 1',
            "ollama ps",
            "free -h"
        ],
        "Sec05_04_Run_Qwen_PS.png",
        timeout=120
    )

    # 05.5 Descarga de Modelo 3 (tinyllama)
    execute_step(
        "Seccion 05 - Descarga de Modelo 3 (tinyllama)",
        [
            "ollama pull tinyllama",
            "ollama list"
        ],
        "Sec05_05_Pull_TinyLlama.png",
        timeout=400
    )

    # 05.6 Ejecucion e inferencia de tinyllama
    execute_step(
        "Seccion 05 - Ejecucion e inferencia de tinyllama",
        [
            'curl -s http://127.0.0.1:11434/api/generate -d \'{"model": "tinyllama", "prompt": "¿Que es un sistema operativo? Responde en una sola linea.", "stream": false}\' | grep -o \'"response":"[^"]*"\' | head -n 1',
            "ollama ps",
            "free -h"
        ],
        "Sec05_06_Run_TinyLlama_PS.png",
        timeout=180
    )

    # 05.7 Comandos de administracion: show, cp, stop, rm
    execute_step(
        "Seccion 05 - Administracion de modelos (show, cp, stop, rm)",
        [
            "ollama show smollm2:135m | head -n 12",
            "ollama cp smollm2:135m modelo-copia-seguridad",
            "ollama list",
            "ollama stop smollm2:135m qwen2.5:0.5b tinyllama",
            "ollama ps",
            "ollama rm modelo-copia-seguridad",
            "ollama list"
        ],
        "Sec05_07_Admin_Show_CP_Stop_RM.png",
        timeout=120
    )

    print("\n>>> Seccion 05 completada exitosamente!")
    print(STUDENTS)
