import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 8
SCREEN_SIZE = 1000
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
HIGHLIGHT = (137, 0, 80)
AIHIGHLIGHT = (101, 168, 236)
BACKGROUND_COLOR = (151, 163, 147)
DELAY = 1500  # milliseconds

# Adjusted constants for table inside the frame
TABLE_OFFSET = 75
TABLE_SIZE = SCREEN_SIZE - 2 * TABLE_OFFSET
SQUARE_SIZE = TABLE_SIZE // BOARD_SIZE

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

class OthelloGame:
    def __init__(self, vs_computer=True, difficulty=1):
        # Initialize the game board with the starting position
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)  # Create an empty board
        self.board[3, 3] = self.board[4, 4] = 1  # Place initial white pieces
        self.board[3, 4] = self.board[4, 3] = -1  # Place initial black pieces
        self.vs_computer = vs_computer  # Set whether the game is against the computer
        self.difficulty = difficulty  # Set the difficulty level of the AI
        self.current_player = -1  # Set the current player (-1 for black, 1 for white)
        self.ai_move_time = 0  # Initialize the AI move time
        self.game_over = False  # Initialize the game over state
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), pygame.RESIZABLE)  # Create the game window
        pygame.display.set_caption('Othello Game')  # Set the window caption
        self.block_user_input = False  # Initialize the user input block state
        self.background_image = pygame.image.load('neon_frame.jpg')  # Load the background image
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_SIZE, SCREEN_SIZE))  # Resize the background image to fit the window
        self.ai_last_move = None  # To store the AI's last move

    def draw_board(self):
        # Draw the game board
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image
        for row in range(BOARD_SIZE):  # Loop through each row
            for col in range(BOARD_SIZE):  # Loop through each column
                pygame.draw.rect(self.screen, BLACK, (TABLE_OFFSET + col * SQUARE_SIZE, TABLE_OFFSET + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)  # Draw the square borders
                if self.board[row, col] == 1:  # Check if the cell has a white piece
                    pygame.draw.circle(self.screen, WHITE, (TABLE_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2, TABLE_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 4)  # Draw white piece
                elif self.board[row, col] == -1:  # Check if the cell has a black piece
                    pygame.draw.circle(self.screen, BLACK, (TABLE_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2, TABLE_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 4)  # Draw black piece
        if self.ai_last_move:  # If there is an AI's last move
            row, col = self.ai_last_move
            pygame.draw.rect(self.screen, AIHIGHLIGHT, (TABLE_OFFSET + col * SQUARE_SIZE - 4, TABLE_OFFSET + row * SQUARE_SIZE - 4, SQUARE_SIZE + 8, SQUARE_SIZE + 8), 5)  # Draw a 4px black border around the AI's last move

    def get_valid_moves(self, board, player):
        # Get all valid moves for the current player
        valid_moves = []  # Initialize the list of valid moves
        for row in range(BOARD_SIZE):  # Loop through each row
            for col in range(BOARD_SIZE):  # Loop through each column
                if board[row, col] == 0:  # Check if the cell is empty
                    for dr in range(-1, 2):  # Loop through the row directions (-1, 0, 1)
                        for dc in range(-1, 2):  # Loop through the column directions (-1, 0, 1)
                            if dr == 0 and dc == 0:  # Skip the direction (0, 0)
                                continue
                            r, c = row + dr, col + dc  # Calculate the new row and column
                            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == -player:  # Check if the new cell has the opponent's piece
                                while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == -player:  # Continue in the direction while the cell has the opponent's piece
                                    r += dr  # Update the row
                                    c += dc  # Update the column
                                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == player:  # Check if the new cell has the player's piece
                                    valid_moves.append((row, col))  # Add the move to the list of valid moves
                                    break  # Break the loop
        return valid_moves  # Return the list of valid moves

    def make_move(self, board, row, col, player):
        # Place a piece on the board and flip the opponent's pieces
        board[row, col] = player  # Place the player's piece on the board
        if player == 1:  # If the player is AI
            self.ai_last_move = (row, col)  # Store the AI's last move
        for dr in range(-1, 2):  # Loop through the row directions (-1, 0, 1)
            for dc in range(-1, 2):  # Loop through the column directions (-1, 0, 1)
                if dr == 0 and dc == 0:  # Skip the direction (0, 0)
                    continue
                r, c = row + dr, col + dc  # Calculate the new row and column
                if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == -player:  # Check if the new cell has the opponent's piece
                    potential_flip = []  # Initialize the list of potential flips
                    while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == -player:  # Continue in the direction while the cell has the opponent's piece
                        potential_flip.append((r, c))  # Add the cell to the list of potential flips
                        r += dr  # Update the row
                        c += dc  # Update the column
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r, c] == player:  # Check if the new cell has the player's piece
                        for flip_r, flip_c in potential_flip:  # Loop through the potential flips
                            board[flip_r, flip_c] = player  # Flip the opponent's piece to the player's piece

    def minimax(self, board, depth, maximizing_player):
        # Minimax algorithm to calculate the best move for the AI
        if depth == 0 or (not self.get_valid_moves(board, 1) and not self.get_valid_moves(board, -1)):  # Check if the maximum depth is reached or there are no valid moves
            return np.sum(board)  # Return the board evaluation

        if maximizing_player:  # If the current player is maximizing
            max_eval = -float('inf')  # Initialize the maximum evaluation
            for move in self.get_valid_moves(board, 1):  # Loop through each valid move for the maximizing player
                new_board = board.copy()  # Create a copy of the board
                self.make_move(new_board, move[0], move[1], 1)  # Make the move on the new board
                eval = self.minimax(new_board, depth - 1, False)  # Recursively call minimax for the minimizing player
                max_eval = max(max_eval, eval)  # Update the maximum evaluation
            return max_eval  # Return the maximum evaluation
        else:  # If the current player is minimizing
            min_eval = float('inf')  # Initialize the minimum evaluation
            for move in self.get_valid_moves(board, -1):  # Loop through each valid move for the minimizing player
                new_board = board.copy()  # Create a copy of the board
                self.make_move(new_board, move[0], move[1], -1)  # Make the move on the new board
                eval = self.minimax(new_board, depth - 1, True)  # Recursively call minimax for the maximizing player
                min_eval = min(min_eval, eval)  # Update the minimum evaluation
            return min_eval  # Return the minimum evaluation

    def draw_valid_moves(self, valid_moves):
        # Draw circles to indicate valid moves
        for move in valid_moves:  # Loop through each valid move
            row, col = move  # Get the row and column of the move
            pygame.draw.circle(self.screen, HIGHLIGHT, (TABLE_OFFSET + col * SQUARE_SIZE + SQUARE_SIZE // 2, TABLE_OFFSET + row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 4)  # Draw the circle to highlight the valid move

    def calculate_scores(self):
        white_score = np.sum(self.board == 1)  # Calculate the white score
        black_score = np.sum(self.board == -1)  # Calculate the black score
        return white_score, black_score  # Return the scores

    def draw_scores(self):
        # Calculate the scores for both players
        white_score, black_score = self.calculate_scores()
        # Render the black score text
        text_black = font.render(f'Black: {black_score}', True, BLACK)
        # Render the white score text
        text_white = font.render(f'White: {white_score}', True, BLACK)
        # Render the current turn text
        turn_text = font.render(f'Turn: {"Black" if self.current_player == -1 else "White"}', True, BLACK)

        # Create a surface for each text with alpha channel
        text_black_surface = pygame.Surface((text_black.get_width(), text_black.get_height()), pygame.SRCALPHA)
        text_white_surface = pygame.Surface((text_white.get_width(), text_white.get_height()), pygame.SRCALPHA)
        turn_text_surface = pygame.Surface((turn_text.get_width(), turn_text.get_height()), pygame.SRCALPHA)

        # Fill the surfaces with a transparent color
        text_black_surface.fill((255, 255, 255, 0))  # Fully transparent
        text_white_surface.fill((255, 255, 255, 0))  # Fully transparent
        turn_text_surface.fill((255, 255, 255, 0))   # Fully transparent

        # Blit the text onto the surfaces
        text_black_surface.blit(text_black, (0, 0))
        text_white_surface.blit(text_white, (0, 0))
        turn_text_surface.blit(turn_text, (0, 0))

        # Draw the surfaces with the text on the main screen
        self.screen.blit(text_black_surface, (10, 10))
        self.screen.blit(text_white_surface, (SCREEN_SIZE - text_white.get_width() - 10, 10))
        self.screen.blit(turn_text_surface, (SCREEN_SIZE // 2 - turn_text.get_width() // 2, 10))

    def check_winner(self):
        # Calculate the scores for both players
        white_score, black_score = self.calculate_scores()
        # Determine the winner based on the scores
        if white_score > black_score:
            winner_text = "White wins!"
        elif black_score > white_score:
            winner_text = "Black wins!"
        else:
            winner_text = "It's a tie!"
        # Render the winner text
        text = large_font.render(winner_text, True, RED, BACKGROUND_COLOR)
        # Draw the winner text on the screen
        self.screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() // 2))

    def run(self):
        # Create a clock object to manage the frame rate
        clock = pygame.time.Clock()
        # Set the running flag to True
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game loop if the QUIT event is triggered
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle the window resize event
                    global SCREEN_SIZE, TABLE_SIZE, SQUARE_SIZE, TABLE_OFFSET
                    SCREEN_SIZE = min(event.w, event.h)
                    TABLE_SIZE = SCREEN_SIZE - 2 * TABLE_OFFSET
                    SQUARE_SIZE = TABLE_SIZE // BOARD_SIZE
                    self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), pygame.RESIZABLE)
                    self.background_image = pygame.transform.scale(self.background_image, (SCREEN_SIZE, SCREEN_SIZE))  # Resize the background image to fit the new window size
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and not self.block_user_input:
                    # Handle mouse button down events
                    x, y = pygame.mouse.get_pos()
                    if TABLE_OFFSET <= x < SCREEN_SIZE - TABLE_OFFSET and TABLE_OFFSET <= y < SCREEN_SIZE - TABLE_OFFSET:  # Ensure clicks are within the table area
                        row, col = (y - TABLE_OFFSET) // SQUARE_SIZE, (x - TABLE_OFFSET) // SQUARE_SIZE
                        if (row, col) in self.get_valid_moves(self.board, self.current_player):
                            # Make the move if it's a valid one
                            self.make_move(self.board, row, col, self.current_player)
                            # Switch to the other player or AI
                            self.current_player = -self.current_player
                            if self.vs_computer and self.current_player == 1:
                                # Set AI move time and block user input during AI's turn
                                self.ai_move_time = pygame.time.get_ticks() + DELAY
                                self.block_user_input = True

            if self.vs_computer and self.current_player == 1 and not self.game_over:
                # Handle the AI's turn
                if pygame.time.get_ticks() >= self.ai_move_time:
                    best_move = None
                    best_value = -float('inf')
                    for move in self.get_valid_moves(self.board, 1):
                        new_board = self.board.copy()
                        self.make_move(new_board, move[0], move[1], 1)
                        move_value = self.minimax(new_board, self.difficulty, False)
                        if move_value > best_value:
                            best_value = move_value
                            best_move = move
                    if best_move:
                        # Make the best move for the AI
                        self.make_move(self.board, best_move[0], best_move[1], 1)
                        # Switch back to the user
                        self.current_player = -1
                    else:
                        # If no valid moves for AI, switch back to the user
                        self.current_player = -1
                    # Allow user input after AI's turn
                    self.block_user_input = False

            # Check if the current player has no valid moves
            if not self.get_valid_moves(self.board, self.current_player):
                if not self.get_valid_moves(self.board, -self.current_player):
                    # No valid moves for both players, game ends
                    self.game_over = True
                else:
                    # Switch to the other player
                    self.current_player = -self.current_player

            # Draw the game board
            self.draw_board()
            if not self.game_over:
                # Highlight valid moves for the current player if it's the user
                if self.current_player == -1 or not self.vs_computer:
                    self.draw_valid_moves(self.get_valid_moves(self.board, self.current_player))
            # Draw the scores
            self.draw_scores()
            if self.game_over:
                # Check and display the winner
                self.check_winner()
            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            clock.tick(FPS)

        # Quit Pygame and exit the program
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    OthelloGame().run()
