import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from typing import Dict, Optional

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Solver Collection")
        self.root.configure(bg="white")

        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.toggle_fullscreen())

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white', font=('Arial', 12))
        self.style.configure('Title.TLabel', font=('Arial', 20, 'bold'))

        self.style.configure(
            'Game.TButton',
            font=('Arial', 14),
            padding=10,
            background='#007acc',
            foreground='white',
            borderwidth=0,
            relief="flat"
        )
        self.style.map(
            'Game.TButton',
            background=[('active', '#005f99')],
            foreground=[('disabled', 'gray')]
        )

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)

        title_label = ttk.Label(
            main_frame, 
            text="Select a Game to Play", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))

        games_frame = ttk.Frame(main_frame)
        games_frame.pack(expand=True, fill=tk.BOTH)

        toggle_btn = ttk.Button(
            main_frame, 
            text="Toggle Fullscreen (Esc)", 
            command=self.toggle_fullscreen
        )
        toggle_btn.pack(pady=(10, 20))

        self.games = {
            "Sudoku": {
                "script": "games/sudoku.py",
                "has_difficulty": True,
                "difficulty_options": [
                    ("Easy", 40),
                    ("Medium", 30),
                    ("Hard", 20)
                ]
            },
            "Crossword": {
                "script": "games/crossword.py",
                "has_difficulty": False
            },
            "Maze": {
                "script": "games/maze.py",
                "has_difficulty": False
            },
            "N-Queens": {
                "script": "games/n_queens.py",
                "has_difficulty": False
            },
            "Graph Coloring": {
                "script": "games/graph_coloring.py",
                "has_difficulty": False
            }
        }
        for _, (game_name, game_info) in enumerate(self.games.items()):
            btn = ttk.Button(
                games_frame,
                text=game_name,
                style='Game.TButton',
                command=lambda gn=game_name: self.launch_game(gn)
            )
            btn.pack(fill=tk.X, pady=16)

    def launch_game(self, game_name: str):
        game_info = self.games[game_name]

        if game_info["has_difficulty"]:
            self.show_difficulty_dialog(game_name, game_info)
        else:
            self.run_game_script(game_info["script"], mode="visual")

    def show_difficulty_dialog(self, game_name: str, game_info: Dict):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Select Difficulty for {game_name}")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        self.center_window(dialog)

        diff_frame = ttk.Frame(dialog)
        diff_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        ttk.Label(diff_frame, text="Select Difficulty:").pack(pady=(10, 20))

        for diff_name, diff_value in game_info["difficulty_options"]:
            btn = ttk.Button(
                diff_frame,
                text=diff_name,
                command=lambda dv=diff_value: self.on_difficulty_selected(
                    game_info["script"], dv, dialog)
            )
            btn.pack(fill=tk.X, pady=5)

    def on_difficulty_selected(self, script: str, difficulty: int, dialog: tk.Toplevel):
        dialog.destroy()
        self.run_game_script(script, mode="visual", difficulty=difficulty)

    def run_game_script(self, script: str, mode: str, difficulty: Optional[int] = None):
        try:
            self.root.withdraw()
            cmd = [sys.executable, script, mode]
            if difficulty is not None:
                cmd.append(str(difficulty))
            subprocess.run(cmd)
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game: {str(e)}")
            self.root.deiconify()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')

    def toggle_fullscreen(self):
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
