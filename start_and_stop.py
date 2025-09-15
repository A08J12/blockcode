import subprocess
import psutil
import os
import requests

JAR_NAME = "server.jar"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # 🐱 dossier du script
SERVER_DIR = os.path.join(SCRIPT_DIR, "server")  # 🐾 chemin absolu du serveur
os.makedirs(SERVER_DIR, exist_ok=True)

# Miaou 😹 : URL du serveur Minecraft 1.21.8
MINECRAFT_URL = "https://launcher.mojang.com/v1/objects/9c85f1b9ad0c6325a70c2c19b2e1f15d34b9a5c2/server.jar"

# 🐾 Télécharger server.jar si nécessaire
def download_server():
    jar_path = os.path.join(SERVER_DIR, JAR_NAME)
    if not os.path.exists(jar_path):
        print("🐾 server.jar introuvable, téléchargement en cours...")
        response = requests.get(MINECRAFT_URL, stream=True)
        with open(jar_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("✅ server.jar téléchargé !")
    else:
        print("😺 server.jar déjà présent.")

# 🐾 Vérifie si le serveur tourne
def find_server_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and "java" in cmdline[0].lower() and JAR_NAME in " ".join(cmdline):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

# 🐱 Lancer le serveur
def start():
    download_server()  # 🐾 assure que server.jar est là
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

# 🐱 Arrêter le serveur
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

# 🐱 Commande principale
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage : python script.py start|stop")
    elif sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "stop":
        stop()
    else:
        print("Commande inconnue 😿")
