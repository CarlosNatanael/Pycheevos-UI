"""
ui/editor/editor_instance.py - wrapper around a single cupcake Editor tab

Responsibilities:
  - Create and own one cupcake Editor widget
  - Load / save file content
  - Notify app_state when content changes (dirty flag)
  - Expose undo / redo / cut / copy / paste / get_content helpers
"""

from __future__ import annotations
import os

import customtkinter as ctk
from cupcake import Editor, Languages

from state.app_state import AppState
from utils.file_utils import read_file, write_file, ask_save_file

# Resolve theme path relative to this file so it works from any cwd
_THEME_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "themes", "pycheevos.toml")
)


class EditorInstance(ctk.CTkFrame):
    """
    A single editor tab - one cupcake Editor + file state.

    Parameters
    ----------
    path : str | None
        File to load on creation. None = new unsaved buffer.
    """

    def __init__(self, parent, app_state: AppState, path: str | None = None):
        super().__init__(parent, corner_radius=0, fg_color="#1e1e2e")
        self.app_state = app_state
        self.path      = path
        self._is_dirty = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._editor = Editor(
            self,
            language=Languages.PYTHON,
            config_file=_THEME_PATH,
        )
        self._editor.grid(row=0, column=0, sticky="nsew")

        # Bind content changes -> dirty flag
        self._editor.content.bind("<<Modified>>", self._on_modified)

        if path:
            self._load(path)

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def _load(self, path: str):
        content = read_file(path)
        if content is None:
            return
        self._editor.content.delete("1.0", "end")
        self._editor.content.insert("1.0", content)
        # Trigger syntax highlight refresh
        self._editor.content.edit_modified(False)
        self._editor.content.event_generate("<KeyRelease>")

    def save(self) -> bool:
        """Save to current path. Returns True on success."""
        if not self.path:
            return self.save_as()
        if write_file(self.path, self.get_content()):
            self._is_dirty = False
            self.app_state.mark_clean(self.path)
            return True
        return False

    def save_as(self) -> bool:
        """Prompt for a new path then save."""
        new_path = ask_save_file(
            initial=os.path.basename(self.path) if self.path else "untitled.py"
        )
        if not new_path:
            return False
        self.path = new_path
        return self.save()

    # ------------------------------------------------------------------
    # Edit helpers (delegated to the underlying tk.Text)
    # ------------------------------------------------------------------

    def get_content(self) -> str:
        return self._editor.content.get("1.0", "end-1c")

    def undo(self):
        try:
            self._editor.content.edit_undo()
        except Exception:
            pass

    def redo(self):
        try:
            self._editor.content.edit_redo()
        except Exception:
            pass

    def cut(self):
        self._editor.content.event_generate("<<Cut>>")

    def copy(self):
        self._editor.content.event_generate("<<Copy>>")

    def paste(self):
        self._editor.content.event_generate("<<Paste>>")

    # ------------------------------------------------------------------
    # Dirty state
    # ------------------------------------------------------------------

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def _on_modified(self, _event=None):
        if self._editor.content.edit_modified():
            if not self._is_dirty:
                self._is_dirty = True
                if self.path:
                    self.app_state.mark_dirty(self.path)
            # Reset tk's internal modified flag so the event fires again next change
            self._editor.content.edit_modified(False)