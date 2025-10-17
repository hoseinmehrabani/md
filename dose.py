def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

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

def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    turn = 0

    while True:
        print_board(board)

        player = players[turn % 2]
        row = int(input(f"Player {player}, enter your row (0, 1, 2): "))
        col = int(input(f"Player {player}, enter your column (0, 1, 2): "))

        if board[row][col] != " ":
            print("That position is already taken. Try again.")
            continue

        board[row][col] = player

        if check_winner(board, player):
            print_board(board)
            print(f"Player {player} wins!")
            break

        if all(all(cell != " " for cell in row) for row in board):
            print_board(board)
            print("It's a tie!")
            break

        turn += 1

if __name__ == "__main__":
    tic_tac_toe()
