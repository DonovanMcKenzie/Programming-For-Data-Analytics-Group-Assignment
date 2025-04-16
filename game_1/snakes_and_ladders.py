"""
Snakes and Ladders Game
Author: Khamani Brown #2408880
"""
import pygame
import random
import time
import statistics

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 820, 820
TILE_SIZE = WIDTH // 10
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 177, 76)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)

# Fonts
font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 36)

# Snakes and Ladders map
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}


# Helper functions
def draw_board():
    screen.fill(WHITE)
    number = 1
    for row in range(10):
        for col in range(10):
            x = col * TILE_SIZE if row % 2 == 0 else (9 - col) * TILE_SIZE
            y = 9 * TILE_SIZE - row * TILE_SIZE
            pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE), 2)
            num_text = font.render(str(number), True, BLACK)
            screen.blit(num_text, (x + 5, y + 5))
            number += 1

    # Draw snakes
    for start, end in snakes.items():
        pygame.draw.line(screen, RED, get_tile_center(start), get_tile_center(end), 4)

    # Draw ladders
    for start, end in ladders.items():
        pygame.draw.line(screen, GREEN, get_tile_center(start), get_tile_center(end), 4)


def get_tile_center(tile):
    row = (tile - 1) // 10
    col = (tile - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = (9 - row) * TILE_SIZE + TILE_SIZE // 2
    return x, y


def animate_movement(player, end):
    for step in range(player.position + 1, end + 1):
        player.position = step
        draw_board()
        draw_player(player1)
        draw_player(player2)
        display_names()
        pygame.display.update()
        pygame.time.delay(200)


def draw_player(player):
    x, y = get_tile_center(player.position)
    pygame.draw.circle(screen, player.color, (x, y), TILE_SIZE // 4)


def display_names():
    p1 = font.render(f"{player1.name}: {player1.position}", True, RED)
    p2 = font.render(f"{player2.name}: {player2.position}", True, YELLOW)
    screen.blit(p1, (10, 10))
    screen.blit(p2, (10, 40))


def roll_dice():
    return random.randint(1, 6)


def display_text_centered(text):
    surface = big_font.render(text, True, BLACK)
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(surface, rect)
    pygame.display.update()
    pygame.time.delay(1000)


def calculate_stats(scores):
    if not scores:
        return None
    try:
        return {
            "mean": round(statistics.mean(scores), 2),
            "median": statistics.median(scores),
            "mode": statistics.mode(scores) if len(set(scores)) < len(scores) else "No mode",
            "min": min(scores),
            "max": max(scores),
            "range": max(scores) - min(scores),
            "count": len(scores)
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        return {}


# Player class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 1
        self.scores = []

    def reset(self):
        self.position = 1


# Main loop
def game_loop():
    turn = 0
    running = True
    winner = None

    while running:
        draw_board()
        draw_player(player1)
        draw_player(player2)
        display_names()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_player = player1 if turn % 2 == 0 else player2
                    roll = roll_dice()

                    display_text_centered(f"{current_player.name} rolled a {roll}")
                    next_pos = current_player.position + roll

                    if next_pos <= 100:
                        animate_movement(current_player, next_pos)

                # Check for snake or ladder AFTER the move
tile = current_player.position

if tile in snakes:
    end_tile = snakes[tile]
    display_text_centered(f"Oh no! {current_player.name} hit a snake!")
    animate_movement(current_player, end_tile)

elif tile in ladders:
    end_tile = ladders[tile]
    display_text_centered(f"Yay! {current_player.name} climbed a ladder!")
    animate_movement(current_player, end_tile)

                    if current_player.position == 100:
                        display_text_centered(f"{current_player.name} wins!")
                        current_player.scores.append(turn + 1)
                        winner = current_player
                        running = False
                    turn += 1
        pygame.time.Clock().tick(60)
    return True


# Ask for names
name1 = input("Enter Player 1 Name: ")
name2 = input("Enter Player 2 Name: ")

player1 = Player(name1 or "Player 1", RED)
player2 = Player(name2 or "Player 2", YELLOW)

# Play multiple games
all_scores = []
keep_playing = True

while keep_playing:
    player1.reset()
    player2.reset()
    keep_playing = game_loop()

    all_scores.extend(player1.scores + player2.scores)

    print("\nGame Over! Scores:")
    print(f"{player1.name}: {player1.scores}")
    print(f"{player2.name}: {player2.scores}")

    stats = calculate_stats(all_scores)
    if stats:
        print("\nGame Stats:")
        for k, v in stats.items():
            print(f"{k.capitalize()}: {v}")

    choice = input("\nPlay again? (y/n): ").lower()
    if choice != 'y':
        break

pygame.quit()
