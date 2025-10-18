
class Pool:
    def __init__(self, factory, size=128):
        self.factory=factory; self.items=[factory() for _ in range(size)]; self.active=[False]*size
    def acquire(self):
        for i,a in enumerate(self.active):
            if not a: self.active[i]=True; return self.items[i], i
        obj=self.factory(); self.items.append(obj); self.active.append(True); return obj, len(self.items)-1
    def release(self, index):
        if 0<=index<len(self.active): self.active[index]=False
