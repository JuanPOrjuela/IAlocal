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

def run_step(title, commands, screenshot_filename, sleep_delay=2.0, timeout=120):
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
    with sftp.file('/tmp/task_sec04.sh', 'w') as f:
        f.write(script_content)
    sftp.close()
    
    exec_cmd = 'chmod +x /tmp/task_sec04.sh && /tmp/task_sec04.sh 2>&1 | sudo tee /dev/tty1'
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
    
    # 04.1 Administracion del servicio Ollama
    run_step(
        "Seccion 04 - Administracion de servicio y logs journalctl",
        [
            "sudo systemctl restart ollama",
            "systemctl status ollama --no-pager | head -n 12",
            "journalctl -u ollama -n 8 --no-pager"
        ],
        "Sec04_01_Servicio_Restart_Logs.png"
    )

    # 04.2 Administracion de red y socket puerto 11434
    run_step(
        "Seccion 04 - Red y Puerto 11434",
        [
            "ss -lntp | grep 11434",
            "curl -s http://127.0.0.1:11434/api/tags",
            "ip -4 addr show enp0s3 | grep inet"
        ],
        "Sec04_02_Red_Puerto11434.png"
    )

    # 04.3 Medicion de recursos en reposo (Baseline RAM)
    run_step(
        "Seccion 04 - Medicion de Recursos en Reposo",
        [
            "free -h",
            "ps aux --sort=-%mem | head -n 10",
            "pgrep -a ollama"
        ],
        "Sec04_03_Recursos_Reposo.png"
    )

    print("\nSeccion 04 finalizada exitosamente.")
    print(STUDENTS)
