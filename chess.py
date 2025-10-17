import pygame
import numpy as np
import pickle

# تنظیمات اولیه
pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")

# رنگ‌ها
white = (255, 255, 255)
black = (0, 0, 0)

# بارگذاری مهره‌ها
pieces = {}
for color in ['w', 'b']:
    for piece in ['K', 'Q', 'R', 'B', 'N', 'P']:
        pieces[f"{color}{piece}"] = pygame.transform.scale(pygame.image.load(f'images/{color}{piece}.png'), (100, 100))

# رسم تخته شطرنج
def draw_board():
    for i in range(8):
        for j in range(8):
            color = white if (i + j) % 2 == 0 else black
            pygame.draw.rect(screen, color, (j * 100, i * 100, 100, 100))

# قرار دادن مهره‌ها
def draw_pieces(board):
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece != "--":
                screen.blit(pieces[piece], (j * 100, i * 100))

# تابع برای بررسی حرکات مهره‌ها
def is_valid_move(board, start, end, player_color):
    start_piece = board[start[0]][start[1]]
    target_piece = board[end[0]][end[1]]

    if target_piece[0] == player_color:  # اگر مهره خودی باشد
        return False

    # قوانین حرکات مهره‌ها
    if start_piece[1] == 'K':
        return abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1

    if start_piece[1] == 'Q':
        return (start[0] == end[0] or start[1] == end[1] or
                abs(start[0] - end[0]) == abs(start[1] - end[1]))

    if start_piece[1] == 'R':
        return start[0] == end[0] or start[1] == end[1]

    if start_piece[1] == 'B':
        return abs(start[0] - end[0]) == abs(start[1] - end[1])

    if start_piece[1] == 'N':
        return (abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1) or \
               (abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2)

    if start_piece[1] == 'P':
        direction = -1 if player_color == 'w' else 1
        if start[1] == end[1]:  # حرکت جلو
            if board[end[0]][end[1]] == "--":
                return (end[0] - start[0] == direction)
            else:  # حمله
                return (end[0] - start[0] == direction and abs(start[1] - end[1]) == 1)

    return False

# تابع برای بررسی وضعیت کیش و کیش مات
def is_in_check(board, player_color):
    king_pos = None
    for i in range(8):
        for j in range(8):
            if board[i][j] == player_color + 'K':
                king_pos = (i, j)
                break

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece[0] != player_color and piece != '--':
                if is_valid_move(board, (i, j), king_pos, piece[0]):
                    return True
    return False

def is_checkmate(board, player_color):
    # بررسی کیش مات
    if not is_in_check(board, player_color):
        return False

    for i in range(8):
        for j in range(8):
            if board[i][j][0] == player_color:  # اگر مهره متعلق به بازیکن باشد
                for x in range(8):
                    for y in range(8):
                        if is_valid_move(board, (i, j), (x, y), player_color):
                            # شبیه‌سازی حرکت و بررسی وضعیت جدید
                            temp_board = [row[:] for row in board]
                            temp_board[x][y] = temp_board[i][j]
                            temp_board[i][j] = "--"
                            if not is_in_check(temp_board, player_color):
                                return False
    return True

# تابع برای ذخیره بازی
def save_game(board, player_color):
    with open('saved_game.pkl', 'wb') as f:
        pickle.dump((board, player_color), f)

# تابع برای بارگذاری بازی
def load_game():
    with open('saved_game.pkl', 'rb') as f:
        return pickle.load(f)

# تابع اصلی بازی
def main():
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    history = []
    running = True
    player_color = 'w'
    selected_piece = None

    while running:
        draw_board()
        draw_pieces(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # ذخیره بازی
                    save_game(board, player_color)
                if event.key == pygame.K_l:  # بارگذاری بازی
                    board, player_color = load_game()
                if event.key == pygame.K_u:  # Undo
                    if history:
                        board, player_color = history.pop()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // 100
                row = mouse_y // 100

                if selected_piece is None:  # انتخاب مهره
                    if board[row][col][0] == player_color:  # مهره خودی
                        selected_piece = (row, col)
                else:  # حرکت مهره
                    if is_valid_move(board, selected_piece, (row, col), player_color):
                        history.append((board, player_color))  # ذخیره وضعیت قبل از حرکت
                        board[row][col] = board[selected_piece[0]][selected_piece[1]]
                        board[selected_piece[0]][selected_piece[1]] = "--"
                        if is_in_check(board, 'w' if player_color == 'b' else 'b'):  # بررسی کیش
                            print(f"{'Black' if player_color == 'w' else 'White'} is in check!")

                        if is_checkmate(board, 'w' if player_color == 'b' else 'b'):
                            print(f"{'Black' if player_color == 'w' else 'White'} is checkmate!")
                            running = False

                        selected_piece = None
                        player_color = 'b' if player_color == 'w' else 'w'  # تغییر نوبت

        pygame.display.flip()

    pygame.quit()

# شروع برنامه
if __name__ == "__main__":
    main()
