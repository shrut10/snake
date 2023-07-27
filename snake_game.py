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
        self.points = 1

    def random_position(self):
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        return x, y

    def respawn(self):
        self.position = self.random_position()
        self.points = random.choice([1, 2, 5])  # Varying point values for different food types

    def draw(self, surface):
        pygame.draw.rect(surface, NEON_PINK, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

def show_game_over_screen(score, high_score):
    font = pygame.font.SysFont(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 'Enter' key to try again
                    return True
                elif event.key == pygame.K_ESCAPE:  # 'Escape' key to exit
                    return False

        # Clear the screen with a black background
        screen.fill(BLACK)

        # Render the "Game Over" text
        game_over_text = font.render("Game Over", True, GREEN)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

        # Render the score and high score text
        score_text = font.render(f"Score: {score}", True, NEON_PINK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
        
        high_score_text = font.render(f"High Score: {high_score}", True, NEON_PINK)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 70))

        # Draw the "Try Again" and "Exit Game" instructions
        instructions_text = font.render("Press Enter to Try Again or Esc to Exit", True, NEON_PINK)
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 120))

        # Update the display
        pygame.display.flip()

def main():
    # Create the snake and set the initial direction
    snake = Snake()
    dx, dy = 1, 0

    # Create the food
    food = Food()

    # Game variables
    score = 0
    high_score = 0
    level = 1
    speed = 10
    countdown_duration = 30  # 30 seconds countdown timer

    # Countdown timer font
    timer_font = pygame.font.SysFont(None, 50)

    # Countdown timer variables
    start_time = pygame.time.get_ticks()

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
            if score > high_score:
                high_score = score
            if not show_game_over_screen(score, high_score):
                pygame.quit()
                sys.exit()
            # Reset the game after the 'Game Over' pop-up
            snake.body = [(WIDTH // 2, HEIGHT // 2)]
            dx, dy = 1, 0
            food.respawn()
            score = 0
            level = 1
            speed = 10
            start_time = pygame.time.get_ticks()  # Reset the countdown timer

        # Check if the snake eats the food
        if snake.body[0] == food.position:
            snake.grow()
            score += food.points
            if score > high_score:
                high_score = score
            food.respawn()

            # Increase speed and level based on the player's score
            if score >= 10:
                speed = 15
                level = 2
            if score >= 20:
                speed = 20
                level = 3
            # Add more levels as needed

        # Clear the screen with a black background
        screen.fill(BLACK)

        # Draw the snake and food
        snake.draw(screen)
        food.draw(screen)

        # Render the score, level, and countdown timer on the game screen
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score} | Level: {level}", True, NEON_PINK)
        screen.blit(score_text, (10, 10))

        # Calculate the remaining time in seconds
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - start_time) // 1000
        time_remaining = max(0, countdown_duration - elapsed_seconds)

        timer_text = timer_font.render(f"Time Remaining: {time_remaining} s", True, NEON_PINK)
        screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

        # Check if time is up
        if time_remaining <= 0:
            if score > high_score:
                high_score = score
            if not show_game_over_screen(score, high_score):
                pygame.quit()
                sys.exit()
            # Reset the game after the 'Game Over' pop-up
            snake.body = [(WIDTH // 2, HEIGHT // 2)]
            dx, dy = 1, 0
            food.respawn()
            score = 0
            level = 1
            speed = 10
            start_time = pygame.time.get_ticks()  # Reset the countdown timer

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(speed)  # Adjust this value to change the snake's speed

if __name__ == "__main__":
    main()
