import pygame
from random import choice

pygame.init()

# Screen size
WIDTH = 1512
HEIGHT = 850

# NPC car frames
NPC_CAR_FRAMES = [(288,  20, 288, 401)  #car 2
                , (576, 20, 288, 401), #car 3
                (20, 401, 288, 401), #car 4
                (288, 401, 288, 401), #car 5
                (576, 401, 288, 401) #car 6
                ]

# Initialize variables
npc_cars = []
score = 0

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Load images with correct paths
ALL_CARS = pygame.image.load("car_game/cars.png").convert_alpha()
road = pygame.image.load("car_game/road.png")
road = pygame.transform.scale(road, (WIDTH, HEIGHT))

# Define the events

NEW_CAR_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(NEW_CAR_EVENT, 1500) #generate a new car every 1.5 secs

MOVE_CAR_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(MOVE_CAR_EVENT, 100) #move every car every 0.1 sec

SCORE_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(SCORE_EVENT, 1000) #upd score every 1 sec

# Car class
class UserCar:
    def __init__(self):
        self.image = ALL_CARS.subsurface((20, 20, 288,  401))  
        self.image = pygame.transform.scale(self.image, (260, 340))
        self.image = pygame.transform.rotate(self.image, -90)  
        self.x = 50
        self.y = HEIGHT // 3   # Center vertically
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0: #check if the up key is pressed and the car is not at the top of the screen
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - 300: #check if the down key is pressed and is not at the bottom of the screen
            self.y += self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class npcCar:
    def __init__(self):
        self.x = WIDTH - 310
        self.y = choice([300, HEIGHT // 3, HEIGHT - 300]) #randomly decide a lane for the car
        self.speed = 5
        img = choice(NPC_CAR_FRAMES)
        try: self.image = ALL_CARS.subsurface(img)
        except: print(img)
        self.image = pygame.transform.scale(self.image, (260, 340))
        self.image = pygame.transform.rotate(self.image, 90) #rotate it
        if len(npc_cars) > 0:  #if there are already cars on the road
            for car in npc_cars:
                if self.y == car.y: #make sure the lane is not occupied
                    self.y = choice([300, HEIGHT // 3, HEIGHT - 300])
        npc_cars.append(self)  #append to NPC cars
    
    def move(self, main_car):
        self.x -= self.speed #move it towards main car
        if self.x < 0: #if it has crossed the road (out of the screen)
            self.get_new_car() #make a new car
        self.check_collision(main_car) #check for collision

    def get_new_car(self):
        npc_cars.remove(self) #remove the car from the list
        npc_cars.append(npcCar()) #add a new car
    
    def check_collision(self, main_car):
        self_rect = pygame.Rect(self.x, self.y, 260, 340)
        main_car_rect = pygame.Rect(main_car.x, main_car.y, 260, 340)
        if self_rect.colliderect(main_car_rect):
            running = False
            print("Collision detected")

# Main loop
running = True
main_car = UserCar()

while running:
    screen.blit(road, (0, 0))  # Draw background

    keys = pygame.key.get_pressed()  # Get pressed keys
    main_car.move(keys)  # Move car
    main_car.draw()  # Draw car

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == NEW_CAR_EVENT:
            npc_cars.append(npcCar())
        if event.type == MOVE_CAR_EVENT:
            for car in npc_cars:
                car.move(main_car)
        if event.type == SCORE_EVENT:
            score += 1


    pygame.display.flip()  # Update display

pygame.quit()
