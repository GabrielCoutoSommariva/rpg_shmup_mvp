
import math
def make_bullets(pattern_name, origin, speed=200, count=1, angle=0):
    x,y=origin; bullets=[]
    if pattern_name=="straight":
        rad=math.radians(angle); bullets.append((x,y, math.cos(rad)*speed, math.sin(rad)*speed))
    elif pattern_name=="spread_3":
        base=angle
        for d in (-20,0,20):
            rad=math.radians(base+d); bullets.append((x,y, math.cos(rad)*speed, math.sin(rad)*speed))
    elif pattern_name=="ring_slow":
        for i in range(count):
            a=math.radians((360/count)*i); bullets.append((x,y, math.cos(a)*speed, math.sin(a)*speed))
    else:
        rad=math.radians(angle); bullets.append((x,y, math.cos(rad)*speed, math.sin(rad)*speed))
    return bullets
