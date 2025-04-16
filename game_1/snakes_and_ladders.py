import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 820, 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 177, 76)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
SNAKE_COLOR = (255, 0, 0)
LADDER_COLOR = (0, 255, 0)

# Fonts
font = pygame.font.SysFont("arial", 20)
large_font = pygame.font.SysFont("arial", 40)
dice_font = pygame.font.SysFont("arial", 60)

# Board setup
TILE_SIZE = WIDTH // 10

# Snakes and Ladders map
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Player setup
players = [
    {"pos": 1, "color": RED, "name": ""},
    {"pos": 1, "color": YELLOW, "name": ""}
]
current_player_index = 0


# === DRAWING FUNCTIONS ===

def draw_board():
    screen.fill(WHITE)
    number = 1
    for row in range(10):
        for col in range(10):
            x = col * TILE_SIZE if row % 2 == 0 else (9 - col) * TILE_SIZE
            y = 9 * TILE_SIZE - row * TILE_SIZE
            pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE), 1)
            num_text = font.render(str(number), True, BLACK)
            screen.blit(num_text, (x + 5, y + 5))
            number += 1
    draw_snakes_and_ladders()

def draw_snakes_and_ladders():
    for start, end in snakes.items():
        pygame.draw.line(screen, SNAKE_COLOR, get_tile_center(start), get_tile_center(end), 4)
    for start, end in ladders.items():
        pygame.draw.line(screen, LADDER_COLOR, get_tile_center(start), get_tile_center(end), 4)

def get_tile_center(tile):
    row = (tile - 1) // 10
    col = (tile - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = (9 - row) * TILE_SIZE + TILE_SIZE // 2
    return x, y

def draw_players():
    for i, player in enumerate(players):
        x, y = get_tile_center(player["pos"])
        offset = -10 if i == 0 else 10  # so they don’t overlap
        pygame.draw.circle(screen, player["color"], (x + offset, y + offset), TILE_SIZE // 4)

def draw_names():
    for i, player in enumerate(players):
        name_text = font.render(f"{player['name']} (P{i+1})", True, player["color"])
        screen.blit(name_text, (10, HEIGHT - 30 - i * 25))

def animate_movement(start, end, player_index):
    for step in range(start + 1, end + 1):
        players[player_index]["pos"] = step
        draw_board()
        draw_players()
        draw_names()
        pygame.display.update()
        pygame.time.delay(250)

def animate_dice_roll():
    roll = random.randint(1, 6)
    for _ in range(10):
        draw_board()
        draw_players()
        draw_names()
        dice_val = random.randint(1, 6)
        dice_text = dice_font.render(str(dice_val), True, BLACK)
        screen.blit(dice_text, (WIDTH // 2 - 30, HEIGHT // 2 - 30))
        pygame.display.update()
        pygame.time.delay(100)
    return roll

def handle_snakes_ladders(player_index):
    current_tile = players[player_index]["pos"]
    new_tile = snakes.get(current_tile, ladders.get(current_tile, current_tile))
    if new_tile != current_tile:
        animate_movement(current_tile, new_tile, player_index)
        players[player_index]["pos"] = new_tile


# === INPUT FUNCTION ===

def get_player_names():
    for i in range(2):
        entering = True
        name = ''
        while entering:
            screen.fill(WHITE)
            prompt = large_font.render(f"Enter Player {i+1}'s Name: {name}", True, BLACK)
            screen.blit(prompt, (WIDTH // 2 - 250, HEIGHT // 2 - 30))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        players[i]["name"] = name or f"Player {i+1}"
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode


# === MAIN GAME LOOP ===

get_player_names()
running = True
clock = pygame.time.Clock()

while running:
    draw_board()
    draw_players()
    draw_names()
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player = players[current_player_index]
            if player["pos"] >= 100:
                continue  # Skip if player already won

            roll = animate_dice_roll()
            next_pos = player["pos"] + roll
            if next_pos <= 100:
                animate_movement(player["pos"], next_pos, current_player_index)
                player["pos"] = next_pos
                handle_snakes_ladders(current_player_index)

            # Check win condition
            if player["pos"] >= 100:
                draw_board()
                draw_players()
                draw_names()
                win_text = large_font.render(f"{player['name']} Wins!", True, player["color"])
                screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
                pygame.display.update()
                pygame.time.delay(3000)
                running = False
                break

            # Switch to next player
            current_player_index = (current_player_index + 1) % 2

pygame.quit()
