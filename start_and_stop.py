import subprocess
import psutil
import os

JAR_NAME = "server.jar"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 🐱 dossier du script
SERVER_DIR = os.path.join(SCRIPT_DIR, "server")  # 🐾 chemin absolu du serveur

def find_server_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and "java" in cmdline[0].lower() and JAR_NAME in " ".join(cmdline):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def start():
    if find_server_process():
        print("😺 Le serveur tourne déjà !")
        return

    cmd = ["java", "-Xmx1G", "-Xms1G", "-jar", JAR_NAME, "nogui"]
    subprocess.Popen(
        cmd,
        cwd=SERVER_DIR,
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # important sous Windows
    )
    print("🐾 Serveur Minecraft lancé !")

def stop():
    proc = find_server_process()
    if not proc:
        print("😿 Aucun serveur trouvé.")
        return

    try:
        proc.terminate()  # tente un arrêt propre
        proc.wait(timeout=10)
        print("🐾 Serveur arrêté !")
    except psutil.TimeoutExpired:
        proc.kill()
        print("😼 Serveur tué de force.")
