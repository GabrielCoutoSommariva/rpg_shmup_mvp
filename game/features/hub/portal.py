
import arcade
class Portal(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(40, 100, arcade.color.ALMOND)
        self.center_x=x; self.center_y=y
