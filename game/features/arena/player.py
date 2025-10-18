
import arcade
from dataclasses import dataclass
@dataclass
class Player:
    sprite: arcade.Sprite; speed: float=220; dash_speed: float=480
    dash_cooldown: float=1.0; dash_time: float=0.12
    dash_timer: float=0.0; dash_cd_timer: float=0.0; hp: int=5
    def update(self, dt, move_x, move_y, bounds):
        if self.dash_timer>0: self.dash_timer-=dt; mult=self.dash_speed
        else: mult=self.speed
        self.sprite.center_x += move_x*mult*dt; self.sprite.center_y += move_y*mult*dt
        self.sprite.center_x = max(bounds[0], min(bounds[1], self.sprite.center_x))
        self.sprite.center_y = max(bounds[2], min(bounds[3], self.sprite.center_y))
        if self.dash_cd_timer>0: self.dash_cd_timer-=dt
    def can_dash(self): return self.dash_cd_timer<=0
    def start_dash(self): self.dash_timer=self.dash_time; self.dash_cd_timer=self.dash_cooldown
