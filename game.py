import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
HERO_SIZE = 150
ENEMY_SIZE = 105
BULLET_SIZE = 15

# Set up some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load the images
hero_img = pygame.image.load('hero.png')
hero_img = pygame.transform.scale(hero_img, (HERO_SIZE, HERO_SIZE))
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

# Load the audio files
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # Play the background music in a loop
death_sound = pygame.mixer.Sound('death_sound.mp3')
lose = pygame.mixer.Sound('lose_sound.mp3')
# Set up the font
font = pygame.font.Font(None, 36)

# Set up the rules
rules = ["Use the arrow keys to move the hero",
         "Press the space bar to shoot",
         "Avoid the enemies!"]

# Set up the start button
start_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 25, 200, 50)

# Set up the retry button
retry_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 25, 200, 50)

# Set up the game state
start_game = False
game_over = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                start_game = True
                game_over = False
            if retry_button.collidepoint(event.pos) and game_over:
                game_over = False
                start_game = True

    if not start_game:
        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the rules
        for i, rule in enumerate(rules):
            text = font.render(rule, True, WHITE)
            screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 50 + i * 30))

        # Draw the start button
        pygame.draw.rect(screen, WHITE, start_button)
        text = font.render("Start", True, BLACK)
        screen.blit(text, (start_button.x + 75, start_button.y + 15))

        # Update the display
        pygame.display.flip()
    else:
        # Set up the hero and enemy positions
        hero_x, hero_y = WIDTH / 2, HEIGHT - HERO_SIZE - 20
        enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0

        # Set up the bullet list
        bullets = []

        # Set up the score and high score
        score = 0
        high_score = 0

        # Game loop
        clock = pygame.time.Clock()
        enemy_alive = True

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append([hero_x + HERO_SIZE / 2, hero_y])

            # Get a list of all keys currently being pressed down
            keys = pygame.key.get_pressed()

            # Move the hero
            
            if keys[pygame.K_LEFT]:
                hero_x -= 5
            if keys[pygame.K_RIGHT]:
                hero_x += 5

            # Keep the hero within the screen
            hero_x = max(0, min(hero_x, WIDTH - HERO_SIZE))
            hero_y = max(0, min(hero_y, HEIGHT - HERO_SIZE))

            # Move the bullets
            for i, bullet in enumerate(bullets):
                bullet[1] -= 5
                if bullet[1] < 0:
                    bullets.pop(i)

            # Move the enemy
            if enemy_alive:
                enemy_y += 2
                if enemy_y > HEIGHT:
                    enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0

            # Check for collisions between bullets and enemy
            for i, bullet in enumerate(bullets):
                if (enemy_x < bullet[0] < enemy_x + ENEMY_SIZE and
                        enemy_y < bullet[1] < enemy_y + ENEMY_SIZE):
                    bullets.pop(i)
                    enemy_x, enemy_y = random.randint(0, WIDTH - ENEMY_SIZE), 0
                    death_sound.play()
                    score+=1
                    break
                    
            # Check for collisions between the hero and enemy
            if (enemy_x < hero_x + HERO_SIZE and
                    enemy_x + ENEMY_SIZE > hero_x and
                    enemy_y < hero_y + HERO_SIZE and
                    enemy_y + ENEMY_SIZE > hero_y):
                game_over = True
                lose.play()
                break

            # Draw everything
            screen.fill(BLACK)
            screen.blit(hero_img, (hero_x, hero_y))
            for bullet in bullets:
                pygame.draw.circle(screen, WHITE, [int(bullet[0]), int(bullet[1])], BULLET_SIZE)
            if enemy_alive:
                screen.blit(enemy_img, (enemy_x, enemy_y))

            # Draw the score
            text = font.render("Score: " + str(score), True, WHITE)
            screen.blit(text, (10, 10))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)

        # Game over screen
        
        screen.fill(BLACK)
        text = font.render("Game Over! Your score was " + str(score), True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT/ 2 - text.get_height() / 2))
        pygame.draw.rect(screen, WHITE, retry_button)
        text = font.render("Retry", True, BLACK)
        screen.blit(text, (retry_button.x + 75, retry_button.y + 15))
        pygame.display.flip()

        # Wait for the user to click the retry button
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        game_over = False
                        start_game = True
                        break
            if not game_over:
                break