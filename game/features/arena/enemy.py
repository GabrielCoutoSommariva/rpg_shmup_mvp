
import arcade
from dataclasses import dataclass
@dataclass
class Enemy:
    sprite: arcade.Sprite; speed: float=80; hp: int=3; pattern: str="straight"
    cooldown: float=1.2; cd_timer: float=0.0
    def update(self, dt, target_xy):
        tx,ty=target_xy; dx,dy=tx-self.sprite.center_x, ty-self.sprite.center_y
        mag=(dx*dx+dy*dy)**0.5 + 1e-6
        self.sprite.center_x += (dx/mag)*self.speed*dt; self.sprite.center_y += (dy/mag)*self.speed*dt
        if self.cd_timer>0: self.cd_timer-=dt
    def ready(self): return self.cd_timer<=0
    def shot(self): self.cd_timer=self.cooldown
