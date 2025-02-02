import pygame

# Initialize Pygame
pygame.init()

WIDTH = 1512
HEIGHT = 850

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((255, 255, 255))
pygame.display.set_caption("Platformer")

# Draw a line
start_pos = (25, HEIGHT - 25*7)
end_pos = (WIDTH - 25, HEIGHT-25*7)
color = (0, 0, 0)
width = 5   
pygame.draw.line(screen, color, start_pos, end_pos, width)

pygame.display.update()

#set up sprite sheet

sprite_sheet = pygame.image.load("sprite_sheet.png").convert_alpha()
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 300)
clock  = pygame.time.Clock()
walking_frames = [(0, 110, 80, 110), (80, 110, 80, 110)]

sprite_counter = 0

# Update the display
pygame.display.flip()

running = True

while running:
    screen.fill((255, 255, 255))
    clock.tick(60)
    screen.blit(sprite_sheet, (100, 100), walking_frames[sprite_counter])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == TIMER_EVENT:
            sprite_counter = (sprite_counter + 1) % 2
    
    pygame.draw.line(screen, color, start_pos, end_pos, width)
    pygame.display.update()

pygame.quit()