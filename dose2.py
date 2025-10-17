import tkinter as tk

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def on_click(row, col):
    global turn, board, buttons

    if board[row][col] == " ":
        player = players[turn % 2]
        board[row][col] = player
        buttons[row][col].config(text=player)

        if check_winner(board, player):
            winner_label.config(text=f"Player {player} wins!")
            disable_buttons()
        elif all(all(cell != " " for cell in row) for row in board):
            winner_label.config(text="It's a tie!")
            disable_buttons()
        
        turn += 1

def disable_buttons():
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(state=tk.DISABLED)

root = tk.Tk()
root.title("Tic-Tac-Toe")

board = [[" " for _ in range(3)] for _ in range(3)]
players = ["X", "O"]
turn = 0

buttons = []
for row in range(3):
    button_row = []
    for col in range(3):
        button = tk.Button(root, text=" ", width=10, height=3, command=lambda r=row, c=col: on_click(r, c))
        button.grid(row=row, column=col)
        button_row.append(button)
    buttons.append(button_row)

winner_label = tk.Label(root, text="")
winner_label.grid(row=3, columnspan=3)

root.mainloop()
