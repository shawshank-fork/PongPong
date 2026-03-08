import tkinter as tk
import math

HUMAN, AI = "X", "O"
board = [" "] * 9
buttons = []

def check_winner():
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    return "Draw" if " " not in board else None

def minimax(is_max):
    result = check_winner()
    if result == AI: return 1
    if result == HUMAN: return -1
    if result == "Draw": return 0

    best = -math.inf if is_max else math.inf
    for i in range(9):
        if board[i] == " ":
            board[i] = AI if is_max else HUMAN
            score = minimax(not is_max)
            board[i] = " "
            best = max(best, score) if is_max else min(best, score)
    return best

def ai_move():
    best_score, move = -math.inf, None
    for i in range(9):
        if board[i] == " ":
            board[i] = AI
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    if move is not None:
        update_button(move, AI)

def update_button(i, player):
    board[i] = player
    buttons[i]["text"] = player
    buttons[i]["state"] = "disabled"

def on_click(i):
    if board[i] == " ":
        update_button(i, HUMAN)
        if not game_over():
            ai_move()
            game_over()

def game_over():
    result = check_winner()
    if result:
        status.config(text="Draw!" if result=="Draw" else f"{result} Wins!")
        for b in buttons: b["state"] = "disabled"
        return True
    return False

def reset():
    global board
    board = [" "] * 9
    status.config(text="Your Turn (X)")
    for b in buttons:
        b["text"], b["state"] = "", "normal"

# GUI
root = tk.Tk()
root.title("Tic Tac Toe - Minimax")
root.geometry("330x420")

status = tk.Label(root, text="Your Turn (X)", font=("Arial", 14))
status.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, font=("Arial", 24),
                    width=4, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

tk.Button(root, text="Reset", command=reset).pack(pady=15)

root.mainloop()