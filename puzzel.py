import pygame
import random

# تنظیمات اولیه
pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Puzzle Game")

# رنگ‌ها
white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)


# منوی اصلی
def main_menu():
    while True:
        screen.fill(white)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Select Puzzle Type:", True, black)
        screen.blit(title_text, (80, 50))

        options = ["1. Number Puzzle", "2. Image Puzzle", "3. Logic Puzzle"]
        for idx, option in enumerate(options):
            text = font.render(option, True, black)
            screen.blit(text, (80, 100 + idx * 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    number_puzzle()
                elif event.key == pygame.K_2:
                    image_puzzle()  # پیاده‌سازی این قسمت در آینده
                elif event.key == pygame.K_3:
                    logic_puzzle()  # پیاده‌سازی این قسمت در آینده
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 80 <= mouse_x <= 320 and 100 <= mouse_y <= 140:  # Number Puzzle
                    number_puzzle()
                elif 80 <= mouse_x <= 320 and 140 <= mouse_y <= 180:  # Image Puzzle
                    image_puzzle()  # پیاده‌سازی این قسمت در آینده
                elif 80 <= mouse_x <= 320 and 180 <= mouse_y <= 220:  # Logic Puzzle
                    logic_puzzle()  # پیاده‌سازی این قسمت در آینده

        pygame.display.flip()


# ۱. پازل عددی
def create_number_puzzle():
    numbers = list(range(1, 9)) + [0]
    random.shuffle(numbers)
    return [numbers[i:i + 3] for i in range(0, 9, 3)]


def draw_number_puzzle(puzzle, moves):
    screen.fill(white)
    for i in range(3):
        for j in range(3):
            num = puzzle[i][j]
            rect = pygame.Rect(j * 100, i * 100, 100, 100)
            pygame.draw.rect(screen, grey if num == 0 else black, rect)
            if num != 0:
                font = pygame.font.Font(None, 74)
                text = font.render(str(num), True, white)
                screen.blit(text, (j * 100 + 30, i * 100 + 20))

    # نمایش تعداد حرکات
    font = pygame.font.Font(None, 36)
    moves_text = font.render(f'Moves: {moves}', True, black)
    screen.blit(moves_text, (10, 10))


def check_win(puzzle):
    correct = list(range(1, 9)) + [0]
    return puzzle == [correct[i:i + 3] for i in range(0, 9, 3)]


def move_tile(puzzle, empty_pos, tile_pos):
    puzzle[empty_pos[0]][empty_pos[1]], puzzle[tile_pos[0]][tile_pos[1]] = (
        puzzle[tile_pos[0]][tile_pos[1]], puzzle[empty_pos[0]][empty_pos[1]]
    )


def number_puzzle():
    puzzle = create_number_puzzle()
    empty_pos = (2, 2)
    moves = 0

    while True:
        draw_number_puzzle(puzzle, moves)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                tile_pos = (mouse_y // 100, mouse_x // 100)
                if (0 <= tile_pos[0] < 3) and (0 <= tile_pos[1] < 3):
                    if (abs(tile_pos[0] - empty_pos[0]) == 1 and tile_pos[1] == empty_pos[1]) or \
                            (abs(tile_pos[1] - empty_pos[1]) == 1 and tile_pos[0] == empty_pos[0]):
                        move_tile(puzzle, empty_pos, tile_pos)
                        empty_pos = tile_pos
                        moves += 1

                        if check_win(puzzle):
                            print("Congratulations! You've solved the puzzle in", moves, "moves!")
                            return


# ۲. پازل تصویری (کد پیاده‌سازی نشده)
def image_puzzle():
    print("Image Puzzle not implemented yet!")


# ۳. پازل معمایی (کد پیاده‌سازی نشده)
def logic_puzzle():
    print("Logic Puzzle not implemented yet!")


# شروع برنامه
if __name__ == "__main__":
    main_menu()
