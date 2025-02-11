import pygame

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1512, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer with Jumping")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load sprite sheet
sprite_sheet = pygame.image.load("sprite_sheet.png").convert_alpha()

# Walking and jumping frames
walking_frames = [(0, 110, 80, 110), (80, 110, 80, 110)]
idle_frame = (0, 0, 80, 110)
jump_frame = (80, 0, 80, 110)

# Constants
VELOCITY = 15
JUMP_FORCE = 10
GRAVITY = 0.5
GROUND_LEVEL = HEIGHT - 150  # Y-coordinate for the ground

# Timer for walking animation
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 200)

clock = pygame.time.Clock()

class Sprite:
    def __init__(self):
        self.x = 100
        self.y = GROUND_LEVEL
        self.sprite_counter = 0
        self.facing_left = False
        self.is_jumping = False
        self.jump_velocity = 0

    def move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.x += VELOCITY
            self.sprite_counter = (self.sprite_counter + 1) % 2
            self.facing_left = False
        elif keys[pygame.K_LEFT]:
            self.x -= VELOCITY
            self.sprite_counter = (self.sprite_counter + 1) % len(walking_frames)
            self.facing_left = True

    def jump(self, keys):
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = JUMP_FORCE

    def apply_gravity(self):
        if self.is_jumping:
            self.y -= self.jump_velocity
            self.jump_velocity -= GRAVITY
            if self.y >= GROUND_LEVEL:
                self.y = GROUND_LEVEL
                self.is_jumping = False
                self.jump_velocity = 0

    def draw(self):
        if self.is_jumping:
            frame_rect = jump_frame
        elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            frame_rect = walking_frames[self.sprite_counter]
        else:
            frame_rect = idle_frame

        current_sprite = sprite_sheet.subsurface(frame_rect)

        if self.facing_left:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        screen.blit(current_sprite, (self.x, self.y))

main_sprite = Sprite()

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)  # Clear screen

    # Draw ground
    pygame.draw.line(screen, BLACK, (0, GROUND_LEVEL + 110), (WIDTH, GROUND_LEVEL + 110), 5)

    main_sprite.apply_gravity()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TIMER_EVENT:
                keys = pygame.key.get_pressed()
                main_sprite.move(keys)
                main_sprite.jump(keys)  
    main_sprite.draw()

    pygame.display.update()

pygame.quit()
