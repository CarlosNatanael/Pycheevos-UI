"""
app.py - root CTk window for PyCheevos UI

Three-column layout:
  col 0 - Sidebar        (fixed width, tabbed)
  col 1 - EditorPane     (expands)
  col 2 - MetadataPanel  (collapsible)

Panels are imported lazily so each file can be built incrementally.
"""

import customtkinter as ctk
from state.app_state import AppState
from ui.sidebar.sidebar import Sidebar
from ui.editor.editor_pane import EditorPane

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -- cupcake registers a ttk element on every Editor instantiation which
# -- raises TclError: "Duplicate element Treeitem.nindicator" for the 2nd+
# -- tab. Patch ttk.Style.element_create to swallow that specific error.
import tkinter.ttk as _ttk
_orig_element_create = _ttk.Style.element_create
def _safe_element_create(self, elementname, etype, *args, **kwargs):
    try:
        _orig_element_create(self, elementname, etype, *args, **kwargs)
    except Exception as e:
        if "Duplicate element" not in str(e):
            raise
_ttk.Style.element_create = _safe_element_create


class PycheevosuiApp(ctk.CTk):

    MIN_W, MIN_H = 1100, 680

    def __init__(self):
        super().__init__()
        self.title("PyCheevos UI")
        self.geometry("1400x800")
        self.minsize(self.MIN_W, self.MIN_H)

        self.app_state = AppState()

        self._build_layout()
        self._build_panels()

        # -- debounce resize to prevent flicker when maximising ----------
        self._resize_job = None
        self.bind("<Configure>", self._on_configure)

    # ------------------------------------------------------------------

    def _on_configure(self, event):
        """Freeze layout updates during rapid resize, apply once settled."""
        if event.widget is not self:
            return
        # Cancel any previously scheduled redraw
        if self._resize_job:
            self.after_cancel(self._resize_job)
        # Temporarily hide content to avoid partial redraws
        self._content.grid_remove()
        # Schedule a single redraw 80ms after the last resize event
        self._resize_job = self.after(80, self._apply_resize)

    def _apply_resize(self):
        self._resize_job = None
        self._content.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()

    # ------------------------------------------------------------------

    def _build_layout(self):
        """Three-row root grid: menu(0) | content(1) | statusbar(2)."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self._content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._content.grid(row=0, column=0, sticky="nsew")

        self._content.grid_rowconfigure(0, weight=1)
        self._content.grid_columnconfigure(0, weight=0)  # sidebar
        self._content.grid_columnconfigure(1, weight=1)  # editor
        self._content.grid_columnconfigure(2, weight=0)  # metadata

    def _build_panels(self):
        # --- placeholder frames until each panel file is written -----
        # Replace each with the real import once that file exists.

        self.sidebar = Sidebar(self._content, self.app_state)
        self.editor  = EditorPane(self._content, self.app_state)
        self.metadata = _PlaceholderFrame(self._content, label="Metadata Panel\n(collapsible)", width=260)

        self.sidebar.grid( row=0, column=0, sticky="nsew")
        self.editor.grid(  row=0, column=1, sticky="nsew", padx=2)
        self.metadata.grid(row=0, column=2, sticky="nsew")

        # --- placeholder status bar ----------------------------------
        self._statusbar = ctk.CTkLabel(
            self, text="PyCheevos UI  |  ready",
            fg_color=("#181825", "#181825"),
            text_color=("#888899", "#888899"),
            anchor="w", font=("Consolas", 11),
        )
        self._statusbar.grid(row=1, column=0, sticky="ew", padx=8, pady=2)


# -----------------------------------------------------------------------
# Temporary placeholder - removed once the real panel is implemented
# -----------------------------------------------------------------------

class _PlaceholderFrame(ctk.CTkFrame):
    """Visible stand-in so the layout is testable before panels are built."""

    def __init__(self, parent, label: str, width: int = 0):
        kw = {"width": width} if width else {}
        super().__init__(parent, corner_radius=4,
                         fg_color=("#1e1e2e", "#1e1e2e"),
                         border_color=("#313244", "#313244"),
                         border_width=1, **kw)
        if width:
            self.grid_propagate(False)

        ctk.CTkLabel(self, text=label,
                     text_color=("#555566", "#555566"),
                     font=("Segoe UI", 11)).place(relx=0.5, rely=0.5, anchor="center")