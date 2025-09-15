from fill import fill
import random
import rcon
def stonecutter(bl,maps):
    """
    renvois la corespondance d'un nombre en block
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    f = fill('block')
    reps = 1
    if len(f) < info[2][0]: 
        reps = 0
    rep = f[info[2][0]]
    return reps,rep,maps
def anvil(bl,maps):
    """
    faire une adition
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][0] + info[2][1],0,maps
def decorated_pot(bl,maps):
    """
    stocker une valeur de 0 a 255 avec la corespondance d'un block
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][1],info[2][0],maps
def furnace(bl,maps):
    """
    faire une soustraction
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][0]-info[2][1],0,maps
def brewing_stand(bl,maps):
    """
    faire une division
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][1] // info[2][0],0,maps
def crafter(bl,maps):
    """
    faire une multiplication
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][1] * info[2][0],0,maps
def grindstone(bl,maps):
    """
    renvois la corespondance d'un block en nombre
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    f = fill('block') 
    if info[2][0] in f:
        rep = f.index(info[2][0])
    else:
        raise IndexError(f"le block {info[2][0]} n'est pas connu.")
    return rep,0,maps
def bookshelf(bl,maps):
    """
    retourne l'id du block qui est le plus haut dans la list des blocks
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return len(fill('block'))-1,0,maps
def white_wool(bl,maps):
    """
    retourner 1 si nombre 1 = nombre 2 else 0
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return 1 if info[2][0] == info[2][1] else 0,0,maps
def black_wool(bl,maps):
    """
    retourner 1 si nombre 1 > nombre 2 else 0
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return 1 if info[2][0] > info[2][1] else 0,0,maps
def red_wool(bl,maps):
    """
    retourner l'inverse d'un nombre
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    if info[2][0] == 1:
        return 0,0,maps
    else:
        return 1,0,maps
def blue_wool(bl,maps):
    """
    xor
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][0] ^ info[2][1],0,maps
def green_wool(bl,maps):
    """
    and
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][0] & info[2][1],0,maps
def yellow_wool(bl,maps):
    """
    or
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    return info[2][0] | info[2][1],0,maps
def sculk_sensor(bl,maps):
    """
    retourner la valeur du de l'utilisateur (nombre)
    input : (info,maps)
    output : (donner)
    """
    return int(input("entre un nombre : ")),0,maps
def calibrated_sculk_sensor(bl,maps):
    """
    retourner la valeur du de l'utilisateur (block)
    input : (info,maps)
    output : (donner)
    """
    f = fill('block') 
    rep = input("entre un block : ")
    if rep in f:
        rep = f.index(rep)
    else:
        raise IndexError(f"le block {rep} n'est pas connu.")
    return rep,0,maps
def oak_trapdoor(bl,maps):
    """
    stocker une valeur de 0 a 1
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    if info[2][0] == 1:
        rcon.mc(f"setblock {bl[0]} {bl[1]} {bl[2]} oak_trapdoor[open=true]")
    return int(bool(info[2][0])),0,maps
def crafting_table(bl,maps):
    """
    afficher le contenu de la table de craft
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    if info[2][1] == 1:
        print(info[2][0],end="")
    else:
        print(info[2][0])
    return 0,0,maps
def observer(bl,maps):
    """
    0 = [1 0 0] 1 = [-1 0 0] 2 = [0 1 0] 3 = [0 -1 0] 4 = [0 0 1] 5 = [0 0 -1]
    donner le block devant l'observateur
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    direction = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]][info[1]]
    if (direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2]) in maps:
        return 1,maps[(direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2])][0],maps
    return 0,"air",maps
def comparator(bl,maps):
    """
    donner le block présent dans le block devant lui
    input = (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    direction = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]][info[1]]
    if (direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2]) in maps:
        return maps[(direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2])][-1],0,maps
    else:
        return 0,"air",maps
def lectern(bl,maps):
    """
    afficher le contenu de la table de craft
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    print(chr(info[2][0]),end="")
    return 0,0,maps
def dropper(bl,maps):
    """
    donner un nombre aléatoire
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl][2].copy()
    return random.randint(info[0],info[1]),0,maps
def dispenser(bl,maps):
    """
    choisir un block et le posser devant
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    if 1 in [1 for i in info[2] if type(i) != str]:
        raise TypeError("Les types des éléments de la liste info ne correspondent pas à ceux attendus.")
    direction = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]][info[1]]
    if (direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2]) in maps:
        return 0,0,maps
    else:
        blo = random.choice(info[2])
        if not blo == "air":
            maps[(direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2])] = [blo, info[1], 0, 0, 0]
    return blo,0,maps
def piston(bl,maps):
    """
    pousser des block minecraft
    input : (info,maps)
    output : (donner)
    """
    info = maps[bl].copy()
    direction = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]][info[1]]
    n = 1
    block = []
    while n>0 :
        prochain_block = (direction[0]*n+bl[0], direction[1]*n+bl[1], direction[2]*n+bl[2])
        n_position = (direction[0]*(n+1)+bl[0], direction[1]*(n+1)+bl[1], direction[2]*(n+1)+bl[2])
        if prochain_block in maps:
            n += 1
            block.append((n_position,maps[prochain_block]))
        else:
            n = 0
    if len(block) > 0:
        for b in block:
            maps[b[0]] = b[1]
    maps.pop((direction[0]+bl[0], direction[1]+bl[1], direction[2]+bl[2]))
    return 0,0,maps
def tnt(bl,maps):
    """
    détruire des block dans un cube donner
    input : (info,maps)
    output : (donner)
    """
    block = maps[bl][2][0]
    cube = maps[bl][2][1]
    count  = 0
    for x in range(bl[0]-cube,bl[0]+cube):
        for y in range(bl[1]-cube,bl[1]+cube):
            for z in range(bl[1]-cube,bl[1]+cube):
                if (x,y,z) in maps:
                    if maps[(x,y,z)][0] == block:
                        count += 1
                        del maps[(x,y,z)]
    return count,block,maps