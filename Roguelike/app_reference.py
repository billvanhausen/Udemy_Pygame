import pygame
import random
import sys

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32

# Map dimensions (in tiles)
MAP_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Colors
COLOR_BG = (15, 15, 25)
COLOR_WALL = (50, 50, 70)
COLOR_FLOOR = (30, 30, 45)
COLOR_PLAYER = (50, 200, 100)
COLOR_ENEMY = (230, 70, 70)

# --- MAP GENERATION ---
def create_map():
    # Fill map with walls (1 = Wall, 0 = Floor)
    game_map = [[1 for _ in range(MAP_HEIGHT)] for _ in range(MAP_WIDTH)]
    rooms = []
    
    # Generate random disconnected rooms for this basic example
    for _ in range(6):
        w = random.randint(4, 8)
        h = random.randint(4, 8)
        x = random.randint(1, MAP_WIDTH - w - 1)
        y = random.randint(1, MAP_HEIGHT - h - 1)
        
        # Carve out the room
        for rx in range(x, x + w):
            for ry in range(y, y + h):
                game_map[rx][ry] = 0
        rooms.append((x, y, w, h))
        
    # Connect rooms with primitive halls
    for i in range(len(rooms) - 1):
        x1, y1, _, _ = rooms[i]
        x2, y2, _, _ = rooms[i+1]
        
        # Horizontal corridor
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map[x][y1] = 0
        # Vertical corridor
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map[x2][y] = 0
            
    return game_map, rooms

# --- ENTITIES ---
class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, dx, dy, game_map):
        # Prevent walking through walls or boundaries
        if 0 <= self.x + dx < MAP_WIDTH and 0 <= self.y + dy < MAP_HEIGHT:
            if game_map[self.x + dx][self.y + dy] == 0:
                self.x += dx
                self.y += dy
                return True
        return False

    def draw(self, surface):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, self.color, rect)

# --- MAIN GAME LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Roguelike Prototype")
    clock = pygame.time.Clock()

    # Initialize map and floor space
    game_map, rooms = create_map()
    
    # Place Player in the center of the first room
    start_x = rooms[0][0] + rooms[0][2] // 2
    start_y = rooms[0][1] + rooms[0][3] // 2
    player = Entity(start_x, start_y, COLOR_PLAYER)
    
    # Spawn a few random enemies on valid floor tiles
    enemies = []
    for room in rooms[1:]:
        ex = room[0] + room[2] // 2
        ey = room[1] + room[3] // 2
        enemies.append(Entity(ex, ey, COLOR_ENEMY))

    running = True
    while running:
        turn_taken = False
        
        # 1. Event Handling
        for event in pygame.get_event_index() if hasattr(pygame, 'get_event_index') else pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key in (pygame.K_LEFT, pygame.K_a): dx = -1
                elif event.key in (pygame.K_RIGHT, pygame.K_d): dx = 1
                elif event.key in (pygame.K_UP, pygame.K_w): dy = -1
                elif event.key in (pygame.K_DOWN, pygame.K_s): dy = 1
                
                # If player moves successfully, they consume a turn
                if (dx != 0 or dy != 0):
                    if player.move(dx, dy, game_map):
                        turn_taken = True

        # 2. Turn-Based AI Processing
        if turn_taken:
            for enemy in enemies:
                # Basic AI: Move 1 step closer to player if randomly decided
                if random.random() < 0.5:
                    edx = 1 if player.x > enemy.x else -1 if player.x < enemy.x else 0
                    edy = 1 if player.y > enemy.y else -1 if player.y < enemy.y else 0
                    
                    # Try moving horizontally, if blocked, try vertically
                    if edx != 0 and not enemy.move(edx, 0, game_map):
                        if edy != 0: enemy.move(0, edy, game_map)
                    elif edy != 0:
                        enemy.move(0, edy, game_map)

        # 3. Rendering
        screen.fill(COLOR_BG)
        
        # Draw Map tiles
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if game_map[x][y] == 1:
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(screen, COLOR_FLOOR, rect)
                    # Simple grid line breakdown
                    pygame.draw.rect(screen, COLOR_BG, rect, 1)

        # Draw Entities
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(30) # Caps execution framework; turn-based logic ignores frame delays

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
