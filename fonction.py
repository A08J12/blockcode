import rcon
import block
from fill import fill
import init
import os
def getBlockInfo(x, y, z, maps):
    """
    obtenir les informations dans le block à la position (x, y, z)
    input : (x, y, z, maps)
    output : (valeur présente dans le block)
    """
    # vérifier que le block éxiste
    if (x, y, z) in maps:
        return maps.get((x, y, z))[3]
    else:
        return 0
#['block',direction,(information recue),'information a donner']
def execute_block(x,y,z,maps,minecraft):
    """
    exécuter le block à la position (x, y, z)
    input : (x, y, z, maps)
    output : (maps)
    """
    if (x, y, z) in maps:
        info_block = fill(f"block/{maps[(x, y, z)][0]}")
        bl = (x,y,z)
        maps_c = maps.copy()
        rep,comp,maps = getattr(block, info_block["execute"])(bl, maps)
        if maps_c.keys() != maps.keys() and minecraft:
            #posser 
            for i in [i for i in maps.keys() if i not in maps_c.keys()]:
                rcon.mc(f"setblock {i[0]} {i[1]} {i[2]} {maps[i][0]}[facing={['east', 'west', 'up', 'down', 'south', 'north'][maps[i][1]]}]")
            for i in [i for i in maps_c.keys() if i not in maps.keys()]:
                rcon.mc(f"setblock {i[0]} {i[1]} {i[2]} air")
        maps[(x, y, z)][3] = int(rep%256) if type(rep) == int else rep
        maps[(x, y, z)][4] = comp
    return maps
def send(x, y, z, info,maps,minecraft):
    """
    envoyer les informations au block x y z
    input : (x, y, z, info)
    output : (None)
    """
    if (x, y, z) in maps:
        info_block = fill(f"block/{maps[(x, y, z)][0]}")
        if type(info_block["send"]) != list:
            a, b = map(int, info_block["send"].split(","))
            if not a < len(info) <= b:
                raise ValueError("Les éléments de la liste info ne correspondent pas aux blocs connus.")
        else:
            if not len(info_block["send"]) == len(info):
                raise TypeError("Les types des éléments de la liste info ne correspondent pas à ceux attendus.")
        block = fill("block")
        if 1 in [1 for i in [i for i in info if type(i) == str] if i not in block ]:
            raise ValueError(f"Les éléments de la liste info ne correspondent pas aux blocs connus : {[i for i in [i for i in info if type(i) == str] if i not in block ]}")
        maps[(x, y, z)][2] = [i%256 if type(i) == int else i for i in info]
        maps = execute_block(x, y, z, maps,minecraft)
def setblock( block, x, y, z, direction, maps,minecraft):
    """
    poser un block à la position (x, y, z) avec une direction donnée
    input : (x, y, z, direction, block, maps)
    output : (maps)
    """
    if block not in fill("block"):
        raise ValueError(f"Block inconnu : {block}")
    if block == "air":
        maps.pop((x, y, z), None)
        if minecraft:
            rcon.mc(f"setblock {x} {y} {z} air")
    else:
        maps[(x, y, z)] = [block, direction,0,0,0]
        if minecraft:
            rcon.mc(f"setblock {x} {y} {z} {block}[facing={['east', 'west', 'up', 'down', 'south', 'north'][direction]}]")
    if fill(f"block/{block}")["start"]:
        maps = execute_block(x, y, z, maps,minecraft)
    return maps
def return_operation(n,x,pointeur):
    """
    aller à l'opération + x
    input : (n, x, pointeur)
    output : (pointeur + x)
    """
    if n == 0:
        return pointeur + x
    elif n == 1:
        return pointeur - x
    else:
        raise TypeError(f"n n'est pas un booléen de la commande return {n} {x}")
def readFile(file):
    """
    lire le fichier et retourner le code
    input : (file)
    output : (code)
    """
    try:
        with open(file, "r") as f:
            code = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {file}")
    return code


def cleanCode(code):
    """
    nétoyer le code
    input : (code)
    output : (code)
    """
    code = code.replace("\n", "") # retirer les entré pour n'avoir qu'une ligne
    hashtag = False

    # gestion des commentaires
    ncode = ""
    for t in code:
        if t == "#":
            hashtag = not hashtag
            continue
        if not hashtag:
            ncode += t

    code = ncode.split(";") #séparer les commandes par le ;
    
    code = [c.strip() for c in code if c != ""] #retirer les espaces devant et derrière et les commandes vides
    code = [c for c in code if c != ""]
    return code

# sépare les éléments d'une seule ligne

def tokeniseLine(line: str):
    """
    Tokeniser le code
    input : (line of code)
    output : (return tokenized line code in a list)
    """

    # Vérifie l'équilibre des parenthèses
    if line.count('(') != line.count(')'):
        raise SyntaxError("Trop de ( ou ) dans la ligne.")

    code = []
    l = line.split(" ")
    inGetBlock = False
    depth = 0

    for word in l:
        if not word:  # saute les vides
            continue

        if not inGetBlock:
            if word.isdigit():
                code.append(int(word))
            elif word[0] == '(':
                # Début d’un bloc
                word = word[1:]
                if not word:  
                    code.append([])
                elif word[0] == '(':
                    depth = word.count('(')
                    code.append([word + ' '])
                else:
                    if word.isdigit():
                        code.append([int(word)])
                    else:
                        code.append([word])
                inGetBlock = True
            else:
                code.append(word)
        else:
            # Dans un bloc
            if word[0] == '(':
                if depth == 0:
                    code[-1].append("")
                depth += word.count('(')

            if word[-1] == ')':
                nword = word.rstrip(")")
                if depth == 0:
                    if nword.isdigit():
                        code[-1].append(int(nword))
                    elif nword:
                        code[-1].append(nword)
                    inGetBlock = False
                else:
                    depth -= word.count(')')
                    if depth < 0:
                        inGetBlock = False
                    code[-1][-1] += nword + ") "
            else:
                if depth == 0:
                    if word.isdigit():
                        code[-1].append(int(word))
                    else:
                        code[-1].append(word)
                else:
                    code[-1][-1] += word + " "

    # Post-traitement récursif
    for i in range(len(code)):
        if isinstance(code[i], list):
            for subi in range(len(code[i])):
                if isinstance(code[i][subi], str) and code[i][subi].startswith("("):
                    code[i][subi] = tokeniseLine(code[i][subi])[0]

    return code


def tokenise(code: list):
    """
    Tokeniser plusieurs lignes
    """
    code = [tokeniseLine(line) for line in code]
    return code


def executeGet(getLists, maps):
    """
    Transforme un get tokénisé [x, y, z] en la valeur réelle du bloc aux coordonnées (x, y, z)
    fonction s'appelle elle même pour résoudre les get imbriqués
    input : getList : list
            maps : dict
    output : value of the block as an integer
    """
    if not isinstance(getLists, list):
        return getLists
    getList = getLists.copy()
    if len(getList) != 3:
        raise SyntaxError("Liste ne contient pas 3 éléments.")
        exit()
    
    for i in range(3):
        if isinstance(getList[i], list):
            getList[i] = executeGet(getList[i], maps)
        elif not isinstance(getList[i], int):
            raise SyntaxError("Type incompatible pour un get.")
            exit()
    return getBlockInfo(getList[0], getList[1], getList[2], maps)

def instructions(pointeur,ligne_code,maps,iteration,pr,minecraft,chemin_code):
    """
    executer l'instruction donner
    input : pointeur, ligne de code, maps, minecraft
    output : none
    """
    instruction = [executeGet(i,maps) for i in ligne_code] #trouver les valeurs
    if init.config("debug.instruction") == "True" :
        print(f"({pr})"," ".join(map(str, ligne_code))," -> "," ".join(map(str, instruction)))
    if instruction[0] == "block": #block <block> <x> <y> <z> <direction>
        if len(instruction) < 5 :
            raise SyntaxError(f"pas asser de donner sur la commande {" ".join(map(str, instruction))}")
        maps = setblock(instruction[1], instruction[2], instruction[3], instruction[4], instruction[5], maps, minecraft)
    elif instruction[0] == "return": #return <n> <x>
        pointeur = return_operation(instruction[1], instruction[2], pointeur) - 1
    elif instruction[0] == "send": #send <x> <y> <z> <info>
        send(instruction[1], instruction[2], instruction[3], instruction[4:], maps,minecraft)
    elif instruction[0] == "if": #if <b> <commande>
        if instruction[1] == 1:
            interation,pointeur, maps = instructions(pointeur, instruction[2:], maps,iteration,pr,minecraft,chemin_code)
    elif instruction[0] == "fill":
        pointeur_me = 0
        pointeur_save = pointeur
        code = readFile(os.path.join(chemin_code, f"{instruction[1]}.bcd"))
        code = cleanCode(code)
        code = tokenise(code)
        while pointeur_me < len(code):
            iteration,pointeur_me, maps = instructions(pointeur_me,code[pointeur_me],maps,iteration,instruction[1],minecraft,chemin_code)
            pointeur_me += 1
            iteration += 1
        pointeur = pointeur_save
    else:
        raise SyntaxError("Instruction inconnue.")
    return iteration,pointeur, maps