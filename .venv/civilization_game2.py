import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
TILE_SIZE = 50
MAP_WIDTH = 20
MAP_HEIGHT = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TERRAIN_COLOR = (0, 255, 0)
CIV_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (0, 255, 255)]

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Civilization Game - Player Controlled")
font = pygame.font.Font(None, 28)

# Variables
turn_count = 0
game_map = [[("grass", None) for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
event_log = []
player_civ = None  # To be set when the player chooses their civilization

# Civilization class
class Civilization:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.territory = []
        self.gold = 50
        self.food = 10
        self.production = 5
        self.relations = {}

    def expand(self, x=None, y=None):
        if not self.territory:
            return

        if x is not None and y is not None:
            # For player-controlled expansion
            if game_map[y][x][1] is None:
                game_map[y][x] = ("grass", self.name)
                self.territory.append((x, y))
                log_event(f"{self.name} expanded to ({x}, {y}).")
            return

        # For AI-controlled expansion
        x, y = random.choice(self.territory)
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= x + dx < MAP_WIDTH and 0 <= y + dy < MAP_HEIGHT
        ]
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if game_map[ny][nx][1] is None:
                game_map[ny][nx] = ("grass", self.name)
                self.territory.append((nx, ny))
                log_event(f"{self.name} expanded to ({nx}, {ny}).")
                break

    def develop(self):
        self.food += random.randint(1, 3)
        self.production += random.randint(1, 3)
        self.gold += random.randint(1, 5)
        log_event(f"{self.name} developed: +Food {self.food}, +Production {self.production}, +Gold {self.gold}")

    def declare_war_if_neighbor(self, civilizations):
        for civ in civilizations:
            if civ == self:
                continue
            for x, y in self.territory:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                        terrain, neighbor_civ_name = game_map[ny][nx]
                        if neighbor_civ_name and neighbor_civ_name != self.name:
                            self.relations[neighbor_civ_name] = "War"
                            civ.relations[self.name] = "War"
                            log_event(f"{self.name} declared war on {neighbor_civ_name} due to proximity.")
                            return

# Logging events
def log_event(event):
    if len(event_log) > 30:
        event_log.pop(0)
    event_log.append(event)

# Initialize civilizations
civilizations = [Civilization(f"Civ_{i+1}", CIV_COLORS[i]) for i in range(5)]
for civ in civilizations:
    start_x, start_y = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
    civ.territory.append((start_x, start_y))
    game_map[start_y][start_x] = ("grass", civ.name)

# Player chooses civilization
def choose_player_civ():
    global player_civ
    player_civ = civilizations[0]  # Default to the first civilization
    log_event(f"You are controlling {player_civ.name}!")

# Draw map
def draw_map():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            terrain, civ_name = game_map[y][x]
            pygame.draw.rect(screen, TERRAIN_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if civ_name:
                civ_color = next(civ.color for civ in civilizations if civ.name == civ_name)
                pygame.draw.rect(screen, civ_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Draw event log
def draw_event_log():
    log_x = MAP_WIDTH * TILE_SIZE + 10
    log_y = 10
    pygame.draw.rect(screen, WHITE, (MAP_WIDTH * TILE_SIZE, 0, SCREEN_WIDTH - MAP_WIDTH * TILE_SIZE, SCREEN_HEIGHT))
    for event in event_log:
        text = font.render(event, True, BLACK)
        screen.blit(text, (log_x, log_y))
        log_y += 20

# Main game loop
def main():
    global turn_count
    clock = pygame.time.Clock()
    running = True
    choose_player_civ()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Player passes the turn
                turn_count += 1
                log_event(f"Turn {turn_count} begins.")
                for civ in civilizations:
                    if civ != player_civ:  # AI-controlled civilizations
                        civ.expand()
                        civ.develop()
                        civ.declare_war_if_neighbor(civilizations)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mx, my = pygame.mouse.get_pos()
                    x, y = mx // TILE_SIZE, my // TILE_SIZE
                    if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                        player_civ.expand(x, y)

        # Draw everything
        screen.fill(WHITE)
        draw_map()
        draw_event_log()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
