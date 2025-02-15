import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load assets
ALL_CARS = pygame.image.load("car_game/cars.png").convert_alpha()
road = pygame.image.load("car_game/road.png").convert()

# Extract car sprites (assuming each car is 288x381)
NPC_CAR_FRAMES = [
    (0, 20, 288, 381), (288, 20, 288, 381), (576, 20, 288, 381),
    (0, 420, 288, 381), (288, 420, 288, 381), (576, 420, 288, 381),
]

# Player car frame (choosing the red car)
PLAYER_CAR_FRAME = (288, 20, 288, 381)

# Scale car images
player_car = pygame.transform.scale(ALL_CARS.subsurface(PLAYER_CAR_FRAME), (60, 80))
npc_cars_images = [pygame.transform.scale(ALL_CARS.subsurface(frame), (60, 80)) for frame in NPC_CAR_FRAMES]

# FPS settings
clock = pygame.time.Clock()
FPS = 60

# Main car class
class PlayerCar:
    def __init__(self):
        self.x = WIDTH // 2 - 30
        self.y = HEIGHT - 100
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 80:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 100:  # Stay within road
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - 160:
            self.x += self.speed

    def draw(self):
        screen.blit(player_car, (self.x, self.y))

# NPC car class
class NPCar:
    def __init__(self):
        self.x = random.choice([150, 250, 350, 450, 550])
        self.y = random.randint(-300, -100)
        self.speed = random.randint(3, 7)
        self.image = random.choice(npc_cars_images)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-300, -100)
            self.x = random.choice([150, 250, 350, 450, 550])
            self.speed = random.randint(3, 7)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Collision detection
def check_collision(player, npc_cars):
    player_rect = pygame.Rect(player.x, player.y, 60, 80)
    for npc in npc_cars:
        npc_rect = pygame.Rect(npc.x, npc.y, 60, 80)
        if player_rect.colliderect(npc_rect):
            pygame.time.delay(1000)
            pygame.quit()
            exit()

# Game loop
def main():
    running = True
    player = PlayerCar()
    npc_cars = [NPCar() for _ in range(3)]
    score = 0

    while running:
        screen.fill((0, 0, 0))
        screen.blit(road, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update player
        player.move()
        player.draw()

        # Update NPC cars
        for npc in npc_cars:
            npc.move()
            npc.draw()

        # Check for collision
        check_collision(player, npc_cars)

        # Increase difficulty over time
        score += 1
        if score % 500 == 0:
            for npc in npc_cars:
                npc.speed += 1

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
