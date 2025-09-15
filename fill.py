import os
import json

# répertoire du script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def fill(qui):
    """
    retourner la list 'qui' présent dans le json
    input : (qui)
    output : (list)
    """
    chemin = os.path.join(SCRIPT_DIR, f"{qui}.json")
    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
