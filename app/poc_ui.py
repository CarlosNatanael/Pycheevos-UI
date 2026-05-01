import tkinter as tk
import customtkinter as ctk
from cupcake import Editor, Languages

# 1. Initial CustomTkinter Setup
ctk.set_appearance_mode("Dark")  # Forcing dark mode
ctk.set_default_color_theme("blue")

class PyCheevosPoC(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyCheevos UI")
        self.geometry("1000x600")
        self.iconbitmap("app/icone.ico")

        # Layout: Grid 1x2 (1 row, 2 columns)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Left: UI (25% space)
        self.grid_columnconfigure(1, weight=3)  # Right: Editor (75% space)

        # ==========================================
        # LEFT PANEL (Pure CustomTkinter UI)
        # ==========================================
        self.left_frame = ctk.CTkFrame(self, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.label = ctk.CTkLabel(self.left_frame, text="PyCheevos UI", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.pack(pady=20, padx=20)

        self.btn_gen = ctk.CTkButton(self.left_frame, text="Generate Boilerplate")
        self.btn_gen.pack(pady=10, padx=20)
        
        self.btn_build = ctk.CTkButton(self.left_frame, text="Build (Mock)", fg_color="green", hover_color="darkgreen")
        self.btn_build.pack(pady=10, padx=20)

        # ==========================================
        # RIGHT PANEL (Cupcake Editor)
        # ==========================================
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1e1e1e")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2) # Slight margin to see the division

        # Instantiating Cupcake and setting Python as the language
        self.editor = Editor(self.right_frame, language=Languages.PYTHON)
        self.editor.pack(expand=True, fill="both")

        # Injecting realistic PyCheevos test code
        codigo_teste = """
# ==========================================
# PyCheevos CORE - Set Logic
# ==========================================
from models.set import AchievementSet

# Mapped variables
mem_level = byte(0x003da8)
mem_hp = byte(0x003da9)

# The UI dictates the metadata, here we focus only on memory!
def cheevo_level_1_logic():
    return (
        mem_level == 1 and 
        mem_hp > 0
    )

# ...
"""
        self.editor.content.insert("end", codigo_teste)
        self.update_idletasks()
        self.editor.content.event_generate("<KeyRelease>")

if __name__ == "__main__":
    app = PyCheevosPoC()
    app.mainloop()