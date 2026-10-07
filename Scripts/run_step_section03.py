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

def run_step(title, commands, screenshot_filename, sleep_delay=2.0, timeout=600):
    print(f"\n=======================================================")
    print(f">>> INICIANDO: {title}")
    print(STUDENTS)
    print(f"=======================================================")
    
    script_lines = [
        "#!/bin/bash",
        "export TERM=linux",
        'echo -e "\\033[2J\\033[H"',
        f'echo "{STUDENTS}"',
        'echo "--------------------------------------------------------------------------------"'
    ]
    
    for cmd in commands:
        script_lines.append(f'echo "ubuntu@ubuntu-vm:~$ {cmd}"')
        script_lines.append(cmd)
        script_lines.append('echo ""')
        
    script_lines.append('echo "--------------------------------------------------------------------------------"')
    script_lines.append(f'echo "{STUDENTS}"')
    
    script_content = "\n".join(script_lines) + "\n"
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("127.0.0.1", port=2222, username="ubuntu", key_filename=KEY_PATH, timeout=20)
    
    sftp = client.open_sftp()
    with sftp.file('/tmp/task_sec03.sh', 'w') as f:
        f.write(script_content)
    sftp.close()
    
    exec_cmd = 'chmod +x /tmp/task_sec03.sh && /tmp/task_sec03.sh 2>&1 | sudo tee /dev/tty1'
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
    
    # 03.1 Actualización de paquetes e instalación de herramientas base
    print("\nActualizando repositorios e instalando paquetes base...")
    run_step(
        "Seccion 03 - Actualizacion e instalacion de herramientas base",
        [
            "sudo apt update -y",
            "sudo apt install -y curl wget git pciutils lshw htop net-tools",
            "which curl wget git htop netstat"
        ],
        "Sec03_01_Instalacion_Herramientas.png",
        timeout=600
    )

    # 03.2 Instalación de Ollama mediante script oficial
    print("\nInstalando Ollama en Ubuntu...")
    run_step(
        "Seccion 03 - Instalacion de Ollama",
        [
            "curl -fsSL https://ollama.com/install.sh | sh",
            "ollama -v",
            "which ollama"
        ],
        "Sec03_02_Instalacion_Ollama.png",
        timeout=600
    )

    # 03.3 Verificación del servicio systemd y API REST local
    print("\nVerificando servicio y API REST...")
    run_step(
        "Seccion 03 - Verificacion de Servicio y API Local",
        [
            "sudo systemctl enable --now ollama",
            "systemctl status ollama --no-pager",
            "curl -s http://127.0.0.1:11434/api/tags"
        ],
        "Sec03_03_Servicio_API_Tags.png",
        timeout=120
    )

    print("\nSeccion 03 finalizada exitosamente.")
    print(STUDENTS)
