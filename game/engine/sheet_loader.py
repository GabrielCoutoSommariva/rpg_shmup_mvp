# game/engine/sheet_loader.py
import arcade

def load_grid_textures(png_path: str, _json_path: str = None,
                       frame_w: int = 32, frame_h: int = 32,
                       cols: int = 4, rows: int = 3):
    """
    Carrega uma spritesheet em grade (cols × rows) e retorna um dicionário
    com listas de textures por direção. Compatível com Arcade 3.x.
    A assinatura mantém o 2º argumento (json) por compatibilidade, mas é ignorado.
    """
    try:
        # Arcade 3.x costuma aceitar (file, w, h, cols, rows)
        textures = arcade.load_spritesheet(png_path, frame_w, frame_h, cols, rows)
    except TypeError:
        # Fallback para assinaturas antigas: (file, w, h, cols, count)
        textures = arcade.load_spritesheet(png_path, frame_w, frame_h, cols, cols * rows)

    # Mapeamento por linha (ajuste se sua ordem for diferente)
    south = textures[0:4]    # linha 0
    east  = textures[4:8]    # linha 1
    west  = textures[8:12]   # linha 2
    # Se adicionar "north" (4ª linha), inclua: north = textures[12:16]

    return {
        "south": south,
        "east":  east,
        "west":  west,
        # "north": north,  # quando tiver a 4ª linha
    }, (frame_w, frame_h)
