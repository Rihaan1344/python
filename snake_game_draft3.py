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
        self.head = Square(WIDTH // 2, HEIGHT // 2)
        self.squares = [self.head]

    def move_snake(self, incr_x, incr_y):
        if len(self.squares) == 1:
            self.head.x += incr_x
            self.head.y += incr_y
        else:
            if incr_x != 0:
                self.head.x += VELOCITY
                for square in self.squares:
                    if square.y != self.head.y:
                        square.y += VELOCITY
                    elif square.y == self.head.y:
                        square.x += VELOCITY
            elif incr_y != 0:
                self.head.y += VELOCITY
                for square in self.squares:
                    if square.x != self.head.x:
                        square.y += VELOCITY
                    elif square.x == self.head.x:
                        square.y += VELOCITY

                    


class Food:
    def __init__(self):
        pass

class Square:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def draw_square(self):
        """
        draws the square
        """
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size), 2)




running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    screen.fill(WHITE)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    

pygame.quit()