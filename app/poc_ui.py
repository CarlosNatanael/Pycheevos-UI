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

        # Adicione estas linhas:
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

        # --- THE STYLE SURGERY ---
        # Trying to force Cupcake's classic Tkinter to accept Dark Mode
        try:
            # Classic tk.Text properties (the core of .content)
            self.editor.content.config(
                bg="#1e1e1e",             # Dark gray background
                fg="#d4d4d4",             # Light base text
                insertbackground="white", # White blinking cursor
                selectbackground="#264f78", # Text selection color (dark blue)
                relief="flat",            # Removes the 90s 3D border
                borderwidth=0
            )
            # Note: If Cupcake uses a Canvas for line numbers, 
            # you might need to access something like `self.editor.linenumbers.config(bg="#1e1e1e")` in the future.
        except Exception as e:
            print(f"Warning: Could not inject style directly. Error: {e}")

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

if __name__ == "__main__":
    app = PyCheevosPoC()
    app.mainloop()