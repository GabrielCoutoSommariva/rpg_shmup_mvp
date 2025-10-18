import arcade, math, os
from engine.scene_manager import SceneManager
from engine.eventbus import global_bus
from engine.rng import RNG
from features.hub.map_loader import HubMap
from features.hub.portal import Portal
from features.arena.player import Player
from features.arena.enemy import Enemy
from features.arena.patterns import make_bullets
from features.arena.wave_spawner import WaveSpawner
from features.arena.ui_arena import draw_hud
from engine.sheet_loader import load_grid_textures

DATA = os.path.join(os.path.dirname(__file__), "data")
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
WIN_W, WIN_H = 800, 600

class HubView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.scene = SceneManager(window)
        self.map = HubMap(WIN_W, WIN_H)

        # Hub usa um marcador simples para o player (sem animação)
        self.player = arcade.SpriteSolidColor(24, 24, arcade.color.BRIGHT_LILAC)
        self.player.center_x, self.player.center_y = 80, 120

        self.portal = Portal(740, 140)
        self.speed = 220

        # Draw compatível
        self.hub_sprites = arcade.SpriteList()
        self.hub_sprites.append(self.player)
        self.hub_sprites.append(self.portal)

    def on_draw(self):
        self.clear()
        self.map.draw()
        self.hub_sprites.draw()

    def on_update(self, dt):
        keys = self.window.pressed_keys
        mx = my = 0
        if arcade.key.W in keys: my += 1
        if arcade.key.S in keys: my -= 1
        if arcade.key.A in keys: mx -= 1
        if arcade.key.D in keys: mx += 1
        if mx or my:
            mag = (mx*mx + my*my) ** 0.5
            self.player.center_x += (mx/mag)*self.speed*dt
            self.player.center_y += (my/mag)*self.speed*dt

        if arcade.check_for_collision(self.player, self.portal):
            self.scene.go(ArenaView(self.window))

    def on_key_press(self, symbol, modifiers): self.window.pressed_keys.add(symbol)
    def on_key_release(self, symbol, modifiers): self.window.pressed_keys.discard(symbol)


class ArenaView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.scene = SceneManager(window)
        self.bounds = (40, WIN_W-40, 40, WIN_H-40)  # left,right,bottom,top

        # ===== PLAYER COM ANIMAÇÃO =====
        # Cria sprite vazio (vamos setar a texture via sheet)
        self.player = Player(arcade.Sprite())
        self.player.sprite.center_x, self.player.sprite.center_y = 120, 300

        # Carrega spritesheet 4x3 (sul, leste, oeste) e injeta na classe Player
        png = os.path.join(ASSETS, "sprites", "player", "anim_sheet_32x32_4x3.png")
        jsn = os.path.join(ASSETS, "sprites", "player", "anim_sheet_32x32_4x3.json")
        try:
            anims, (fw, fh) = load_grid_textures(png, jsn)
            self.player.set_animations(anims)
            # Escala opcional (1.25x) — ajuste se quiser maior/menor
            self.player.sprite.scale = 1.0
        except Exception as e:
            # Fallback visível caso assets não estejam disponíveis
            self.player.sprite = arcade.SpriteSolidColor(20, 20, arcade.color.SPRING_BUD)
            self.player.sprite.center_x, self.player.sprite.center_y = 120, 300
            print("[WARN] Falha ao carregar sheet do player:", e)

        # ===== RESTANTE =====
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.time = 0.0
        self.wave = WaveSpawner(os.path.join(DATA, "waves.json"))
        self.rng = RNG(42)
        self.upgrades = []
        self._setup_lists()

    def _setup_lists(self):
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player.sprite)
        self.enemy_sprite_list = arcade.SpriteList()
        self.bullet_sprite_list = arcade.SpriteList()
        self.enemy_bullet_sprite_list = arcade.SpriteList()

    def on_draw(self):
        self.clear()
        l, r, b, t = self.bounds
        arcade.draw_lrbt_rectangle_outline(l, r, b, t, arcade.color.WHITE, 2)
        self.player_sprite_list.draw()
        self.enemy_sprite_list.draw()
        self.bullet_sprite_list.draw()
        self.enemy_bullet_sprite_list.draw()
        draw_hud(self.player.hp, max(0, 90 - self.time), self.upgrades)

    def on_update(self, dt):
        self.time += dt

        # Input de movimento
        keys = self.window.pressed_keys
        mx = my = 0
        if arcade.key.W in keys: my += 1
        if arcade.key.S in keys: my -= 1
        if arcade.key.A in keys: mx -= 1
        if arcade.key.D in keys: mx += 1
        mag = (mx*mx + my*my) ** 0.5 or 1.0
        self.player.update(dt, mx/mag, my/mag, self.bounds)

        # Tiro (mouse esquerdo pressionado)
        if arcade.MOUSE_BUTTON_LEFT in self.window.pressed_mouse:
            px, py = self.player.sprite.center_x, self.player.sprite.center_y
            mxp, myp = self.window.mouse_xy
            angle = math.degrees(math.atan2(myp - py, mxp - px))
            for x, y, vx, vy in make_bullets("straight", (px, py), 300, angle=angle):
                spr = arcade.SpriteSolidColor(4, 4, arcade.color.YELLOW)
                spr.center_x, spr.center_y = x, y
                self.bullet_sprite_list.append(spr)
                self.bullets.append((spr, vx, vy))

        # Atualização de projéteis (método safe rebuild)
        new_bullets = []
        for spr, vx, vy in self.bullets:
            spr.center_x += vx * dt
            spr.center_y += vy * dt
            if 0 <= spr.center_x <= WIN_W and 0 <= spr.center_y <= WIN_H:
                new_bullets.append((spr, vx, vy))
            else:
                spr.remove_from_sprite_lists()
        self.bullets = new_bullets

        new_enemy_bullets = []
        for spr, vx, vy in self.enemy_bullets:
            spr.center_x += vx * dt
            spr.center_y += vy * dt
            if 0 <= spr.center_x <= WIN_W and 0 <= spr.center_y <= WIN_H:
                new_enemy_bullets.append((spr, vx, vy))
            else:
                spr.remove_from_sprite_lists()
        self.enemy_bullets = new_enemy_bullets

        # Spawns
        for ev in self.wave.update(dt):
            for entry in ev["spawn"]:
                for _ in range(entry["n"]):
                    ex, ey = self.wave.random_spawn_position(self.bounds)
                    e = Enemy(arcade.SpriteSolidColor(18, 18, arcade.color.RED_DEVIL))
                    e.sprite.center_x, e.sprite.center_y = ex, ey
                    e.pattern = entry.get("pattern", "straight")
                    self.enemies.append(e)
                    self.enemy_sprite_list.append(e.sprite)

        # Inimigos: update & tiro
        for e in list(self.enemies):
            e.update(dt, (self.player.sprite.center_x, self.player.sprite.center_y))
            if e.ready():
                e.shot()
                px, py = self.player.sprite.center_x, self.player.sprite.center_y
                dx, dy = px - e.sprite.center_x, py - e.sprite.center_y
                angle = math.degrees(math.atan2(dy, dx))
                for x, y, vx, vy in make_bullets(e.pattern, (e.sprite.center_x, e.sprite.center_y), 180, angle=angle):
                    spr = arcade.SpriteSolidColor(4, 4, arcade.color.ORANGE_PEEL)
                    spr.center_x, spr.center_y = x, y
                    self.enemy_bullet_sprite_list.append(spr)
                    self.enemy_bullets.append((spr, vx, vy))

        # Colisões
        for spr, vx, vy in list(self.bullets):
            hits = arcade.check_for_collision_with_list(spr, self.enemy_sprite_list)
            if hits:
                for h in hits:
                    for e in list(self.enemies):
                        if e.sprite is h:
                            self.enemies.remove(e)
                            break
                    h.remove_from_sprite_lists()
                spr.remove_from_sprite_lists()
                self.bullets.remove((spr, vx, vy))

        if arcade.check_for_collision_with_list(self.player.sprite, self.enemy_bullet_sprite_list):
            self.player.hp -= 1
            for _ in range(min(5, len(self.enemy_bullets))):
                spr, vx, vy = self.enemy_bullets.pop(0)
                spr.remove_from_sprite_lists()
            if self.player.hp <= 0:
                self.window.show_view(HubView(self.window))

        if self.time >= 90:
            self.window.show_view(HubView(self.window))

    def on_key_press(self, symbol, modifiers): self.window.pressed_keys.add(symbol)
    def on_key_release(self, symbol, modifiers): self.window.pressed_keys.discard(symbol)
    def on_mouse_motion(self, x, y, dx, dy): self.window.mouse_xy = (x, y)
    def on_mouse_press(self, x, y, button, modifiers): self.window.pressed_mouse.add(button)
    def on_mouse_release(self, x, y, button, modifiers): self.window.pressed_mouse.discard(button)


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIN_W, WIN_H, "RPG+Shmup MVP (Patched)")
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        self.pressed_keys = set()
        self.pressed_mouse = set()
        self.mouse_xy = (0, 0)

def main():
    window = GameWindow()
    hub = HubView(window)
    window.show_view(hub)
    arcade.run()

if __name__ == "__main__":
    main()
