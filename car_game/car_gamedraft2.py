import pygame
from random import choice

pygame.init()

# Screen size
WIDTH = 1512
HEIGHT = 850

# NPC car frames (cropped from sprite sheet)
NPC_CAR_FRAMES = [
    (268, 20, 248, 360),
    (268 + 248, 20, 248, 360),
    (20, 360 + 20, 248, 360),
    (20 + 248, 360 + 20, 248, 360),
    (268 + 248, 360 + 20, 248, 360)
]

# Initialize variables
npc_cars = []
occupied_lanes = []  # Track which lanes are occupied
score = 0
LANES = [300, HEIGHT // 2, HEIGHT - 300]  # Keep original lane list
MAX_CARS = 5  # Limit number of NPC cars

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Load images
ALL_CARS = pygame.image.load("car_game/cars.png").convert_alpha()
road = pygame.image.load("car_game/road.png")
road = pygame.transform.scale(road, (WIDTH, HEIGHT))

# Define game events
NEW_CAR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_CAR_EVENT, 1500)  # Generate a new car every 1.5 secs

SCORE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCORE_EVENT, 1000)  # Update score every 1 sec


class UserCar:
    def __init__(self):
        self.image = ALL_CARS.subsurface((20, 20, 288, 401))
        self.image = pygame.transform.scale(self.image, (260, 340))
        self.image = pygame.transform.rotate(self.image, -90)
        self.x = 50
        self.y = HEIGHT // 3  # Start in the middle lane
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 300:
            self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class NpcCar:
    def __init__(self):
        global occupied_lanes

        self.image = ALL_CARS.subsurface(choice(NPC_CAR_FRAMES))
        self.image = pygame.transform.rotate(self.image, 90)
        self.x = WIDTH - 310

        # Select a lane that is NOT occupied
        available_lanes = [lane for lane in LANES if lane not in occupied_lanes]

        if available_lanes:
            self.y = choice(available_lanes)
            occupied_lanes.append(self.y)  # Mark lane as occupied
        else:
            self.y = choice(LANES)  # Fallback if all lanes are occupied

        self.speed = 5
        npc_cars.append(self)

        # 🛠 Debugging (Check where the car spawns)
        print(f"✅ NPC Car Spawned in Lane: {self.y}")
        print(LANES)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, mainCar):
        self.x -= self.speed
        if self.x < -300:
            npc_cars.remove(self)
            if self.y in occupied_lanes:
                occupied_lanes.remove(self.y)  # Free up the lane

        self.check_collision(mainCar)
        self.draw()

    def check_collision(self, mainCar):
        global running
        self_rect = pygame.Rect(self.x, self.y, 180, 250)
        main_car_rect = pygame.Rect(mainCar.x, mainCar.y, 180, 250)

        if self_rect.colliderect(main_car_rect):
            print("💥 Collision!")
            running = False


running = True
main_car = UserCar()

while running:
    screen.blit(road, (0, 0))  # Draw background

    keys = pygame.key.get_pressed()
    main_car.move(keys)
    main_car.draw()

    for car in npc_cars:
        car.move(main_car)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == SCORE_EVENT:
            score += 1
            print(f"🏆 Score: {score}")

        if event.type == NEW_CAR_EVENT:
            if len(npc_cars) < MAX_CARS:
                npc_cars.append(NpcCar())

    pygame.display.flip()

pygame.quit()
