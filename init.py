import rcon
def init_map(t, max_blocs=32768):
    t = t-1
    x = t+1
    y = t+1
    z = t+1
        # taille max d'une dimension pour ne pas dépasser max_blocs
    max_size = int(round(max_blocs ** (1/3)))

    for xi in range(-2, x + 2, max_size):
        for yi in range(-2, y + 2, max_size):
            for zi in range(-2, z + 2, max_size):
                x_end = min(x + 1, xi + max_size - 1)
                y_end = min(y + 1, yi + max_size - 1)
                z_end = min(z + 1, zi + max_size - 1)
                rcon.mc(f"fill {xi} {yi} {zi} {x_end} {y_end} {z_end} air",)

    rcon.mc(f"fill -1 -1 -1 64 -1 255 barrier")
    rcon.mc(f"fill 64 -1 -1 128 -1 255 barrier")
    rcon.mc(f"fill 128 -1 -1 192 -1 255 barrier")
    rcon.mc(f"fill 192 -1 -1 256 -1 255 barrier")
    # Arêtes X
    rcon.mc(f"fill -1 -1 -1 {x} -1 -1 quartz_block")
    rcon.mc(f"fill -1 {y} -1 {x} {y} -1 quartz_block")
    rcon.mc(f"fill -1 -1 {z} {x} -1 {z} quartz_block")
    rcon.mc(f"fill -1 {y} {z} {x} {y} {z} quartz_block")
    # Arêtes Y
    rcon.mc(f"fill -1 -1 -1 -1 {y} -1 quartz_block")
    rcon.mc(f"fill {x} -1 -1 {x} {y} -1 quartz_block")
    rcon.mc(f"fill -1 -1 {z} -1 {y} {z} quartz_block")
    rcon.mc(f"fill {x} -1 {z} {x} {y} {z} quartz_block")

    # Arêtes Z
    rcon.mc(f"fill -1 -1 -1 -1 -1 {z} quartz_block")
    rcon.mc(f"fill {x} -1 -1 {x} -1 {z} quartz_block")
    rcon.mc(f"fill -1 {y} -1 -1 {y} {z} quartz_block")
    rcon.mc(f"fill {x} {y} -1 {x} {y} {z} quartz_block")
    rcon.mc("kill @e[type=!minecraft:player]")
def config(key):
    filename = "C:/blockcode/blockcode.config"
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"')

            if k == key:  # correspondance exacte 🐱
                if v.isdigit():
                    return int(v)
                return v