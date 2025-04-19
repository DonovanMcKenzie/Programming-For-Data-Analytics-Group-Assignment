import pygame
import random
import sys
import statistics

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 820, 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snakes and Ladders")

# Fonts
font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 30)
leaderboard_font = pygame.font.SysFont("arial", 26)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
PURPLE = (128, 0, 128)

# Tile & board setup
TILE_SIZE = WIDTH // 10
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}


# Player class
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 1
        self.scores = []

    def reset(self):
        self.position = 1


# Helper functions
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
        pygame.draw.line(screen, RED, get_tile_center(start), get_tile_center(end), 4)
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


def draw_players(players):
    for player in players:
        x, y = get_tile_center(player.position)
        pygame.draw.circle(screen, player.color, (x, y), TILE_SIZE // 4)


def animate_movement(player, end_tile):
    start = player.position
    step = 1 if end_tile > start else -1
    for tile in range(start + step, end_tile + step, step):
        player.position = tile
        draw_board()
        draw_players(players)
        display_leaderboard(players)
        pygame.display.update()
        pygame.time.delay(300)


def display_text_centered(text):
    pygame.draw.rect(screen, WHITE, (0, HEIGHT // 2 - 30, WIDTH, 60))
    rendered = big_font.render(text, True, BLACK)
    screen.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, HEIGHT // 2 - 20))
    pygame.display.update()
    pygame.time.delay(1000)


def get_text_input(prompt):
    input_text = ""
    typing = True
    while typing:
        draw_board()
        render = big_font.render(f"{prompt}: {input_text}", True, BLACK)
        screen.blit(render, (WIDTH // 2 - render.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isprintable():
                    input_text += event.unicode
    return input_text


def display_leaderboard(players):
    y_offset = 10
    x_offset = WIDTH - 250
    title = leaderboard_font.render("Leaderboard", True, PURPLE)
    screen.blit(title, (x_offset, y_offset))
    y_offset += 35
    for player in players:
        scores = player.scores
        if scores:
            avg = round(sum(scores) / len(scores), 2)
            score_text = f"{player.name}: Avg: {avg} | Games: {len(scores)}"
        else:
            score_text = f"{player.name}: No games yet"
        rendered = leaderboard_font.render(score_text, True, player.color)
        screen.blit(rendered, (x_offset, y_offset))
        y_offset += 35


def show_statistics(player):
    if len(player.scores) >= 2:
        data = player.scores
        stats_text = f"{player.name}'s Stats - Mean: {round(statistics.mean(data), 2)}, " \
                     f"Median: {statistics.median(data)}, Mode: {statistics.mode(data)}, " \
                     f"Range: {max(data) - min(data)}"
        display_text_centered(stats_text)


# Game loop
while True:
    # Get names
    p1_name = get_text_input("Enter Player 1 Name")
    p2_name = get_text_input("Enter Player 2 Name")

    player1 = Player(p1_name, RED)
    player2 = Player(p2_name, GREEN)
    players = [player1, player2]

    current_player_index = 0
    game_over = False
    clock = pygame.time.Clock()

    while not game_over:
        draw_board()
        draw_players(players)
        display_leaderboard(players)
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_player = players[current_player_index]
                    roll = random.randint(1, 6)
                    display_text_centered(f"{current_player.name} rolled a {roll}")
                    next_pos = current_player.position + roll

                    if next_pos <= 100:
                        animate_movement(current_player, next_pos)

                        # Now check snake or ladder
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
                            current_player.scores.append(roll)
                            show_statistics(current_player)
                            game_over = True
                            break

                    current_player_index = (current_player_index + 1) % 2

    # Replay prompt
    replay = get_text_input("Play again? (y/n)").lower()
    if replay != 'y':
        break
