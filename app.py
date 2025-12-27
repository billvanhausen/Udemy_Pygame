import pygame, sys, random

def laser_update(list, speed = 1000):
    
    for laser in list:
        if laser.bottom < 0:
            list.remove(laser)
        else:
            laser.y -= speed * delta_time
        
        display_surface.blit(laser_surface, laser)

def laser_timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pygame.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

def display_score():
    # if not game_status:
    #     return None
    score_text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surface = game_font.render(score_text, True, 'White')
    text_rect = text_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80)) 
    display_surface.blit(text_surface,text_rect)
    pygame.draw.rect(display_surface,'white',text_rect.inflate(30,30),width = 5, border_radius=5)

def meteor_update(list, speed = 100):
    
    for meteor in list:
        rect, direction = meteor

        if rect.bottom > WINDOW_HEIGHT:
            list.remove(meteor)
        else:
            rect.center += direction * speed * delta_time
 
        display_surface.blit(meteor_surface, rect)

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Meteor Shooter')
clock = pygame.time.Clock()

# Import Images
ship_surface = pygame.image.load('./graphics/ship.png').convert_alpha( )
ship_rect = ship_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

meteor_surface = pygame.image.load('./graphics/meteor.png').convert_alpha( )
meteor_list = []

laser_surface = pygame.image.load('./graphics/laser.png').convert_alpha( )
laser_list = []
can_shoot = True
shoot_time = None

background_surface = pygame.image.load('./graphics/background.png').convert( )

# Import Text
game_font = pygame.font.Font('./graphics/subatomic.ttf', 50)

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

game_paused = False

# Game Loop
while True:

    delta_time = clock.tick(120) / 1000

    # Input/Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            # Laser
            laser_list.append(laser_surface.get_rect(midbottom = ship_rect.midtop))

            # Time
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

        if event.type == meteor_timer:
            # Random position
            pos_x = random.randint(0, WINDOW_WIDTH)
            pos_y = 10
            direction = pygame.math.Vector2(random.uniform(-1,1), 1)
            meteor_rect = meteor_surface.get_rect(midbottom = (pos_x,pos_y))
            meteor_list.append((meteor_rect,direction))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('Pause Game')
                game_paused = not game_paused
                print(game_paused)
            
    if not game_paused:
        # Input/Mouse
        pygame.mouse.set_visible(False)
        ship_rect.center = pygame.mouse.get_pos()

        # Update Objects
        display_surface.blit(background_surface,(0,0))

        display_score()
        laser_update(laser_list)
        can_shoot = laser_timer(can_shoot)

        display_surface.blit(ship_surface,ship_rect)
        meteor_update(meteor_list)
    
        # Render Frame    
        pygame.display.update()