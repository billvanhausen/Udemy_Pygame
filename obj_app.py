import pygame, sys, random

class Laser(pygame.sprite.Sprite):
    can_shoot = True
    shoot_time = None
    sound = None

    def __init__(self,groups,position):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = position)

    def move(self):
        if self.rect.y < 0:
            laser_group.remove(self)
        else:
            self.rect.y -= round(delta_time * 1000)

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
    can_spawn = True
    spawn_time = None
    sound = None

    def __init__(self,groups,position):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/meteor.png').convert_alpha()
        self.rect = self.image.get_rect(center = position)
        self.direction = pygame.math.Vector2(random.uniform(-0.5,0.5), 1)

    def move(self):
        if self.rect.y > WINDOW_HEIGHT:
            meteor_group.remove(self)
        else:
            self.rect.x += round(self.direction.x * 1000 * delta_time)
            self.rect.y += round(self.direction.y * 500 * delta_time)

    @staticmethod
    def timer(duration = 500):
        if not Meteor.can_spawn:
            current_time = pygame.time.get_ticks()
            if current_time - Meteor.spawn_time > duration:
                Meteor.can_spawn = True

    @staticmethod
    def spawn():
        if Meteor.can_spawn:
            Meteor(meteor_group, (random.randint(-100, WINDOW_WIDTH + 100), 10))
            Meteor.can_spawn = False
            Meteor.spawn_time = pygame.time.get_ticks()
            
    def update(self):
        Meteor.timer()
        self.move()

class Score:
    def __init__(self):
        self.font = pygame.font.Font('./graphics/subatomic.ttf', 50)
        self.text = f'Score: {pygame.time.get_ticks() // 1000}'
        self.surface = self.font.render(self.text, True, 'White')
        self.rect = self.image.get_rect(center = position)

'''
game_font = pygame.font.Font('./graphics/subatomic.ttf', 50)
    score_text = f'Score: {pygame.time.get_ticks() // 1000}'
    text_surface = game_font.render(score_text, True, 'White')
    text_rect = text_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80)) 
    display_surface.blit(text_surface,text_rect)
    pygame.draw.rect(display_surface,'white',text_rect.inflate(30,30),width = 5, border_radius=5)
'''


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
    delta_time = clock.tick() / 1000

    # Input/Events Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()      
 
    # Input/Mouse
    pygame.mouse.set_visible(False)
    
    # Update
    Meteor.spawn()
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()
    
    # Draw
    display_surface.blit(background_surface,(0,0))
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    # Render Frame    
    pygame.display.update()
