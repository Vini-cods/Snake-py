import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
gray = (40, 40, 40)

# Block size of the snake
block_size = 20

# Starting speed
speed = 10

# Font settings
font = pygame.font.SysFont(None, 30)
font_big = pygame.font.SysFont(None, 50)

# Function to display score
def show_score(score):
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, [0, 0])

# Draw grid in the background
def draw_grid():
    for x in range(0, width, block_size):
        pygame.draw.line(screen, gray, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(screen, gray, (0, y), (width, y))

# Function to display start screen
def start_screen():
    waiting = True
    while waiting:
        screen.fill(black)
        title = font_big.render("Welcome to Snake Game!", True, green)
        instructions = font.render("Use arrow keys to move. Avoid walls and yourself.", True, white)
        instructions2 = font.render("Press [SPACE] to start or [Q] to quit.", True, white)

        screen.blit(title, [width / 2 - title.get_width() / 2, height / 3])
        screen.blit(instructions, [width / 2 - instructions.get_width() / 2, height / 2])
        screen.blit(instructions2, [width / 2 - instructions2.get_width() / 2, height / 2 + 40])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main game function
def snake_game():
    global speed
    # Snake starting position
    snake_x = width / 2
    snake_y = height / 2

    # Change in position
    change_x = 0
    change_y = 0

    # Snake body list and length
    snake_body = []
    snake_length = 1

    # Food position
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    # Game loop control
    game_over = False
    game_end = False

    clock = pygame.time.Clock()

    while not game_over:
        while game_end:
            screen.fill(black)
            message = font.render("Game Over! Press C to play again or Q to quit.", True, red)
            screen.blit(message, [width / 6, height / 3])
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_end = False
                    if event.key == pygame.K_c:
                        snake_game()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and change_x == 0:
                    change_x = -block_size
                    change_y = 0
                elif event.key == pygame.K_RIGHT and change_x == 0:
                    change_x = block_size
                    change_y = 0
                elif event.key == pygame.K_UP and change_y == 0:
                    change_y = -block_size
                    change_x = 0
                elif event.key == pygame.K_DOWN and change_y == 0:
                    change_y = block_size
                    change_x = 0

        # Check for wall collision
        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
            game_end = True

        # Update snake position
        snake_x += change_x
        snake_y += change_y

        screen.fill(black)
        draw_grid()

        # Draw food
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        # Update snake body
        head = [snake_x, snake_y]
        snake_body.append(head)

        if len(snake_body) > snake_length:
            del snake_body[0]

        # Check for self-collision
        for segment in snake_body[:-1]:
            if segment == head:
                game_end = True

        # Draw snake
        for segment in snake_body:
            pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])

        show_score(snake_length - 1)
        pygame.display.update()

        # Check if snake eats the food
        if snake_x == food_x and snake_y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1

            # Increase speed every 5 points
            if snake_length % 5 == 0:
                speed += 1

        clock.tick(speed)

    pygame.quit()
    quit()

# Run the start screen, then the game
start_screen()
snake_game()
