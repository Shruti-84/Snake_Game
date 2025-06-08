import pygame
import sys
import random
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

background_music_path = resource_path("background.mp3")
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.play(-1)

# --------- Constants and Setup ---------
# Screen dimensions
WIDTH, HEIGHT = 1000, 600

# Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Setup clock and fonts
clock = pygame.time.Clock()
font_small = pygame.font.SysFont('timesnewroman', 24)
font_large = pygame.font.SysFont('timesnewroman', 50)

# Load and play background music (loop forever)
pygame.mixer.music.load("background.mp3")  # Make sure this file exists
pygame.mixer.music.play(-1)

# --------- High Score Handling ---------
def load_high_score():
    """Load high score from file, safely handle empty or invalid data."""
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            content = file.read().strip()
            if content.isdigit():
                return int(content)
    return 0

def save_high_score(score):
    """Save the high score to file."""
    with open("highscore.txt", "w") as file:
        file.write(str(score))

high_score = load_high_score()

# --------- Display Functions ---------
def show_text(text, font, color, x, y):
    """Helper to render and draw text on the screen."""
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def show_start_screen():
    """Display start menu until user presses SPACE."""
    screen.fill(BLACK)
    show_text("Welcome to Snake Game!", font_large, WHITE, WIDTH//2 - 180, HEIGHT//3)
    show_text("Press SPACE to start", font_small, WHITE, WIDTH//2 - 90, HEIGHT//2)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def show_score(score, high_score):
    """Display current score and high score on screen."""
    score_text = f"Score: {score}   High Score: {high_score}"
    show_text(score_text, font_small, WHITE, 10, 10)

def game_over_screen(score):
    """Display game over message and final scores."""
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    pygame.mixer.music.stop()  # Stop music on game over

    screen.fill(BLACK)
    show_text("Game Over!", font_large, RED, WIDTH//2 - 130, HEIGHT//3)
    show_score(score, high_score)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# --------- Main Game Logic ---------
def main():
    # Initial snake and food setup
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction

    food_pos = [random.randrange(1, WIDTH // 10) * 10,
                random.randrange(1, HEIGHT // 10) * 10]
    food_spawn = True

    score = 0
    speed = 15
    paused = False

    show_start_screen()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(max(score, high_score))
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_p:  # Pause toggle
                    paused = not paused

        if paused:
            # Show paused message
            show_text("Paused - Press 'P' to Resume", font_small, WHITE, WIDTH//2 - 140, HEIGHT//2)
            pygame.display.update()
            clock.tick(5)
            continue

        direction = change_to

        # Update snake position
        if direction == 'RIGHT':
            snake_pos[0] += 10
        elif direction == 'LEFT':
            snake_pos[0] -= 10
        elif direction == 'UP':
            snake_pos[1] -= 10
        elif direction == 'DOWN':
            snake_pos[1] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            speed = min(speed + 1, 30)  # Increase speed but limit max
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn new food if needed
        if not food_spawn:
            food_pos = [random.randrange(1, WIDTH // 10) * 10,
                        random.randrange(1, HEIGHT // 10) * 10]
            food_spawn = True

        # Fill background
        screen.fill(BLACK)

        # Draw snake
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Check for collisions with boundaries
        if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
            game_over_screen(score)

        # Check if snake collides with itself
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over_screen(score)

        # Display score
        show_score(score, high_score)

        # Refresh game screen
        pygame.display.update()

        # Control game speed
        clock.tick(speed)


if __name__ == "__main__":
    main()
