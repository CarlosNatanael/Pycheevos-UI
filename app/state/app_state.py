"""
state/app_state.py - shared application state + event bus

Panels communicate through named events rather than direct references.

    state.on("file_opened", callback)   # subscribe
    state.emit("file_opened", path=p)   # publish
"""

from __future__ import annotations
from collections import defaultdict
from typing import Any, Callable


class AppState:

    def __init__(self):
        # -- IDE-wide state fields ------------------------------------
        self.open_files:       list[str]  = []
        self.active_file:      str | None = None
        self.memory_addresses: list[dict] = []
        self.dirty_files:      set[str]   = set()

        self._listeners: dict[str, list[Callable]] = defaultdict(list)

    # -- event bus ----------------------------------------------------

    def on(self, event: str, cb: Callable) -> None:
        self._listeners[event].append(cb)

    def off(self, event: str, cb: Callable) -> None:
        try:
            self._listeners[event].remove(cb)
        except ValueError:
            pass

    def emit(self, event: str, **kwargs: Any) -> None:
        for cb in list(self._listeners[event]):
            cb(**kwargs)

    # -- convenience mutators -----------------------------------------

    def open_file(self, path: str) -> None:
        if path not in self.open_files:
            self.open_files.append(path)
        self.active_file = path
        self.emit("file_opened", path=path)

    def close_file(self, path: str) -> None:
        if path in self.open_files:
            self.open_files.remove(path)
        self.dirty_files.discard(path)
        self.active_file = self.open_files[-1] if self.open_files else None
        self.emit("file_closed", path=path)

    def mark_dirty(self, path: str) -> None:
        self.dirty_files.add(path)
        self.emit("content_changed", path=path)

    def mark_clean(self, path: str) -> None:
        self.dirty_files.discard(path)
        self.emit("file_saved", path=path)