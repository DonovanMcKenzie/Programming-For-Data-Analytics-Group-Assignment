import pygame
import random
import time

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

# Board setup
TILE_SIZE = WIDTH // 10
font = pygame.font.SysFont("arial", 20)

# Player setup
player_pos = 1
player_color = RED
player_name = "Player 1"  # Default name

# Snakes and Ladders map
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

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

def get_tile_center(tile):
    row = (tile - 1) // 10
    col = (tile - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = (9 - row) * TILE_SIZE + TILE_SIZE // 2
    return x, y

def draw_player(tile):
    x, y = get_tile_center(tile)
    pygame.draw.circle(screen, player_color, (x, y), TILE_SIZE // 4)

def animate_movement(start, end):
    global player_pos
    for step in range(start + 1, end + 1):
        player_pos = step
        draw_board()
        draw_player(player_pos)
        pygame.display.update()
        pygame.time.delay(300)  # pause for 300ms between moves

def animate_dice_roll():
    # Simulate dice roll animation (shaking dice)
    roll_result = random.randint(1, 6)
    for _ in range(10):  # Shake the dice a few times
        screen.fill(WHITE)
        draw_board()
        dice_text = font.render(str(roll_result), True, BLACK)
        screen.blit(dice_text, (WIDTH // 2 - 10, HEIGHT // 2 - 10))
        pygame.display.update()
        pygame.time.delay(100)
        roll_result = random.randint(1, 6)  # Update dice number
    return roll_result

def draw_player_name():
    name_text = font.render(f"{player_name}", True, BLACK)
    screen.blit(name_text, (WIDTH // 2 - 50, HEIGHT - 30))

def handle_snakes_ladders():
    global player_pos
    new_pos = snakes.get(player_pos, ladders.get(player_pos, player_pos))
    if new_pos != player_pos:
        # Animate the player moving on a snake or ladder
        animate_movement(player_pos, new_pos)
        player_pos = new_pos
        return True
    return False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    draw_board()
    draw_player(player_pos)
    draw_player_name()
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Animate the dice roll and get the result
                roll_result = animate_dice_roll()
                next_pos = player_pos + roll_result
                if next_pos <= 100:
                    animate_movement(player_pos, next_pos)
                    player_pos = next_pos

                    # Handle snakes and ladders after moving
                    if handle_snakes_ladders():
                        pygame.time.delay(300)  # Pause for a moment after snake/ladder

pygame.quit()
