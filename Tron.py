import pygame
import sys
from collections import deque

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 5  # Reduce the trail thickness
SPEED = 3
GRID_SPACING = 20  # Spacing between grid lines
TRAIL_LENGTH_LIMIT = 500  # Adjust the trail length limit

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (41, 41, 41)
BLUE = (0, 0, 255)    # Blue trail color
ORANGE = (255, 165, 0)  # Orange trail color

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tron Light Cycles - Memory Management")

# Initialize player positions
player1_x, player1_y = WIDTH // 2, HEIGHT // 4
player1_direction = (0, SPEED)

player2_x, player2_y = WIDTH // 2, 3 * HEIGHT // 4
player2_direction = (0, -SPEED)

# Initialize Deque to track the trails and colors
player1_trail = deque(maxlen=TRAIL_LENGTH_LIMIT)
player2_trail = deque(maxlen=TRAIL_LENGTH_LIMIT)
player1_colors = deque(maxlen=TRAIL_LENGTH_LIMIT)  # Store trail colors for player 1
player2_colors = deque(maxlen=TRAIL_LENGTH_LIMIT)  # Store trail colors for player 2

# Game state
game_active = False

#Font for displaying text
font = pygame.font.Font(None, 28)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_active:
                # Start the game
                game_active = True
                player1_trail = []
                player2_trail = []
                player1_colors = []
                player2_colors = []
                player1_x, player1_y = WIDTH // 2, HEIGHT // 4
                player1_direction = (0, SPEED)
                player2_x, player2_y = WIDTH // 2, 3 * HEIGHT // 4
                player2_direction = (0, -SPEED)

    if game_active:
        # Player 1 controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player1_direction != (SPEED, 0):
            player1_direction = (-SPEED, 0)
        if keys[pygame.K_RIGHT] and player1_direction != (-SPEED, 0):
            player1_direction = (SPEED, 0)
        if keys[pygame.K_UP] and player1_direction != (0, SPEED):
            player1_direction = (0, -SPEED)
        if keys[pygame.K_DOWN] and player1_direction != (0, -SPEED):
            player1_direction = (0, SPEED)

        # Player 2 controls
        if keys[pygame.K_a] and player2_direction != (SPEED, 0):
            player2_direction = (-SPEED, 0)
        if keys[pygame.K_d] and player2_direction != (-SPEED, 0):
            player2_direction = (SPEED, 0)
        if keys[pygame.K_w] and player2_direction != (0, SPEED):
            player2_direction = (0, -SPEED)
        if keys[pygame.K_s] and player2_direction != (0, -SPEED):
            player2_direction = (0, SPEED)

        # Update player positions
        player1_x += player1_direction[0]
        player1_y += player1_direction[1]
        player2_x += player2_direction[0]
        player2_y += player2_direction[1]

        
        if (
            (player1_x, player1_y) in player2_trail or
             player1_x < 0 or player1_x >= WIDTH or player1_y < 0 or player1_y >= HEIGHT
):
            winner_text = font.render("Process 2 wins!", True, WHITE)
            line1_text = font.render("Process 1 encountered a memory issue", True, WHITE)
            line2_text = font.render("by accessing memory occupied by Process 2", True, WHITE)
            screen.blit(winner_text, (WIDTH // 25, HEIGHT // 2 - 20))
            screen.blit(line1_text, (WIDTH // 30, HEIGHT // 2))
            screen.blit(line2_text, (WIDTH // 40, HEIGHT // 2 + 20))
            pygame.display.flip()
            game_active = False

        
        elif (
            (player2_x, player2_y) in player1_trail or
             player2_x < 0 or player2_x >= WIDTH or player2_y < 0 or player2_y >= HEIGHT
):
            winner_text = font.render("Process 1 wins!", True, WHITE)
            line1_text = font.render("Process 2 encountered a memory issue", True, WHITE)
            line2_text = font.render("by accessing memory occupied by Process 1", True, WHITE)
            screen.blit(winner_text, (WIDTH // 25, HEIGHT // 2 - 20))
            screen.blit(line1_text, (WIDTH // 30, HEIGHT // 2))
            screen.blit(line2_text, (WIDTH // 40, HEIGHT // 2 + 20))
            pygame.display.flip()
            game_active = False


        

        else:
            # Add new positions to the trails and colors
            player1_trail.append((player1_x, player1_y))
            player2_trail.append((player2_x, player2_y))
            player1_colors.append(BLUE)   # Add a blue color for player 1's trail
            player2_colors.append(ORANGE)  # Add an orange color for player 2's trail

            # Limit trail length
            player1_trail = player1_trail[-TRAIL_LENGTH_LIMIT:]
            player2_trail = player2_trail[-TRAIL_LENGTH_LIMIT:]
            player1_colors = player1_colors[-TRAIL_LENGTH_LIMIT:]
            player2_colors = player2_colors[-TRAIL_LENGTH_LIMIT:]

            # Draw the background grid
            screen.fill(BLACK)
            for x in range(0, WIDTH, GRID_SPACING):
                pygame.draw.line(screen, GREY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, GRID_SPACING):
                pygame.draw.line(screen, GREY, (0, y), (WIDTH, y))

            # Draw the trails
            for i, segment in enumerate(player1_trail):
                pygame.draw.rect(screen, player1_colors[i], (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            for i, segment in enumerate(player2_trail):
                pygame.draw.rect(screen, player2_colors[i], (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

            pygame.display.flip()

    else:
        # Display game over message
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to restart", True, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

    # Limit the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
