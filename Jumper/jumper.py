# Ensure pygame is installed by running the following command in your terminal:
# pip install pygame

import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumper")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Load images
player_image = pygame.image.load("C:/Users/AjMcb/Downloads/game_char_cage.png")  # Full path to 'game_char_cage.png'
player_image = pygame.transform.scale(player_image, (50, 50))  # Resize to fit the game

# Load obstacle image
obstacle_image = pygame.image.load("C:/Users/AjMcb/Downloads/spike edit.png")  # Full path to 'spike edit.png'
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # Resize to fit the game

# Load background image
background_image = pygame.image.load("C:/Users/AjMcb/Downloads/background.png")  # Full path to 'background.png'
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the screen

# Function to display the start screen
def show_start_screen():
    screen.fill(WHITE)
    font_title = pygame.font.Font(None, 36)  # Smaller font for the title
    font_body = pygame.font.Font(None, 28)  # Smaller font for instructions and start text

    title_text = font_title.render("Welcome to Jumper!", True, BLACK)
    instructions_text = font_body.render("Press SPACE to jump obstacles. Double jump is allowed.", True, BLACK)
    start_text = font_body.render("Press any key to start.", True, BLACK)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 1.5))
    pygame.display.flip()

    # Wait for the player to press any key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Function to reset the game
def reset_game():
    global player_x, player_y, jumping, player_y_velocity, obstacles, score, jump_count
    player_x, player_y = 100, HEIGHT - player_height - 50
    jumping = False
    player_y_velocity = 0
    obstacles = [{"x": WIDTH, "y": HEIGHT - obstacle_height - 50, "velocity": obstacle_velocity}]
    score = 0
    jump_count = 0

# Player settings
player_width, player_height = 50, 50
player_x, player_y = 100, HEIGHT - player_height - 50
jumping = False
jump_height = 15
gravity = 1
player_y_velocity = 0
jump_count = 0  # Track the number of jumps

# Obstacle settings
obstacle_width, obstacle_height = 50, 50
obstacle_velocity = 7
obstacles = [{"x": WIDTH, "y": HEIGHT - obstacle_height - 50, "velocity": obstacle_velocity}]

# Scoring
score = 0

# Initialize high score and attempt counter
high_score = 0
attempts = 0

# Show the start screen
show_start_screen()

# Game loop
running = True
while running:
    # Draw the background image
    screen.blit(background_image, (0, 0))  # Draw at the top-left corner

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and jump_count < 2:  # Allow up to 2 jumps
        if jump_count == 0 or player_y_velocity > 0:  # Allow the second jump only if falling or on the ground
            player_y_velocity = -jump_height
            jump_count += 1  # Increment jump count

    # Player movement
    player_y += player_y_velocity
    player_y_velocity += gravity

    # Reset jump count when the player lands
    if player_y >= HEIGHT - player_height - 50:
        player_y = HEIGHT - player_height - 50
        player_y_velocity = 0
        jump_count = 0  # Reset jump count when player lands

    # Update score
    score += 1

    # Add new obstacles based on score
    if score % 500 == 0:  # Add a new obstacle every 500 points
        obstacles.append({"x": WIDTH, "y": HEIGHT - obstacle_height - 50, "velocity": obstacle_velocity + len(obstacles)})

    # Obstacle movement and collision detection
    player_rect = pygame.Rect(player_x + 10, player_y + 10, player_width - 20, player_height - 20)  # Shrink player's rectangle
    for obstacle in obstacles:
        obstacle["x"] -= obstacle["velocity"]
        if obstacle["x"] < -obstacle_width:
            obstacle["x"] = WIDTH

        # Create a rectangle for the obstacle (used for collision detection)
        obstacle_rect = pygame.Rect(obstacle["x"] + 10, obstacle["y"] + 10, obstacle_width - 20, obstacle_height - 20)

        # Draw the obstacle as an image
        screen.blit(obstacle_image, (obstacle["x"], obstacle["y"]))

        # Check for collision
        if player_rect.colliderect(obstacle_rect):  # If the player collides with the obstacle
            # Increment attempts
            attempts += 1

            # Highlight the collision
            pygame.draw.rect(screen, (255, 0, 0), player_rect, 3)  # Red outline around the player
            pygame.draw.rect(screen, (255, 0, 0), obstacle_rect, 3)  # Red outline around the obstacle
            pygame.display.flip()

            # Pause briefly to show how the player lost
            pygame.time.delay(1000)  # 1-second delay to highlight the collision

            # Check if the player beat their high score
            if score > high_score:
                high_score = score
                high_score_text = "New High Score!" if attempts > 1 else ""
            else:
                high_score_text = ""

            # Display Game Over screen
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!", True, BLACK)
            score_text = font.render(f"Score: {score}", True, BLACK)
            high_score_display = font.render(high_score_text, True, BLACK)
            play_again_text = font.render("Play Again? (y/n)", True, BLACK)

            screen.fill(WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            if high_score_text:
                screen.blit(high_score_display, (WIDTH // 2 - high_score_display.get_width() // 2, HEIGHT // 1.6))  # Adjusted spacing
            screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 1.3))
            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:  # Restart the game
                            reset_game()
                            waiting = False
                        elif event.key == pygame.K_n:  # Quit the game
                            running = False
                            waiting = False

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
