import pygame, sys, random

class Laser(pygame.sprite.Sprite):
    can_shoot = True
    shoot_time = None
    sound = None

    def __init__(self,groups,position):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = position)
        self.pos = pygame.math.Vector2(self.rect.midbottom)

    def move(self):
        print(1 * delta_time * 1000)
        if self.rect.y < 0:
            laser_group.remove(self)
        else:
            self.rect.y -= round(1 * delta_time * 1000)

    @staticmethod
    def timer(duration = 500):
        if not Laser.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - Laser.shoot_time > duration:
                Laser.can_shoot = True

    @staticmethod
    def shoot():
            Laser.sound.play()
            Laser.can_shoot = False
            Laser.shoot_time = pygame.time.get_ticks()

    def update(self):
        self.move()

class Ship(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        self.rect = self.image.get_rect(center = (0,0))

    def shoot_laser(self):
        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0] and Laser.can_shoot:
            Laser(laser_group,self.rect.midtop)
            Laser.shoot()
        
        Laser.timer()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.shoot_laser()

class Meteor(pygame.sprite.Sprite):
    def __init__(self,groups,position_x, position_y):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/meteor.png').convert_alpha()
        self.rect = self.image.get_rect(center = (position_x, position_y))

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1024,576
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('OOP Meteor Shooter')
clock = pygame.time.Clock()

background_surface = pygame.image.load('./graphics/background.png').convert()

# Import Sound
background_music = pygame.mixer.Sound('./sounds/music.wav')
Laser.sound = pygame.mixer.Sound('./sounds/laser.ogg')
meteor_sound = pygame.mixer.Sound('./sounds/explosion.wav')

# Sprite Groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# Sprite Creation
ship = Ship(spaceship_group)
# meteor = Meteor(meteor_group)

background_music.set_volume(0.1)
background_music.play(loops=-1)

# Game Loop
while True:
    delta_time = clock.tick(120) / 1000

    # Input/Events Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()      
 
    # Input/Mouse
    pygame.mouse.set_visible(False)
    
    # Update
    spaceship_group.update()
    laser_group.update()
    
    # Draw
    display_surface.blit(background_surface,(0,0))
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    # Laser.timer()

    # Render Frame    
    pygame.display.update()
