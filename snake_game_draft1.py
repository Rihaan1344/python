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

VELOCITY = 5

# Snake class
class Snake:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = [50, 50]
        self.direction = 'e'
        self.font = pygame.font.SysFont(None, 48)  # Font defined once

    def update_pos(self, incr_x, incr_y, new_dir):
        if new_dir == self.direction:
            self.x += incr_x
            self.y += incr_y
            self.wrap_snake()

        elif new_dir == 'e' and self.direction == 'w':
            self.direction = new_dir
            self.x += incr_x
            self.y += incr_y
            self.size[0], self.size[1] = self.size[1], self.size[0]
            self.wrap_snake()
        
        elif new_dir == 'e' and self.direction == 's':
            pass

        elif new_dir == 'e' and self.direction == 'n':
            pass

        elif new_dir == 'n' and self.direction == 's':
            pass

        elif new_dir == 'n' and self.direction == 'w':
            pass

        elif new_dir == 's' and self.direction == 'w':
            pass

        elif new_dir == 'ud' and self.direction == 'ud':
            self.direction = new_dir
            self.x += incr_x
            self.y += incr_y
            self.wrap_snake()
        
        elif new_dir == 'ud' and self.direction == 'ss':
            self.direction = new_dir
            self.x += incr_x
            self.y += incr_y
            self.size[0], self.size[1] = self.size[1], self.size[0]
            self.wrap_snake()
        

    def wrap_snake(self):
        if self.x >= WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH - self.sizex
        if self.y >= HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT - self.sizey

    def draw_snake(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size[0], self.size[1]))

    def collided_with(self, food):
        rect_snake = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        rect_food = pygame.Rect(food.x, food.y, food.size, food.size)
        return rect_snake.colliderect(rect_food)

    def make_snake_fatter(self):
        if self.direction == 'ss':
            self.size[0] += 50
        elif self.direction == 'ud':
            self.size[1] += 50


class Food:
    def __init__(self):
        self.size = 20
        self.generate_new()

    def generate_new(self):
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

    def draw_food(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))


# Main loop
running = True
clock = pygame.time.Clock()
my_snake = Snake()
snakes_food = Food()

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        my_snake.update_pos(VELOCITY, 0, 'e')
    elif keys[pygame.K_LEFT]:
        my_snake.update_pos(-VELOCITY, 0, 'w')
    elif keys[pygame.K_DOWN]:
        my_snake.update_pos(0, VELOCITY, 's')
    elif keys[pygame.K_UP]:
        my_snake.update_pos(0, -VELOCITY, 'n')

    # Collision detection
    if my_snake.collided_with(snakes_food):
        my_snake.make_snake_fatter()
        snakes_food.generate_new()

    # Draw snake and food
    my_snake.draw_snake()
    snakes_food.draw_food()

    # Update display
    pygame.display.update()

pygame.quit()
