"""
ui/editor/editor_tab_bar.py - horizontal tab bar for open editor buffers

Each tab shows the filename and a close (×) button.
Dirty tabs get a dot (•) prefix instead of a space.
Calls on_select(path) and on_close(path) when clicked.
"""

from __future__ import annotations
import os
import customtkinter as ctk

TAB_BG_ACTIVE   = ("#1e1e2e", "#1e1e2e")
TAB_BG_INACTIVE = ("#181825", "#181825")
TAB_FG_ACTIVE   = ("#cdd6f4", "#cdd6f4")
TAB_FG_INACTIVE = ("#6c6c8a", "#6c6c8a")
TAB_ACCENT      = ("#cba6f7", "#cba6f7")   # top border on active tab
CLOSE_HOVER     = ("#f38ba8", "#f38ba8")
BAR_BG          = ("#181825", "#181825")


class EditorTabBar(ctk.CTkFrame):

    def __init__(self, parent, on_select, on_close):
        super().__init__(parent, corner_radius=0, fg_color=BAR_BG, height=34)
        self.pack_propagate(False)
        self._on_select = on_select
        self._on_close  = on_close
        self._tabs:   dict[str, _Tab] = {}   # path -> Tab widget
        self._active: str | None = None

    # ------------------------------------------------------------------

    def add_tab(self, path: str):
        if path in self._tabs:
            self.set_active(path)
            return
        tab = _Tab(self, path=path,
                   on_click=self._on_select,
                   on_close=self._on_close)
        tab.pack(side="left", fill="y")
        self._tabs[path] = tab
        self.set_active(path)

    def remove_tab(self, path: str):
        if path not in self._tabs:
            return
        self._tabs[path].destroy()
        del self._tabs[path]

    def set_active(self, path: str):
        self._active = path
        for p, tab in self._tabs.items():
            tab.set_active(p == path)

    def set_dirty(self, path: str, dirty: bool):
        if path in self._tabs:
            self._tabs[path].set_dirty(dirty)


class _Tab(ctk.CTkFrame):

    def __init__(self, parent, path: str, on_click, on_close):
        super().__init__(parent, corner_radius=0,
                         fg_color=TAB_BG_INACTIVE, height=34)
        self.pack_propagate(False)
        self._path     = path
        self._on_click = on_click
        self._on_close = on_close
        self._dirty    = False
        self._active   = False

        self._name_lbl = ctk.CTkLabel(
            self,
            text=self._label_text(),
            font=("Segoe UI", 11),
            text_color=TAB_FG_INACTIVE,
            cursor="hand2",
        )
        self._name_lbl.pack(side="left", padx=(10, 4), pady=4)

        self._close_btn = ctk.CTkButton(
            self, text="×", width=18, height=18,
            corner_radius=3,
            fg_color="transparent",
            hover_color=("#313244", "#313244"),
            text_color=TAB_FG_INACTIVE,
            font=("Segoe UI", 13),
            command=self._close,
        )
        self._close_btn.pack(side="left", padx=(0, 6))

        # Click on the label or frame selects the tab
        for w in (self, self._name_lbl):
            w.bind("<Button-1>", lambda e: self._on_click(self._path))

    # ------------------------------------------------------------------

    def set_active(self, active: bool):
        self._active = active
        bg = TAB_BG_ACTIVE if active else TAB_BG_INACTIVE
        fg = TAB_FG_ACTIVE if active else TAB_FG_INACTIVE
        self.configure(fg_color=bg)
        self._name_lbl.configure(text_color=fg)
        self._close_btn.configure(text_color=fg)

    def set_dirty(self, dirty: bool):
        self._dirty = dirty
        self._name_lbl.configure(text=self._label_text())

    def _label_text(self) -> str:
        prefix = "• " if self._dirty else ""
        return prefix + os.path.basename(self._path)

    def _close(self):
        self._on_close(self._path)