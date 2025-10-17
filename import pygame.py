import pygame
import sys
import tkinter.messagebox
def show_message(title, message):
    #tkinter.messagebox.showinfo(title, message,type=OK)
   tkinter.messagebox.askyesnocancel("بله No Cansel", "askyesnocancel message", default=tkinter.messagebox.NO  )
# نمادهای بازی
PLAYER_X = 1
PLAYER_O = 2

# ابعاد صفحه نمایش
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

# ابعاد خانه‌های بازی
CELL_WIDTH = SCREEN_WIDTH // 3
CELL_HEIGHT = SCREEN_HEIGHT // 3

# رنگ‌ها
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BG_COLOR = WHITE

# تابعی برای رسم صفحه بازی


def draw_board():
    # پاک کردن صفحه
    screen.fill(BG_COLOR)

    # رسم خط‌های افقی
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_HEIGHT),
                     (SCREEN_WIDTH, CELL_HEIGHT))
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * CELL_HEIGHT),
                     (SCREEN_WIDTH, 2 * CELL_HEIGHT))

    # رسم خط‌های عمودی
    pygame.draw.line(screen, LINE_COLOR, (CELL_WIDTH, 0),
                     (CELL_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(screen, LINE_COLOR, (2 * CELL_WIDTH, 0),
                     (2 * CELL_WIDTH, SCREEN_HEIGHT))

    # رسم علامت‌ها
    for row in range(3):
        for col in range(3):
            if board[row][col] == PLAYER_X:
                draw_x(row, col)
            elif board[row][col] == PLAYER_O:
                draw_o(row, col)

# تابعی برای رسم علامت X


def draw_x(row, col):
    x = col * CELL_WIDTH + CELL_WIDTH // 2
    y = row * CELL_HEIGHT + CELL_HEIGHT // 2
    pygame.draw.line(screen, LINE_COLOR, (x - 20, y - 20), (x + 20, y + 20))
    pygame.draw.line(screen, LINE_COLOR, (x + 20, y - 20), (x - 20, y + 20))

# تابعی برای رسم علامت O


def draw_o(row, col):
    x = col * CELL_WIDTH + CELL_WIDTH // 2
    y = row * CELL_HEIGHT + CELL_HEIGHT // 2
    pygame.draw.circle(screen, LINE_COLOR, (x, y), 20, 2)

# تابعی برای بررسی وضعیت پیروزی


def check_win(player):
    # بررسی افقی
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    # بررسی عمودی
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True

    # بررسی قطر اصلی
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True

    # بررسی قطر فرعی
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False

# تابعی برای بررسی تساوی


def check_draw():
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

# تابعی برای پردازش کلیک کردن در خانه


def process_click(row, col):
    if board[row][col] != 0:
        return
    global turn
    if turn == PLAYER_X:
        board[row][col] = PLAYER_X
        if check_win(PLAYER_X):
            print("Player X wins!")
            show_message("Tic Tac Toe", "Player X wins!")
            pygame.quit()
            sys.exit()
            pygame.clear()
            sys.clear()
        elif check_draw():
            print("Draw!")
            pygame.quit()
            sys.exit()
        else:
            turn = PLAYER_O
    else:
        board[row][col] = PLAYER_O
        if check_win(PLAYER_O):
            print("Player O wins!")
            pygame.quit()
            sys.exit()
        elif check_draw():
            print("Draw!")
            pygame.quit()
            sys.exit()
        else:
            turn = PLAYER_X

    draw_board()


# ماتریسی برای نمایش وضعیت بازی
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# بازیکنی که نوبتش است
turn = PLAYER_X

# شروع نمایش بازی
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
draw_board()
pygame.display.update()

# حلقه‌ی اصلی بازی
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // CELL_HEIGHT
            clicked_col = mouse_pos[0] // CELL_WIDTH
            process_click(clicked_row, clicked_col)
            pygame.display.update()