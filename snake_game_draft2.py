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

class Snake:
    def __init__(self):
        """
        Initialize snake while maintaing:
            -x
            -y
            -square count
            -font(can be global)
        """
        self.headx = WIDTH // 2
        self.heady = HEIGHT // 2
        self.sqare_count = 1
        self.head = Square(self.x, self.y)
        self.squares = [self.head]
        self.font = self.font = pygame.font.SysFont(None, 48)

    def move_snake_for1square(self, incr_x, incr_y):
        """
        moves snake only when square count is 1 (checking done in loop ->)
        """
        self.headx += incr_x
        self.heady += incr_y
        self.head.x = self.headx
        self.head.y = self.heady
        
        

    def move_snake_for_morethan1square(self, incr_x, incr_y):
        """
        moves the snake when there is more than 1 square
        """
        for square in self.squares:
            square.x += incr_x
            square.y += incr_y


    def wrap_snake(self):
        """
        allows snake to wrap around the screen
        """
        if self.x >= WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH - self.sizex
        if self.y >= HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT - self.sizey

    def draw_snake(self):
        """
        draw the snake(so that we dont have to keep typing whatever this is ->
        """
        for square in self.squares:
            square.draw_square()

class Food:
    pass

class Square:
    """
    class for every square
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50

    def draw_square(self):
        """
        draws the square
        """
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size), 2)


running = True
clock = pygame.time.Clock()

my_snake = Snake()

while running:
    clock.tick(60)

    screen.fill(WHITE)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    

pygame.quit()