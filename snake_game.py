import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
NEON_PINK = (255, 0, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.grow_pending = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)
        self.body.insert(0, new_head)

        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx * CELL_SIZE, dy * CELL_SIZE)

    def check_collision(self):
        return len(self.body) != len(set(self.body))

    def grow(self):
        self.grow_pending = True

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return x, y

    def respawn(self):
        self.position = self.random_position()

    def draw(self, surface):
        pygame.draw.rect(surface, NEON_PINK, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

def main():
    # Create the snake and set the initial direction
    snake = Snake()
    dx, dy = 1, 0

    # Create the food
    food = Food()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key events to change the snake's direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    dx, dy = 1, 0

        # Change the snake's direction based on key events
        snake.change_direction(dx, dy)

        # Move the snake and check for collisions
        snake.move()
        if snake.check_collision():
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Check if the snake eats the food
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()

        # Clear the screen with a black background
        screen.fill(BLACK)

        # Draw the snake and food
        snake.draw(screen)
        food.draw(screen)

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(10)  # Adjust this value to change the snake's speed

if __name__ == "__main__":
    main()
