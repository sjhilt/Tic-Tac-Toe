"""
Tic-Tac-Toe with AI and Score Tracking
Author: Stephen Hilt
Date: 03-2025
Description: A Python-based Tic-Tac-Toe game with an AI opponent.
Features:
    - AI opponent using Minimax algorithm
    - AI has a 10% chance to make a mistake (random move)
    - Score tracking for Player (X) and AI (O)
    - Restart button without resetting scores
"""

import tkinter as tk
from tkinter import messagebox
import random

# Initialize game variables
current_player = "X"  # Human player starts
board = [""] * 9  # Empty board representation
buttons = []  # Holds the button references
mistake_chance = 0.1  # 10% chance of AI making a mistake

# Score tracking
player_wins = 0
ai_wins = 0

def player_move(index):
    """Handles the player's move when a button is clicked."""
    global current_player

    # Ensure move is valid and game is not over
    if board[index] == "" and not check_winner():
        board[index] = current_player
        buttons[index].config(text=current_player, state="disabled")

        # Check if the player has won
        winner = check_winner()
        if winner:
            highlight_winner(winner)
            update_score(current_player)
            messagebox.showinfo("Game Over", f"Player {current_player} Wins!")
            return

        # Check for a draw
        if "" not in board:
            messagebox.showinfo("Game Over", "It's a Draw!")
            return

        # Switch to AI turn
        current_player = "O"
        root.after(500, ai_move)  # Add delay for AI move

def ai_move():
    """Handles the AI move with Minimax and random mistakes."""
    global current_player

    # AI makes a mistake with the given probability
    if random.random() < mistake_chance:
        available_moves = [i for i in range(9) if board[i] == ""]
        best_move = random.choice(available_moves)  # AI picks a random move
    else:
        best_move = get_best_move()  # AI uses Minimax normally

    if best_move is not None:
        board[best_move] = "O"
        buttons[best_move].config(text="O", state="disabled")

    # Check if AI has won
    winner = check_winner()
    if winner:
        highlight_winner(winner)
        update_score("O")
        messagebox.showinfo("Game Over", "AI Wins! 🤖")
        return

    # Check for a draw
    if "" not in board:
        messagebox.showinfo("Game Over", "It's a Draw!")
        return

    # Switch back to human turn
    current_player = "X"

def get_best_move():
    """Finds the best move for AI using the Minimax algorithm."""
    best_score = -float("inf")
    best_move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i

    return best_move

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to determine the best move for AI."""
    result = evaluate(board)
    if result is not None:
        return result

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

def evaluate(board):
    """Evaluates the board state to check for winners."""
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c]:
            if board[a] == "O":
                return 10  # AI wins
            elif board[a] == "X":
                return -10  # Human wins

    if "" not in board:
        return 0  # Draw

    return None

def check_winner():
    """Checks if there's a winner and returns the winning combination."""
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    
    for combo in winning_combinations:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != "":
            return combo  # Return winning combination indices
    
    return None

def update_score(winner):
    """Updates the score display for Player and AI."""
    global player_wins, ai_wins
    if winner == "X":
        player_wins += 1
    elif winner == "O":
        ai_wins += 1
    player_score_label.config(text=f"Player Wins: {player_wins}")
    ai_score_label.config(text=f"AI Wins: {ai_wins}")

def highlight_winner(combo):
    """Highlights the winning combination in green."""
    for index in combo:
        buttons[index].config(bg="lightgreen")

def restart_game():
    """Resets the board but keeps the score."""
    global current_player, board
    current_player = "X"
    board = [""] * 9
    for button in buttons:
        button.config(text="", bg="white", state="normal")

# Create the game window
root = tk.Tk()
root.title("Tic-Tac-Toe (AI Mode)")

# Create the Tic-Tac-Toe buttons
for i in range(9):
    button = tk.Button(root, text="", font=("Arial", 24), height=2, width=5, 
                       bg="white", command=lambda i=i: player_move(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

# Score labels
player_score_label = tk.Label(root, text="Player Wins: 0", font=("Arial", 14))
player_score_label.grid(row=3, column=0, columnspan=1)

ai_score_label = tk.Label(root, text="AI Wins: 0", font=("Arial", 14))
ai_score_label.grid(row=3, column=2, columnspan=1)

# Add Restart button
restart_button = tk.Button(root, text="Restart", font=("Arial", 14), command=restart_game)
restart_button.grid(row=4, column=0, columnspan=3)

# Run the game loop
root.mainloop()
