import tkinter as tk
from OthelloGame import OthelloGame

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello Game")
        self.master.geometry("200x350") 
        self.master.resizable(False, False)
        self.difficulty_value = tk.IntVar(value=1)  # Default to easy
        self.vs_computer = tk.BooleanVar(value=True)  # Default to vs computer
        self.create_widgets()

    def create_widgets(self):
        # Create the title label
        tk.Label(self.master, text="Othello Game", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Create the vs computer/user buttons
        tk.Label(self.master, text="Play against:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=20)
        tk.Radiobutton(self.master, text="Computer", variable=self.vs_computer, value=True, font=("Arial", 12), command=self.update_difficulty_visibility).grid(row=2, column=0, sticky="w", padx=50, pady=5)
        tk.Radiobutton(self.master, text="User", variable=self.vs_computer, value=False, font=("Arial", 12), command=self.update_difficulty_visibility).grid(row=3, column=0, sticky="w", padx=50, pady=5)

        # Create the difficulty buttons
        self.difficulty_label = tk.Label(self.master, text="Select difficulty:", font=("Arial", 12))
        self.difficulty_label.grid(row=4, column=0, sticky="w", padx=20)
        self.easy_rb = tk.Radiobutton(self.master, text="Easy", variable=self.difficulty_value, value=1, font=("Arial", 12))
        self.easy_rb.grid(row=5, column=0, sticky="w", padx=50, pady=5)
        self.normal_rb = tk.Radiobutton(self.master, text="Normal", variable=self.difficulty_value, value=2, font=("Arial", 12))
        self.normal_rb.grid(row=6, column=0, sticky="w", padx=50, pady=5)
        self.hard_rb = tk.Radiobutton(self.master, text="Hard", variable=self.difficulty_value, value=3, font=("Arial", 12))
        self.hard_rb.grid(row=7, column=0, sticky="w", padx=50, pady=5)

        # Create the start button
        tk.Button(self.master, text="Start", font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#8BC34A", activeforeground="white", command=self.startGame).grid(row=8, column=0, columnspan=2, pady=20)

        self.update_difficulty_visibility()

    def update_difficulty_visibility(self):
        if self.vs_computer.get():
            self.difficulty_label.grid()
            self.easy_rb.grid()
            self.normal_rb.grid()
            self.hard_rb.grid()
        else:
            self.difficulty_label.grid_remove()
            self.easy_rb.grid_remove()
            self.normal_rb.grid_remove()
            self.hard_rb.grid_remove()

    def startGame(self):
        # Get the value of the selected difficulty
        difficulty = self.difficulty_value.get()
        vs_computer = self.vs_computer.get()

        # Close the current window
        self.master.destroy()

        # Start the Othello game with the chosen settings
        game = OthelloGame(vs_computer=vs_computer, difficulty=difficulty)
        game.run()

# Create the main window and run the GUI
root = tk.Tk()
app = GUI(root)
root.mainloop()