
import arcade
from dataclasses import dataclass
@dataclass
class Bullet:
    sprite: arcade.Sprite; vx: float=0.0; vy: float=0.0; alive: bool=False
    def reset(self, x,y,vx,vy):
        self.sprite.center_x=x; self.sprite.center_y=y; self.vx=vx; self.vy=vy; self.alive=True
    def update(self, dt):
        if not self.alive: return
        self.sprite.center_x += self.vx*dt; self.sprite.center_y += self.vy*dt
        if (self.sprite.center_x < -100 or self.sprite.center_x > 2000 or
            self.sprite.center_y < -100 or self.sprite.center_y > 2000): self.alive=False
