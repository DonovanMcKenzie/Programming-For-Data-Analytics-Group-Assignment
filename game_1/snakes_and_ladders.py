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
RED = (200, 0, 0)
GREEN = (34, 177, 76)
YELLOW = (255, 215, 0)

# Board setup
TILE_SIZE = WIDTH // 10
font = pygame.font.SysFont("arial", 20)

# Snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Player setup
players = [{"pos": 1, "color": RED}, {"pos": 1, "color": GREEN}]
current_player = 0

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
    draw_lines()

def get_tile_center(tile):
    row = (tile - 1) // 10
    col = (tile - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = (9 - row) * TILE_SIZE + TILE_SIZE // 2
    return x, y

def draw_player(tile, color, offset):
    x, y = get_tile_center(tile)
    pygame.draw.circle(screen, color, (x + offset, y), TILE_SIZE // 4)

def animate_movement(start, end, player):
    for step in range(start + 1, end + 1):
        player["pos"] = step
        draw_board()
        draw_all_players()
        pygame.display.update()
        pygame.time.delay(300)

def draw_all_players():
    draw_player(players[0]["pos"], players[0]["color"], -10)
    draw_player(players[1]["pos"], players[1]["color"], 10)

def draw_lines():
    # Ladders: green
    for start, end in ladders.items():
        start_pos = get_tile_center(start)
        end_pos = get_tile_center(end)
        pygame.draw.line(screen, GREEN, start_pos, end_pos, 5)

    # Snakes: red
    for start, end in snakes.items():
        start_pos = get_tile_center(start)
        end_pos = get_tile_center(end)
        pygame.draw.line(screen, RED, start_pos, end_pos, 5)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    draw_board()
    draw_all_players()
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player = players[current_player]
                roll = random.randint(1, 6)
                next_pos = player["pos"] + roll

                if next_pos <= 100:
                    animate_movement(player["pos"], next_pos, player)

                    # Check for snake or ladder
                    new_pos = snakes.get(player["pos"], ladders.get(player["pos"], player["pos"]))
                    if new_pos != player["pos"]:
                        pygame.time.delay(300)
                        animate_movement(player["pos"], new_pos, player)

                # Check for win
                if player["pos"] == 100:
                    print(f"Player {current_player + 1} wins!")
                    running = False
                    break

                # Switch turn
                current_player = (current_player + 1) % 2

pygame.quit()
