
from dataclasses import dataclass
@dataclass
class InputState:
    up: bool=False; down: bool=False; left: bool=False; right: bool=False
    shoot: bool=False; dash: bool=False; mx: float=0.0; my: float=0.0
