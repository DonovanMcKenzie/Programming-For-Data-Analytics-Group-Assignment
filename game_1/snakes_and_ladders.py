import pygame
import random
import statistics
from collections import defaultdict

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
ORANGE = (255, 165, 0)

TILE_SIZE = WIDTH // 10
font = pygame.font.SysFont("arial", 24)

# Define snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Stats Tracker
class StatsTracker:
    def __init__(self):
        self.scores = defaultdict(list)

    def add_score(self, player_name, score):
        self.scores[player_name].append(score)

    def display_stats(self):
        print("\n----- Game Statistics -----")
        for player, scores in self.scores.items():
            print(f"\nStats for {player}:")
            print(f"Scores: {scores}")
            print(f"Games played: {len(scores)}")
            print(f"Mean: {statistics.mean(scores):.2f}")
            print(f"Median: {statistics.median(scores):.2f}")
            try:
                print(f"Mode: {statistics.mode(scores)}")
            except statistics.StatisticsError:
                print("Mode: No unique mode")
            print(f"Range: {max(scores) - min(scores)}")
            print(f"Min: {min(scores)}, Max: {max(scores)}")

# Player class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 1

# Helper functions
def get_tile_center(tile):
    row = (tile - 1) // 10
    col = (tile - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * TILE_SIZE + TILE_SIZE // 2
    y = (9 - row) * TILE_SIZE + TILE_SIZE // 2
    return x, y

def draw_board():
    screen.fill(WHITE)
    number = 1
    for row in range(10):
        for col in range(10):
            x = col * TILE_SIZE if row % 2 == 0 else (9 - col) * TILE_SIZE
            y = 9 * TILE_SIZE - row * TILE_SIZE
            pygame.draw.rect(screen, BLUE, (x, y,)
