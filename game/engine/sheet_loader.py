# game/engine/sheet_loader.py (Arcade 3.x)
import os, json, arcade

def load_grid_textures(png_path: str, json_path: str):
    """
    Retorna um dicionário com listas de textures por direção.
    Suposição do JSON: grid 4 colunas × 3 linhas; ordem das linhas:
      0=sul, 1=leste, 2=oeste (ajuste se seu sheet tiver outra ordem).
    """
    meta = json.load(open(json_path, "r", encoding="utf-8"))
    w, h = meta["normalized_size"]
    cols = meta["grid"]["cols"]
    rows = meta["grid"]["rows"]

    def tex(ix: int):
        fr = meta["frames"][f"frame_{ix}"]
        return arcade.load_texture(
            png_path, x=fr["x"], y=fr["y"], width=w, height=h
        )

    # fatia por linhas
    south = [tex(i) for i in range(0, 4)]
    east  = [tex(i) for i in range(4, 8)]
    west  = [tex(i) for i in range(8, 12)]
    # se você tiver a linha “north”, troque o sheet para 4×4; por enquanto usamos 3 linhas.

    return {
        "south": south,  # [0..3]
        "east":  east,
        "west":  west,
        # opcional: "north": north
    }, (w, h)
