"""
ui/sidebar/tab_strip.py - narrow (~48px) vertical icon rail

Each tab has:
  - an icon (always visible)
  - a short text label shown only when that tab is active

Settings button is pinned to the bottom.
Calls on_select(name) when the active tab changes.
"""

from __future__ import annotations
import customtkinter as ctk


# Icons for each tab (unicode)
TAB_DEFS = [
    ("Files",    "📁"),
    ("Cheevos",  "🏆"),
]
SETTINGS_DEF = ("Settings", "⚙")

RAIL_WIDTH   = 52
ICON_SIZE    = 22
ACTIVE_FG    = ("#cba6f7", "#cba6f7")   # purple accent when active
INACTIVE_FG  = ("#6c6c8a", "#6c6c8a")
ACTIVE_BG    = ("#313244", "#313244")
HOVER_BG     = ("#2a2a3d", "#2a2a3d")
RAIL_BG      = ("#181825", "#181825")


class TabStrip(ctk.CTkFrame):
    """Narrow vertical icon rail."""

    def __init__(self, parent, on_select, on_settings, active: str = "Files"):
        super().__init__(
            parent,
            width=RAIL_WIDTH,
            corner_radius=0,
            fg_color=RAIL_BG,
        )
        self.grid_propagate(False)
        self.pack_propagate(False)

        self._on_select   = on_select
        self._on_settings = on_settings
        self._active      = active
        self._buttons: dict[str, _RailButton] = {}

        self._build()

    # ------------------------------------------------------------------

    def _build(self):
        # Top section - main tabs
        top = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        top.pack(side="top", fill="x")

        for name, icon in TAB_DEFS:
            btn = _RailButton(top, name=name, icon=icon,
                              on_click=self._on_tab_click)
            btn.pack(fill="x")
            self._buttons[name] = btn

        # Bottom section - settings pinned to bottom
        bottom = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        bottom.pack(side="bottom", fill="x")

        self._settings_btn = _RailButton(
            bottom,
            name=SETTINGS_DEF[0],
            icon=SETTINGS_DEF[1],
            on_click=lambda n: self._on_settings(),
        )
        self._settings_btn.pack(fill="x")

        # Set initial active state
        self._refresh(self._active)

    def _on_tab_click(self, name: str):
        self._active = name
        self._refresh(name)
        self._on_select(name)

    def _refresh(self, active: str):
        for name, btn in self._buttons.items():
            btn.set_active(name == active)


# -----------------------------------------------------------------------
# Single rail button
# -----------------------------------------------------------------------

class _RailButton(ctk.CTkFrame):
    """One icon + optional label in the rail."""

    def __init__(self, parent, name: str, icon: str, on_click):
        super().__init__(parent, fg_color="transparent", corner_radius=0,
                         height=56)
        self.pack_propagate(False)
        self._name     = name
        self._on_click = on_click
        self._active   = False

        # -- icon label ----------------------------------------------
        self._icon_lbl = ctk.CTkLabel(
            self, text=icon,
            font=("Segoe UI Emoji", ICON_SIZE),
            text_color=INACTIVE_FG,
            fg_color="transparent",
            cursor="hand2",
        )
        self._icon_lbl.pack(pady=(8, 0))

        # -- text label (hidden when inactive) -----------------------
        self._text_lbl = ctk.CTkLabel(
            self, text=name,
            font=("Segoe UI", 9),
            text_color=INACTIVE_FG,
            fg_color="transparent",
            cursor="hand2",
        )
        self._text_lbl.pack(pady=(0, 4))

        # -- click + hover bindings ----------------------------------
        for widget in (self, self._icon_lbl, self._text_lbl):
            widget.bind("<Button-1>", self._click)
            widget.bind("<Enter>",    self._hover_on)
            widget.bind("<Leave>",    self._hover_off)

    def set_active(self, active: bool):
        self._active = active
        if active:
            self.configure(fg_color=ACTIVE_BG)
            self._icon_lbl.configure(text_color=ACTIVE_FG)
            self._text_lbl.configure(text_color=ACTIVE_FG)
        else:
            self.configure(fg_color="transparent")
            self._icon_lbl.configure(text_color=INACTIVE_FG)
            self._text_lbl.configure(text_color=INACTIVE_FG)

    def _click(self, _event=None):
        self._on_click(self._name)

    def _hover_on(self, _event=None):
        if not self._active:
            self.configure(fg_color=HOVER_BG)

    def _hover_off(self, _event=None):
        if not self._active:
            self.configure(fg_color="transparent")