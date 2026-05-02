"""
ui/sidebar/cheevos_pane.py - achievements panel (stub)

Displays a placeholder list of achievements.
Will be wired to real pycheevos data later.
"""

from __future__ import annotations
import customtkinter as ctk
from state.app_state import AppState

PANEL_BG  = ("#1e1e2e", "#1e1e2e")
HEADER_FG = ("#888899", "#888899")
ITEM_BG   = ("#2a2a3d", "#2a2a3d")
ITEM_FG   = ("#cdd6f4", "#cdd6f4")
DIM_FG    = ("#6c6c8a", "#6c6c8a")

# Stub data - replace with real pycheevos data later
_STUB_ACHIEVEMENTS = [
    {"title": "First Blood",    "points": 5,  "desc": "Get a kill for the first time"},
    {"title": "Speed Demon",    "points": 10, "desc": "Finish a race under 1:30"},
    {"title": "Completionist",  "points": 25, "desc": "Collect every item in the game"},
]


class CheevosPane(ctk.CTkFrame):

    def __init__(self, parent, app_state: AppState):
        super().__init__(parent, corner_radius=0, fg_color=PANEL_BG)
        self.app_state = app_state
        self._build()

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # -- header --
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=32)
        header.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 2))
        ctk.CTkLabel(header, text="ACHIEVEMENTS",
                     font=("Segoe UI", 10, "bold"),
                     text_color=HEADER_FG).pack(side="left")

        # -- scrollable list --
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0,
                                         fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
        scroll.grid_columnconfigure(0, weight=1)

        for i, ach in enumerate(_STUB_ACHIEVEMENTS):
            _AchievementItem(scroll, ach).grid(
                row=i, column=0, sticky="ew", pady=(0, 4))


class _AchievementItem(ctk.CTkFrame):
    """Single achievement row."""

    def __init__(self, parent, data: dict):
        super().__init__(parent, corner_radius=6, fg_color=ITEM_BG)
        self.grid_columnconfigure(0, weight=1)

        title_row = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        title_row.grid(row=0, column=0, sticky="ew", padx=8, pady=(6, 0))
        title_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(title_row, text=data["title"],
                     font=("Segoe UI", 11, "bold"),
                     text_color=ITEM_FG, anchor="w").grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(title_row, text=f"{data['points']}pts",
                     font=("Segoe UI", 10),
                     text_color=("#f9e2af", "#f9e2af"), anchor="e").grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(self, text=data["desc"],
                     font=("Segoe UI", 10),
                     text_color=DIM_FG, anchor="w",
                     wraplength=160).grid(row=1, column=0, sticky="ew", padx=8, pady=(2, 6))