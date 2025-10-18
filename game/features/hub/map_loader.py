
import arcade
class HubMap:
    def __init__(self, width=800, height=600):
        self.width=width; self.height=height
    def draw(self):
        # Correct Arcade call: left,right,bottom,top
        arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height, arcade.color.DARK_SLATE_BLUE)
        arcade.draw_text("Hub — portal à direita", 20, self.height-30, arcade.color.WHITE, 18)
