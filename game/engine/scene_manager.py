
import arcade
class SceneManager:
    def __init__(self, window: arcade.Window): self.window = window
    def go(self, view: arcade.View): self.window.show_view(view)
