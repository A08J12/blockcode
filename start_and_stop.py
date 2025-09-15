import subprocess
import psutil
import os
import requests
import shutil

# 🐾 Paramètres par défaut
VERSION = "1.21.8"
JAR_NAME = "server.jar"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(SCRIPT_DIR, "server")
LOG_FILE = os.path.join(SERVER_DIR, "server.log")

# Mémoire allouée
XMX = "1G"
XMS = "1G"

# -----------------------------------
# Fonction pour obtenir le lien du server.jar depuis le manifest officiel
# -----------------------------------
def get_server_jar_url(version=VERSION):
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest = requests.get(manifest_url).json()

    # Trouve la version désirée
    version_info = next((v for v in manifest["versions"] if v["id"] == version), None)
    if not version_info:
        raise ValueError(f"Version {version} non trouvée dans le manifest ! 😿")

    version_json = requests.get(version_info["url"]).json()
    return version_json["downloads"]["server"]["url"]

# -----------------------------------
# Téléchargement du serveur Minecraft
# -----------------------------------
def telecharger_minecraft(version=VERSION, server_dir=SERVER_DIR):
    os.makedirs(server_dir, exist_ok=True)
    
    jar_path = os.path.join(server_dir, JAR_NAME)
    json_path = os.path.join(server_dir, "server.jar")
    
    if not os.path.exists(json_path):
        print(f"😺 server.json introuvable, téléchargement de server.jar Minecraft {version} ... 🐱")
        
        url = get_server_jar_url(version)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(jar_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("😸 Téléchargement terminé !")
    else:
        print("😺 server.json existe déjà, téléchargement annulé.")

# -----------------------------------
# Vérifie si le serveur tourne déjà
# -----------------------------------
def find_server_process():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and "java" in cmdline[0].lower() and JAR_NAME in " ".join(cmdline):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

# -----------------------------------
# Lancer le serveur
# -----------------------------------
def start():
    # Vérification de Java
    if not shutil.which("java"):
        print("😿 Java non trouvé ! Installez Java avant de lancer le serveur.")
        return

    telecharger_minecraft()
    
    if find_server_process():
        print("😺 Le serveur tourne déjà !")
        return

    cmd = ["java", f"-Xmx{XMX}", f"-Xms{XMS}", "-jar", JAR_NAME, "nogui"]
    
    with open(LOG_FILE, "a") as log_file:
        subprocess.Popen(
            cmd,
            cwd=SERVER_DIR,
            stdin=subprocess.PIPE,
            stdout=log_file,
            stderr=log_file,
            text=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    
    print("🐾 Serveur Minecraft lancé ! Les logs sont dans server/server.log 😸")

# -----------------------------------
# Arrêter le serveur
# -----------------------------------
def stop():
    proc = find_server_process()
    if not proc:
        print("😿 Aucun serveur trouvé.")
        return

    try:
        proc.terminate()
        proc.wait(timeout=10)
        print("🐾 Serveur arrêté !")
    except psutil.TimeoutExpired:
        proc.kill()
        print("😼 Serveur tué de force.")


