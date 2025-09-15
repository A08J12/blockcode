from mcrcon import MCRcon
import init
import re
ip = init.config("minecraft.ip")
port = init.config("minecraft.port")
passeword = init.config("minecraft.passeword")
def mc(cmd: str,prints = False, host=ip, port=port, password="blockcode"):
    try:
        with MCRcon(host, password, port) as mcr:
            repon = mcr.command(cmd)  # envoie la commande
            if prints:
                print(repon)
            if "facing" in repon:
                mc(str(re.sub(r"\[.*?\]", "", cmd).strip()))
    except Exception as e:
        print(f"Erreur RCON: {e}")
def init():
    mc("say yo j'éxécute")