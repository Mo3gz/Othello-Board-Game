import tkinter as tk
import subprocess
from GameBoard import OthelloGUI

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello Game")
        self.master.resizable(False, False)
        self.difficulty_value = tk.IntVar()
        self.strategy_value = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        # Create the title label
        tk.Label(self.master, text="Othello Game", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Create the difficulty buttons
        tk.Label(self.master, text="Select difficulty:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=20)
        tk.Radiobutton(self.master, text="Easy", variable=self.difficulty_value, value=1, font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=50, pady=5)
        tk.Radiobutton(self.master, text="Normal", variable=self.difficulty_value, value=3, font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=50, pady=5)
        tk.Radiobutton(self.master, text="Hard", variable=self.difficulty_value, value=5, font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=50, pady=5)
        
        # Create the start button
        tk.Button(self.master, text="Start", font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#8BC34A", activeforeground="white", command=self.startGame).grid(row=5, column=0, columnspan=2, pady=20)

    def startGame(self):
        # Get the value of the selected difficulty
        difficulty = self.difficulty_value.get()
        
        # Close the current window
        self.master.destroy()

        # Open the new window with OthelloGUI based on the selected difficulty
        root = tk.Tk()
        game = OthelloGUI(root, difficulty)
        root.mainloop()

# Create the main window and run the GUI
root = tk.Tk()
app = GUI(root)
root.mainloop()
