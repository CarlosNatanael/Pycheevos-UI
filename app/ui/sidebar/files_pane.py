"""
ui/sidebar/files_pane.py - file explorer content panel

Shows a ttk Treeview populated from a chosen folder.
Only .py files are double-click openable; folders expand lazily.
"""

from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from state.app_state import AppState
from utils.file_utils import ask_open_folder
from utils import persistence

PANEL_BG   = ("#1e1e2e", "#1e1e2e")
HEADER_FG  = ("#888899", "#888899")
TREE_BG    = "#1e1e2e"
TREE_FG    = "#cdd6f4"
TREE_SEL   = "#313244"
TREE_FONT  = ("Consolas", 11)


class FilesPane(ctk.CTkFrame):

    def __init__(self, parent, app_state: AppState):
        super().__init__(parent, corner_radius=0, fg_color=PANEL_BG)
        self.app_state = app_state
        self._build()
        self._restore_last_folder()

    # ------------------------------------------------------------------

    def _restore_last_folder(self):
        config = persistence.load()
        last = config.get("last_folder")
        if last and os.path.isdir(last):
            self._placeholder.place_forget()
            self._populate(last)

    # ------------------------------------------------------------------

    def _build(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # -- header bar --
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent", height=32)
        header.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 2))

        ctk.CTkLabel(header, text="EXPLORER",
                     font=("Segoe UI", 10, "bold"),
                     text_color=HEADER_FG).pack(side="left")

        ctk.CTkButton(header, text="📂", width=28, height=24,
                      fg_color="transparent",
                      hover_color=("#313244", "#313244"),
                      command=self.open_folder).pack(side="right")

        # -- tree --
        tree_wrap = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        tree_wrap.grid(row=1, column=0, sticky="nsew")
        tree_wrap.grid_rowconfigure(0, weight=1)
        tree_wrap.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Files.Treeview",
                        background=TREE_BG, foreground=TREE_FG,
                        fieldbackground=TREE_BG, font=TREE_FONT, rowheight=22)
        style.map("Files.Treeview",
                  background=[("selected", TREE_SEL)],
                  foreground=[("selected", "#cba6f7")])
        style.configure("Files.Treeview.Heading", background=TREE_BG,
                        foreground=TREE_FG)

        self._tree = ttk.Treeview(tree_wrap, style="Files.Treeview",
                                   show="tree", selectmode="browse")
        self._tree.grid(row=0, column=0, sticky="nsew")

        sb = ctk.CTkScrollbar(tree_wrap, command=self._tree.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self._tree.configure(yscrollcommand=sb.set)

        self._tree.bind("<<TreeviewOpen>>",   self._on_expand)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        # -- placeholder --
        self._placeholder = ctk.CTkLabel(
            tree_wrap, text="Open a folder\nto explore files",
            font=("Segoe UI", 11), text_color=("#444455", "#444455"),
        )
        self._placeholder.place(relx=0.5, rely=0.45, anchor="center")

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def open_folder(self):
        path = ask_open_folder()
        if not path:
            return
        config = persistence.load()
        config["last_folder"] = path
        persistence.save(config)
        self._placeholder.place_forget()
        self._populate(path)

    # ------------------------------------------------------------------
    # Tree population (lazy)
    # ------------------------------------------------------------------

    def _populate(self, path: str):
        self._tree.delete(*self._tree.get_children())
        node = self._tree.insert("", "end",
                                  text=f"📁 {os.path.basename(path)}",
                                  values=[path, "dir"], open=True)
        self._fill(node, path)

    def _fill(self, parent_node, dir_path: str):
        try:
            entries = sorted(os.scandir(dir_path),
                             key=lambda e: (not e.is_dir(), e.name.lower()))
        except PermissionError:
            return

        for entry in entries:
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                node = self._tree.insert(parent_node, "end",
                                          text=f"📁 {entry.name}",
                                          values=[entry.path, "dir"])
                # Dummy child so expand arrow appears
                self._tree.insert(node, "end", values=["__loading__", ""])
            elif entry.name.endswith(".py"):
                self._tree.insert(parent_node, "end",
                                   text=f"📄 {entry.name}",
                                   values=[entry.path, "file"])

    def _on_expand(self, _event):
        node = self._tree.focus()
        children = self._tree.get_children(node)
        if len(children) == 1:
            val = self._tree.item(children[0], "values")
            if val and val[0] == "__loading__":
                self._tree.delete(children[0])
                path = self._tree.item(node, "values")[0]
                self._fill(node, path)

    def _on_select(self, _event):
        selection = self._tree.selection()
        if not selection:
            return
        vals = self._tree.item(selection[0], "values")
        if vals and vals[1] == "file":
            self.app_state.open_file(vals[0])