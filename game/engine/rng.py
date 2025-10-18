
import random
class RNG:
    def __init__(self, seed=None): self._rng=random.Random(seed)
    def choice(self, seq): return self._rng.choice(seq)
    def randint(self, a,b): return self._rng.randint(a,b)
    def random(self): return self._rng.random()
