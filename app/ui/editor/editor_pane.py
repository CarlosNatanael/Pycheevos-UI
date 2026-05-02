"""
ui/editor/editor_pane.py - manages the tab bar + stack of EditorInstances

One EditorInstance is created per open file and stacked in a grid.
Only the active instance is raised to the top.
"""

from __future__ import annotations
import customtkinter as ctk

from state.app_state import AppState
from ui.editor.editor_tab_bar  import EditorTabBar
from ui.editor.editor_instance import EditorInstance
from utils.file_utils import ask_open_file

PANE_BG = ("#1e1e2e", "#1e1e2e")

_WELCOME = """\
# Welcome to PyCheevos UI
# Open a file from the sidebar or File menu to get started.

from pycheevos import *

"""


class EditorPane(ctk.CTkFrame):

    def __init__(self, parent, app_state: AppState):
        super().__init__(parent, corner_radius=0, fg_color=PANE_BG)
        self.app_state = app_state

        self._instances: dict[str, EditorInstance] = {}   # path -> instance
        self._active_path: str | None = None

        self._build()
        self._wire_state()

        # Open a blank welcome buffer on launch
        self.new_file(content=_WELCOME)

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build(self):
        self.grid_rowconfigure(0, weight=0)   # tab bar
        self.grid_rowconfigure(1, weight=1)   # editor area
        self.grid_columnconfigure(0, weight=1)

        self._tab_bar = EditorTabBar(
            self,
            on_select=self._activate,
            on_close=self._close_tab,
        )
        self._tab_bar.grid(row=0, column=0, sticky="ew")

        self._editor_area = ctk.CTkFrame(self, corner_radius=0,
                                          fg_color=PANE_BG)
        self._editor_area.grid(row=1, column=0, sticky="nsew")
        self._editor_area.grid_rowconfigure(0, weight=1)
        self._editor_area.grid_columnconfigure(0, weight=1)

    def _wire_state(self):
        """Subscribe to app_state events."""
        self.app_state.on("file_opened",    self._on_file_opened)
        self.app_state.on("content_changed", self._on_content_changed)
        self.app_state.on("file_saved",     self._on_file_saved)

    # ------------------------------------------------------------------
    # State event handlers
    # ------------------------------------------------------------------

    def _on_file_opened(self, path: str):
        self._open_or_focus(path)

    def _on_content_changed(self, path: str):
        self._tab_bar.set_dirty(path, dirty=True)

    def _on_file_saved(self, path: str):
        self._tab_bar.set_dirty(path, dirty=False)

    # ------------------------------------------------------------------
    # Internal tab management
    # ------------------------------------------------------------------

    def _open_or_focus(self, path: str):
        if path not in self._instances:
            inst = EditorInstance(self._editor_area, self.app_state, path=path)
            inst.grid(row=0, column=0, sticky="nsew")
            self._instances[path] = inst
            self._tab_bar.add_tab(path)
        self._activate(path)

    def _activate(self, path: str):
        self._active_path = path
        for p, inst in self._instances.items():
            if p == path:
                inst.lift()
            else:
                inst.lower()
        self._tab_bar.set_active(path)

    def _close_tab(self, path: str):
        inst = self._instances.get(path)
        if inst and inst.is_dirty:
            from tkinter import messagebox
            save = messagebox.askyesnocancel(
                "Unsaved Changes",
                f"{path}\n\nSave before closing?",
            )
            if save is None:
                return       # cancel
            if save:
                inst.save()

        if inst:
            inst.destroy()
        self._instances.pop(path, None)
        self._tab_bar.remove_tab(path)
        self.app_state.close_file(path)

        # Focus another open tab if one exists
        if self._instances:
            self._activate(next(iter(self._instances)))

    # ------------------------------------------------------------------
    # Public API (called by menubar / app)
    # ------------------------------------------------------------------

    def new_file(self, content: str = ""):
        key = f"__new_{len(self._instances)}__"
        inst = EditorInstance(self._editor_area, self.app_state, path=None)
        inst.grid(row=0, column=0, sticky="nsew")
        if content:
            inst._editor.content.insert("1.0", content)
            inst._editor.content.event_generate("<KeyRelease>")
        self._instances[key] = inst
        self._tab_bar.add_tab(key)
        self._activate(key)

    def open_file(self):
        path = ask_open_file()
        if path:
            self.app_state.open_file(path)

    def save(self):
        if self._active_path and self._active_path in self._instances:
            self._instances[self._active_path].save()

    def save_as(self):
        if self._active_path and self._active_path in self._instances:
            self._instances[self._active_path].save_as()

    def undo(self):
        self._active_instance_call("undo")

    def redo(self):
        self._active_instance_call("redo")

    def cut(self):
        self._active_instance_call("cut")

    def copy(self):
        self._active_instance_call("copy")

    def paste(self):
        self._active_instance_call("paste")

    # Callback wired from app_state "content_changed"
    def on_content_changed(self, path: str):
        self._tab_bar.set_dirty(path, dirty=True)

    def _active_instance_call(self, method: str):
        if self._active_path and self._active_path in self._instances:
            getattr(self._instances[self._active_path], method)()