"""
ui/sidebar/sidebar.py - sidebar outer frame

Combines the narrow TabStrip rail on the left with a content panel on
the right. Swapping tabs shows/hides the relevant pane.

Public method:
    open_folder()  - forwarded from the Files pane (called by menubar)
"""

from __future__ import annotations
from tkinter import messagebox
import customtkinter as ctk

from state.app_state import AppState
from ui.sidebar.tab_strip  import TabStrip
from ui.sidebar.files_pane import FilesPane
from ui.sidebar.cheevos_pane import CheevosPane

SIDEBAR_W  = 260   # total width including the rail
CONTENT_BG = ("#1e1e2e", "#1e1e2e")
DIVIDER    = ("#313244", "#313244")


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, app_state: AppState):
        super().__init__(parent, corner_radius=0,
                         fg_color=CONTENT_BG,
                         width=SIDEBAR_W)
        self.grid_propagate(False)
        self.app_state = app_state
        self._build()

    # ------------------------------------------------------------------

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # rail
        self.grid_columnconfigure(1, weight=1)  # content

        # -- icon rail --
        self._rail = TabStrip(
            self,
            on_select=self._switch_pane,
            on_settings=self._open_settings,
            active="Files",
        )
        self._rail.grid(row=0, column=0, sticky="ns")

        # -- thin divider line --
        divider = ctk.CTkFrame(self, width=1, corner_radius=0,
                                fg_color=DIVIDER)
        divider.grid(row=0, column=1, sticky="ns")

        # -- content panes (stacked, only one visible at a time) --
        self._panes: dict[str, ctk.CTkFrame] = {}

        self._files_pane   = FilesPane(self, self.app_state)
        self._cheevos_pane = CheevosPane(self, self.app_state)

        self._panes["Files"]   = self._files_pane
        self._panes["Cheevos"] = self._cheevos_pane

        for pane in self._panes.values():
            pane.grid(row=0, column=2, sticky="nsew")

        self.grid_columnconfigure(2, weight=1)

        self._switch_pane("Files")

    # ------------------------------------------------------------------
    # Tab switching
    # ------------------------------------------------------------------

    def _switch_pane(self, name: str):
        for key, pane in self._panes.items():
            if key == name:
                pane.lift()
            else:
                pane.lower()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def open_folder(self):
        """Forward to the Files pane (called by menubar / app)."""
        self._switch_pane("Files")
        self._rail._on_tab_click("Files")
        self._files_pane.open_folder()

    def _open_settings(self):
        # Stub - settings dialog will come later
        messagebox.showinfo("Settings", "Settings panel coming soon.")