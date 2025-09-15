import sys
from fonction import *
import init
import os
if len(sys.argv) not in  [2,3]:
    print("Usage: blockcode <fichier.bcd>")
    exit()
if len(sys.argv) == 3:
    minecraft = True if sys.argv[2] == "minecraft" else False
else:
    minecraft = False
if minecraft == True and init.config("minecraft.map.init") == "True":
    print("initialisation de la map ...")
    init.init_map(init.config("minecraft.map"))
if sys.argv[1] == "start" :
    import start_and_stop
    start_and_stop.start()
    exit()
elif sys.argv[1] == "stop":
    import start_and_stop
    start_and_stop.stop()
    exit()
chemin_code = os.path.dirname(os.path.abspath(sys.argv[1]))
code = readFile(sys.argv[1])
code = cleanCode(code)
code = tokenise(code)
print("code recuperé et éxécuter : ")
maps = {} #création de la map
pointeur = 0
iteration = 0
while pointeur < len(code):
    iteration,pointeur, maps = instructions(pointeur,code[pointeur],maps,iteration,"base",minecraft,chemin_code)
    pointeur += 1
    iteration += 1
if init.config("debug.map") == "True":
    print(maps)
    print("pointeur : ",pointeur)
print(f"fin de l'éxécution après {iteration} itérations")