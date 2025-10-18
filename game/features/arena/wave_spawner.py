
import json, os, random
class WaveSpawner:
    def __init__(self, waves_path, biome="biome_1"):
        self.data=json.load(open(waves_path, "r", encoding="utf-8"))
        self.timeline=self.data.get(biome, []); self.t=0.0; self.i=0
    def update(self, dt):
        self.t+=dt; events=[]
        while self.i<len(self.timeline) and self.timeline[self.i]["t"]<=self.t:
            events.append(self.timeline[self.i]); self.i+=1
        return events
    @staticmethod
    def random_spawn_position(bounds):
        x0,x1,y0,y1=bounds
        side=random.choice(["top","bottom","left","right"])
        if side=="top": return random.uniform(x0,x1), y1+30
        if side=="bottom": return random.uniform(x0,x1), y0-30
        if side=="left": return x0-30, random.uniform(y0,y1)
        return x1+30, random.uniform(y0,y1)
