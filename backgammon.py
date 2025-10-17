import pygame
import random
import json

# تنظیمات اولیه
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Backgammon Game")

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# بارگذاری تصاویر
white_piece_img = pygame.image.load("white_piece.png")
black_piece_img = pygame.image.load("black_piece.png")
board_img = pygame.image.load("board.png")

# تنظیمات تخته
BOARD_WIDTH = 800
BOARD_HEIGHT = 600

# رسم تخته
def draw_board():
    screen.blit(board_img, (0, 0))
    font = pygame.font.Font(None, 48)
    title_text = font.render("Backgammon", True, BLACK)
    screen.blit(title_text, (width // 2 - 100, 20))

# رسم مهره‌ها
def draw_pieces(white_positions, black_positions):
    for pos in white_positions:
        screen.blit(white_piece_img, (pos * (BOARD_WIDTH // 24) + (BOARD_WIDTH // 48) - 15, BOARD_HEIGHT // 4 - 15))
    for pos in black_positions:
        screen.blit(black_piece_img, (pos * (BOARD_WIDTH // 24) + (BOARD_WIDTH // 48) - 15, (3 * BOARD_HEIGHT) // 4 - 15))

# نمایش تعداد مهره‌ها
def display_piece_count(white_count, black_count):
    font = pygame.font.Font(None, 36)
    white_text = font.render(f"White Pieces: {white_count}", True, BLACK)
    black_text = font.render(f"Black Pieces: {black_count}", True, BLACK)
    screen.blit(white_text, (10, 10))
    screen.blit(black_text, (10, 40))

# نوبت بازیکن
def switch_turn(turn):
    return 'black' if turn == 'white' else 'white'

# بررسی حرکت مجاز
def is_valid_move(start, end, turn, white_positions, black_positions):
    if turn == 'white':
        if start not in white_positions:
            return False
        if end in black_positions and black_positions.count(end) > 1:
            return False
    else:
        if start not in black_positions:
            return False
        if end in white_positions and white_positions.count(end) > 1:
            return False
    return True

# حرکت مهره
def move_piece(start, end, turn, white_positions, black_positions):
    if turn == 'white':
        white_positions.remove(start)
        white_positions.append(end)
    else:
        black_positions.remove(start)
        black_positions.append(end)

# بررسی برنده
def check_winner(white_positions, black_positions):
    if not black_positions:
        return "White wins!"
    elif not white_positions:
        return "Black wins!"
    return None

# پرتاب تاس
def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

# سیستم امتیازدهی
def update_score(winner, scores):
    if winner == "White wins!":
        scores['white'] += 1
    elif winner == "Black wins!":
        scores['black'] += 1

# ذخیره وضعیت بازی
def save_game(white_positions, black_positions, turn, scores, dice_roll):
    game_state = {
        'white_positions': white_positions,
        'black_positions': black_positions,
        'turn': turn,
        'scores': scores,
        'dice_roll': dice_roll,
    }
    with open("backgammon_save.json", "w") as f:
        json.dump(game_state, f)
    save_history(turn, scores)

# بارگذاری وضعیت بازی
def load_game():
    with open("backgammon_save.json", "r") as f:
        game_state = json.load(f)
    return game_state['white_positions'], game_state['black_positions'], game_state['turn'], game_state['scores'], game_state['dice_roll']

# ذخیره تاریخچه بازی
def save_history(turn, scores):
    history_entry = {
        'turn': turn,
        'scores': scores,
    }
    with open("game_history.json", "a") as f:
        json.dump(history_entry, f)
        f.write("\n")  # هر ورودی در خط جدید

# نمایش پیام تأیید
def display_message(msg):
    font = pygame.font.Font(None, 36)
    text = font.render(msg, True, BLACK)
    screen.blit(text, (width // 2 - 100, height // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# تابع اصلی
def main():
    white_positions = list(range(1, 7))  # مهره‌های سفید در خانه‌های 1 تا 6
    black_positions = list(range(19, 25))  # مهره‌های سیاه در خانه‌های 19 تا 24
    turn = 'white'  # نوبت بازیکن سفید
    selected_piece = None
    dice_roll = (0, 0)
    scores = {'white': 0, 'black': 0}

    running = True
    while running:
        draw_board()
        draw_pieces(white_positions, black_positions)

        # نمایش تعداد مهره‌ها
        display_piece_count(len(white_positions), len(black_positions))

        # نمایش امتیاز
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score - White: {scores['white']} | Black: {scores['black']}", True, BLACK)
        screen.blit(score_text, (10, 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # ذخیره بازی
                    save_game(white_positions, black_positions, turn, scores, dice_roll)
                    display_message("Game saved!")
                elif event.key == pygame.K_l:  # بارگذاری بازی
                    white_positions, black_positions, turn, scores, dice_roll = load_game()
                    display_message("Game loaded!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                clicked_pos = mouse_x // (BOARD_WIDTH // 24) + 1

                if selected_piece is None:
                    if turn == 'white' and clicked_pos in white_positions:
                        selected_piece = clicked_pos
                    elif turn == 'black' and clicked_pos in black_positions:
                        selected_piece = clicked_pos
                else:
                    if is_valid_move(selected_piece, clicked_pos, turn, white_positions, black_positions):
                        move_piece(selected_piece, clicked_pos, turn, white_positions, black_positions)
                        selected_piece = None
                        turn = switch_turn(turn)

        # نوبت‌گیری با تاس
        if dice_roll == (0, 0):
            dice_roll = roll_dice()
            print(f"Dice rolled: {dice_roll}")

        winner = check_winner(white_positions, black_positions)
        if winner:
            update_score(winner, scores)
            font = pygame.font.Font(None, 74)
            text = font.render(winner, True, RED)
            screen.blit(text, (width // 2 - 100, height // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()

    pygame.quit()

# شروع برنامه
if __name__ == "__main__":
    main()
