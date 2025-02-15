import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1500, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

VELOCITY = 50

class Snake:
    def __init__(self):
        self.head = Square(WIDTH // 2, HEIGHT // 2)
        self.squares = [self.head]
        self.direction = [0, 0]
        self.score = 0

    def move_snake(self, incr_x, incr_y):
        # Move the head first
        new_head = Square(self.head.x + incr_x, self.head.y + incr_y)
        
        # Add the new head to the front of the snake
        self.squares.insert(0, new_head)
        
        # If the snake is growing, we don't remove the tail
        if len(self.squares) > 1:
            self.squares.pop()  # Remove the last segment
        
        # Update the head
        self.head = self.squares[0]
        
        # Wrap the snake
        self.wrap_snake()

    def wrap_snake(self):
        # Loop through all squares and wrap around if needed
        for square in self.squares:
            if square.x >= WIDTH:
                square.x = 0  # Wrap around to the left side
            elif square.x < 0:
                square.x = WIDTH - square.size  # Wrap around to the right side
            if square.y >= HEIGHT:
                square.y = 0  # Wrap around to the top
            elif square.y < 0:
                square.y = HEIGHT - square.size  # Wrap around to the bottom

    def make_snake_fatter(self):
        # Add a new square in the opposite direction of the head
        if self.direction == [VELOCITY, 0]:
            new_square = Square(self.head.x - 50, self.head.y)
            self.squares.append(new_square)
        elif self.direction == [-VELOCITY, 0]:
            new_square = Square(self.head.x + 50, self.head.y)
            self.squares.append(new_square)
        elif self.direction == [0, VELOCITY]:
            new_square = Square(self.head.x, self.head.y - 50)
            self.squares.append(new_square)
        elif self.direction == [0, -VELOCITY]:
            new_square = Square(self.head.x, self.head.y + 50)
            self.squares.append(new_square)
        
        self.score += 1

    def collided_with_food(self, food):
        snake_rect = pygame.Rect(self.head.x, self.head.y, 50, 50)
        food_rect = pygame.Rect(food.x, food.y, food.size, food.size)
        return snake_rect.colliderect(food_rect)
    
    def collided_with_self(self):
        if len(self.squares) == 2: return False
        head = pygame.Rect(self.head.x, self.head.y, 50, 50)
        for square in self.squares[2::]:
            new_square_rect = snake_rect = pygame.Rect(square.x, square.y, 50, 50)
            if head.colliderect(new_square_rect): return True
        return False


    def draw_snake(self):
        for square in self.squares:
            square.draw_square()

class Food:
    def __init__(self):
        self.size = 20
        self.generate_new()

    def generate_new(self):
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

    def draw_food(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))

class Square:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = 50

    def draw_square(self):
        """
        Draws the square
        """
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size), 2)


# Main game loop
my_snake = Snake()
snakes_food = Food()

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60 / 4)

    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        my_snake.direction = [VELOCITY, 0]
        my_snake.move_snake(VELOCITY, 0)
    elif keys[pygame.K_LEFT]:
        my_snake.direction = [-VELOCITY, 0]
        my_snake.move_snake(-VELOCITY, 0)
    elif keys[pygame.K_DOWN]:
        my_snake.direction = [0, VELOCITY]
        my_snake.move_snake(0, VELOCITY)
    elif keys[pygame.K_UP]:
        my_snake.direction = [0, -VELOCITY]
        my_snake.move_snake(0, -VELOCITY)

    # Collision detection(for food)
    if my_snake.collided_with_food(snakes_food):
        my_snake.make_snake_fatter()
        snakes_food.generate_new()

    #Collision detection (if the snake collided with itselg)
    if my_snake.collided_with_self():
        print(f"You Lose! Your score was {my_snake.score}")
        running = False

    # Draw snake and food
    my_snake.draw_snake()
    snakes_food.draw_food()

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
