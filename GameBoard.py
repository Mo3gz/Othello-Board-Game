import tkinter as tk
from tkinter import messagebox

class OthelloGUI:
    def __init__(self, master, difficultyLevel):
        self.master = master
        self.difficultyLevel = difficultyLevel
        self.master.title("Othello")
        self.master.resizable(False, False)
        
        self.canvas = tk.Canvas(master, width=800, height=800, bg="#3EB489")
        self.canvas.pack()
        
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        
        self.draw_board()
        
        self.turn = 'B'  # 'B' for black (user), 'W' for white (computer)
        self.black_counter_label = tk.Label(master, text="Black Player: 2", bg="#3EB489", fg="white")
        self.black_counter_label.pack(side='left', padx=90) 
        self.turn_label = tk.Label(master, text="Turn: Black", bg="#3EB489", fg="white")
        self.turn_label.pack(side='left', padx=90)
        self.white_counter_label = tk.Label(master, text="White Player: 2", bg="#3EB489", fg="white")
        self.white_counter_label.pack(side='left', padx=90)
        
        self.show_valid_moves() 

        self.canvas.bind("<Button-1>", self.place_piece)

        print(self.difficultyLevel)

        
    def draw_board(self):
        self.canvas.delete("pieces")
        for row in range(8):
            for col in range(8):
                x1 = col * 100
                y1 = row * 100
                x2 = x1 + 100
                y2 = y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, tags="pieces")
                if self.board[row][col] == 'B':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black", tags="pieces")
                elif self.board[row][col] == 'W':
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white", tags="pieces")
    
    def valid_move(self, row, col):
        # Check if the cell is empty
        if self.board[row][col] != ' ':
            return False

        # Iterate over all directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # Skip the case where both dr and dc are 0
                if dr == 0 and dc == 0:
                    continue

                # Check adjacent cells in the current direction
                nr, nc = row + dr, col + dc
                while 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] != ' ' and self.board[nr][nc] != self.turn:
                    nr += dr
                    nc += dc

                # If a valid sequence of opponent pieces ends with the current player's piece, the move is valid
                if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] == self.turn and (nr != row + dr or nc != col + dc):
                    return True

        return False

    def show_valid_moves(self):
        self.canvas.delete("valid_moves")
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == ' ' and self.valid_move(row, col):
                    x1 = col * 100 + 10
                    y1 = row * 100 + 10
                    x2 = x1 + 80
                    y2 = y1 + 80
                    self.canvas.create_oval(x1, y1, x2, y2, fill=self.canvas['bg'], outline="black", width=3, tags="valid_moves")

    def place_piece(self, event):
        col = event.x // 100
        row = event.y // 100
        
        if self.board[row][col] == ' ' and self.valid_move(row, col):
            self.board[row][col] = self.turn
            self.update_board(row, col)
            self.switch_turn()
            self.show_valid_moves() 
        else:
            messagebox.showerror("Invalid Move", "Invalid move! Please try again.")

    
    def update_board(self, row, col):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                while 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] != ' ' and self.board[nr][nc] != self.turn:
                    nr += dr
                    nc += dc
                    if 0 <= nr < 8 and 0 <= nc < 8 and self.board[nr][nc] == self.turn:
                        while nr != row or nc != col:
                            nr -= dr
                            nc -= dc
                            self.board[nr][nc] = self.turn
                        break
        self.draw_board()
    
    def switch_turn(self):
        self.check_winner()
        if self.turn == 'B':
            self.turn = 'W'
            self.turn_label.config(text="Turn: White")
            if not self.check_exist_valid_move():
                self.switch_turn()

            # Call function here to get position of computer move
            
            # Choose a move for the computer
            # move = self.get_computer_move(self.difficultyLevel)
            # if move:
            #     self.board[move[0]][move[1]] = self.turn
            #     self.update_board(move[0], move[1])
            #     self.switch_turn()  # Switch back to the user's turn
            #     self.show_valid_moves()
        else:
            self.turn = 'B'
            self.turn_label.config(text="Turn: Black")
            if not self.check_exist_valid_move():
                self.switch_turn()
        
        # Count the number of black and white pieces after each turn
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        
        # Update the counter labels
        self.black_counter_label.config(text="Black Player:: " + str(black_count))
        self.white_counter_label.config(text="White Player: " + str(white_count))
        
        

    def check_exist_valid_move(self):
        for row in range(8):
            for col in range(8):
                if self.valid_move(row,col):
                    return True
        return False        

    def check_winner(self):
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)

        if black_count + white_count == 64:
            if black_count > white_count:
                winner = "Black"
            elif white_count > black_count:
                winner = "White"
            else:
                winner = "It's a draw"
            
            # Display the winner
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
            self.master.destroy()  # Close the window after displaying the message

def main():
    root = tk.Tk()
    game = OthelloGUI(root, 5)
    root.mainloop()

if __name__ == "__main__":
    main()
