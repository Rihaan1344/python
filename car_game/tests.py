import pygame

pygame.init()

# Screen size
WIDTH = 1512
HEIGHT = 850

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Load images with correct paths
ALL_CARS = pygame.image.load("car_game/cars.png").convert()
road = pygame.image.load("car_game/road.png")
road = pygame.transform.scale(road, (WIDTH, HEIGHT))


# Car class
class UserCar:
    def __init__(self):
        self.image = ALL_CARS.subsurface((20 + 248, 360 + 20, 248, 360))  # Adjust if needed
        self.image = pygame.transform.rotate(self.image, -90)  # Adjust if needed
        self.x = 401 
        self.y = HEIGHT // 2 - 248  # Center vertically
        self.speed = 10

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 160:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 100:
            self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# Main loop
running = True
main_car = UserCar()

while running:
    screen.fill((255, 255, 255))  # Draw background
    keys = pygame.key.get_pressed()  # Get pressed keys
    main_car.move(keys)  # Move car
    main_car.draw()  # Draw car

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update display

pygame.quit()