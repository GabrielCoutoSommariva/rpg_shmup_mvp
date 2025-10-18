# game/features/arena/player.py
import arcade
from dataclasses import dataclass, field

@dataclass
class Player:
    sprite: arcade.Sprite
    speed: float = 220
    dash_speed: float = 480
    dash_cooldown: float = 1.0
    dash_time: float = 0.12
    dash_timer: float = 0.0
    dash_cd_timer: float = 0.0
    hp: int = 5

    # --- animação ---
    animations: dict = field(default_factory=dict)  # {"south":[textures], "east":[...], "west":[...]}
    frame_index: int = 0
    frame_time: float = 0.0
    frame_rate: float = 0.15        # troca a cada 0.15s
    facing: str = "south"           # direção atual
    is_moving: bool = False

    def set_animations(self, anims: dict):
        """Passe o dicionário retornado pelo loader (direção -> lista de textures)."""
        self.animations = anims
        # textura inicial
        if "south" in anims and anims["south"]:
            self.sprite.texture = anims["south"][0]

    def set_facing_from_vec(self, mx: float, my: float):
        # Decide direção com base no input; simples (3 direções)
        if abs(mx) > abs(my):
            self.facing = "east" if mx > 0 else "west"
        else:
            self.facing = "south"   # se não tiver “north”, padronize pra south

    def update_anim(self, dt: float):
        if not self.animations:
            return
        frames = self.animations.get(self.facing, [])
        if not frames:
            return
        # idle usa frame 0; walk usa [1..3] se estiver andando
        if self.is_moving and len(frames) >= 4:
            self.frame_time += dt
            if self.frame_time >= self.frame_rate:
                self.frame_time = 0.0
                # ciclo entre 1,2,3
                if self.frame_index < 1 or self.frame_index > 3:
                    self.frame_index = 1
                else:
                    self.frame_index += 1
                    if self.frame_index > 3:
                        self.frame_index = 1
        else:
            self.frame_index = 0
            self.frame_time = 0.0
        self.sprite.texture = frames[self.frame_index]

    def update(self, dt, move_x, move_y, bounds):
        # movimento / dash (igual ao seu)
        if self.dash_timer > 0:
            self.dash_timer -= dt
            mult = self.dash_speed
        else:
            mult = self.speed

        self.sprite.center_x += move_x * mult * dt
        self.sprite.center_y += move_y * mult * dt
        self.sprite.center_x = max(bounds[0], min(bounds[1], self.sprite.center_x))
        self.sprite.center_y = max(bounds[2], min(bounds[3], self.sprite.center_y))

        if self.dash_cd_timer > 0:
            self.dash_cd_timer -= dt

        # estado de movimento + direção + animação
        self.is_moving = (abs(move_x) + abs(move_y)) > 0.01
        self.set_facing_from_vec(move_x, move_y)
        self.update_anim(dt)

    def can_dash(self):
        return self.dash_cd_timer <= 0

    def start_dash(self):
        self.dash_timer = self.dash_time
        self.dash_cd_timer = self.dash_cooldown
