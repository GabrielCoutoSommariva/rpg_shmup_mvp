
class EventBus:
    def __init__(self): self._subs = {}
    def on(self, event, fn): self._subs.setdefault(event, []).append(fn)
    def emit(self, event, *args, **kwargs):
        for fn in self._subs.get(event, []): fn(*args, **kwargs)

global_bus = EventBus()
