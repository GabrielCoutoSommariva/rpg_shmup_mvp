
import arcade
def draw_hud(player_hp, time_left, upgrades):
    arcade.draw_text(f"HP: {player_hp}", 20, 560, arcade.color.WHITE, 14)
    arcade.draw_text(f"T: {time_left:0.1f}", 120, 560, arcade.color.WHITE, 14)
    if upgrades: arcade.draw_text("Mods: " + ", ".join(upgrades), 220, 560, arcade.color.WHITE, 14)
