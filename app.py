import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont('comicsansms', 48)

# Load and scale shooter image
shooter_img = pygame.image.load('shooter.png')
shooter_width = 60  # Set desired width
shooter_height = 20  # Set desired height
shooter_img = pygame.transform.scale(shooter_img, (shooter_width, shooter_height))

# High score file handling
def save_high_score(new_score):
    high_score = load_high_score()
    if new_score > high_score:
        with open("high_score.txt", "w") as file:
            file.write(str(new_score))

def load_high_score():
    if not os.path.exists("high_score.txt"):
        return 0
    with open("high_score.txt", "r") as file:
        try:
            return int(file.read())
        except ValueError:
            return 0

# Button function
def draw_button(text, x, y, width, height, color, text_color=white):
    button_rect = pygame.draw.rect(screen, color, (x, y, width, height))
    text_img = font.render(text, True, text_color)
    text_rect = text_img.get_rect(center=button_rect.center)
    screen.blit(text_img, text_rect)
    return button_rect

def main_menu():
    menu = True
    while menu:
        screen.fill(white)
        start_button = draw_button("Start", 300, 200, 200, 50, green)
        high_score_button = draw_button("High Score", 300, 270, 200, 50, red)
        instructions_button = draw_button("Instructions", 300, 340, 200, 50, yellow)
        exit_button = draw_button("Exit", 300, 410, 200, 50, black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    if main_game():
                        game_over_screen()
                elif high_score_button.collidepoint(event.pos):
                    display_high_scores()
                elif instructions_button.collidepoint(event.pos):
                    show_instructions()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def display_high_scores():
    running = True
    high_score = load_high_score()
    while running:
        screen.fill(white)
        high_score_text = font.render(f"High Score: {high_score}", True, black)
        screen.blit(high_score_text, (300, 270))
        back_button = draw_button("Back", 300, 340, 200, 50, blue)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False

        pygame.display.update()

def show_instructions():
    running = True
    while running:
        screen.fill(white)
        instructions_text = [
            "Welcome to the Shooting Game!",
            "Objective: Shoot the colored balls for points.",
            "Controls: Left/Right arrow keys to move, Space to shoot.",
            "Points: Red = 10, Yellow = 5, Black = 2",
            "Game Over: Missing 10 balls ends the game.",
            "Press ESC to return to the main menu."
        ]
        y = 100
        for line in instructions_text:
            render = font.render(line, True, black)
            screen.blit(render, (100, y))
            y += 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

def main_game():
    # Main game setup
    shooter_x = screen_width // 2 - shooter_width // 2
    shooter_y = screen_height - shooter_height - 10
    shooter_speed = 10
    bullets = []
    bullet_speed = 10

    initial_ball_speed = 2
    ball_speed = initial_ball_speed
    balls = []
    ball_spawn_rate = 25
    ball_radius = 20

    score = 0
    missed_balls = 0
    max_missed_balls = 10
    game_over = False
    last_score_check = 0

    clock = pygame.time.Clock()
    frame_count = 0

    running = True
    while running:
        screen.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([shooter_x + shooter_width // 2, shooter_y])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            shooter_x = max(0, shooter_x - shooter_speed)
        if keys[pygame.K_RIGHT]:
            shooter_x = min(screen_width - shooter_width, shooter_x + shooter_speed)

        frame_count += 1
        if frame_count >= ball_spawn_rate:
            frame_count = 0
            ball_color = random.choice([(red, 10), (yellow, 5), (black, 2)])
            ball_x = random.randint(0, screen_width)
            balls.append([ball_x, 0, ball_color[0], ball_color[1]])

        for ball in balls[:]:
            ball[1] += ball_speed
            if ball[1] > screen_height:
                balls.remove(ball)
                missed_balls += 1
                if missed_balls >= max_missed_balls:
                    game_over = True
                    save_high_score(score)
                    return True

        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Draw shooter
        screen.blit(shooter_img, (shooter_x, shooter_y))

        for ball in balls:
            pygame.draw.circle(screen, ball[2], (ball[0], ball[1]), ball_radius)

        for bullet in bullets:
            pygame.draw.rect(screen, black, (bullet[0], bullet[1], 2, 10))

        for bullet in bullets[:]:
            for ball in balls[:]:
                if (bullet[0] - ball[0])**2 + (bullet[1] - ball[1])**2 <= (ball_radius + 5)**2:
                    score += ball[3]
                    balls.remove(ball)
                    bullets.remove(bullet)
                    break

        if score // 100 > last_score_check:
            last_score_check = score // 100
            ball_speed += 1

        score_text = font.render('Score: ' + str(score), True, black)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

def game_over_screen():
    running = True
    while running:
        screen.fill(white)
        score_text = font.render('Game Over! Click to restart or go to main menu.', True, black)
        screen.blit(score_text, (screen_width // 2 - 200, screen_height // 2 - 20))
        restart_button = draw_button("Restart", screen_width // 2 - 100, screen_height // 2 + 50, 100, 40, green)
        main_menu_button = draw_button("Main Menu", screen_width // 2 + 20, screen_height // 2 + 50, 140, 40, blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True  # Restart game
                if main_menu_button.collidepoint(event.pos):
                    return False  # Go back to main menu

        pygame.display.update()

# Run the game
main_menu()
pygame.quit()
