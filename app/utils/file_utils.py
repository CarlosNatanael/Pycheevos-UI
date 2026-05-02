"""
utils/file_utils.py - file dialog helpers and path utilities
"""

from __future__ import annotations
import os
from tkinter import filedialog, messagebox


def ask_open_folder() -> str | None:
    return filedialog.askdirectory(title="Open Project Folder") or None


def ask_open_file() -> str | None:
    return filedialog.askopenfilename(
        title="Open File",
        filetypes=[("Python files", "*.py"), ("All files", "*.*")],
    ) or None


def ask_save_file(initial: str | None = None) -> str | None:
    return filedialog.asksaveasfilename(
        title="Save As",
        initialfile=initial,
        defaultextension=".py",
        filetypes=[("Python files", "*.py"), ("All files", "*.*")],
    ) or None


def read_file(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception as exc:
        messagebox.showerror("Open Error", f"Could not read file:\n{exc}")
        return None


def write_file(path: str, content: str) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        return True
    except Exception as exc:
        messagebox.showerror("Save Error", f"Could not save file:\n{exc}")
        return False