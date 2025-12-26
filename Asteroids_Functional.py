import pygame, sys

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Meteor Shooter')
clock = pygame.time.Clock()
mouse_button = ();

# Import Images
ship_surface = pygame.image.load('./graphics/ship.png').convert_alpha( )
ship_rect = ship_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surface = pygame.image.load('./graphics/laser.png').convert_alpha( )
laser_rect = laser_surface.get_rect(midbottom = ship_rect.midtop)

background_surface = pygame.image.load('./graphics/background.png').convert( )

# Import Text
game_font = pygame.font.Font('./graphics/subatomic.ttf', 50)
text_surface = game_font.render('Score:', True, 'White')
text_rect = text_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

while True:

    # Input/Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input/Mouse
    pygame.mouse.set_visible(False)
    ship_rect.center = pygame.mouse.get_pos()
    laser_rect.centery -= 3

    # Frame Rate Limiter
    clock.tick(60)

    display_surface.blit(background_surface,(0,0))
    display_surface.blit(laser_surface,laser_rect)
    display_surface.blit(ship_surface,ship_rect)
    display_surface.blit(text_surface,text_rect)

    # Render Frame    
    pygame.display.update()