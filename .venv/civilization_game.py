import pygame
import random

# Initialisation de Pygame
pygame.init()

# Constantes de la carte
TILE_SIZE = 40  # Taille des cases
MAP_WIDTH, MAP_HEIGHT = 20, 15  # Dimensions de la carte (en cases)
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE + 250  # Largeur de la fenêtre
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE  # Hauteur de la fenêtre

# Couleurs des terrains
TERRAIN_COLORS = {
    "Plaines": (144, 238, 144),  # Vert clair
    "Forêt": (34, 139, 34),      # Vert foncé
    "Montagnes": (169, 169, 169), # Gris
    "Eau": (30, 144, 255),       # Bleu
}

# Couleurs des civilisations
CIVILIZATION_COLORS = [
    (255, 0, 0),         # Rouge
    (0, 255, 0),         # Lime
    (0, 0, 128),         # Navy
    (255, 255, 0),       # Jaune
    (0, 255, 255),       # Cyan
    (255, 0, 255),       # Magenta
    (255, 165, 0),       # Orange
    (128, 0, 128),       # Violet
    (255, 105, 180),     # Hot Pink
    (255, 255, 255),     # Blanc
    (128, 128, 0),       # Olive
    (255, 20, 147),      # Deep Pink
    (255, 140, 0),       # Dark Orange
    (0, 128, 128),       # Teal
    (255, 69, 0),        # Red-Orange
]  # Liste des couleurs, étendue à 15

# Police de caractères
FONT = pygame.font.Font(None, 24)

# Fonction pour générer la carte
def generate_map(width, height):
    """Génère une carte aléatoire avec des terrains."""
    terrain_types = ["Plaines", "Forêt", "Montagnes", "Eau"]
    return [[(random.choice(terrain_types), "") for _ in range(width)] for _ in range(height)]

# Classe Civilization
class Civilization:
    def __init__(self, color, start_position):
        self.color = color
        self.name = self.generate_name_from_color()
        self.territory = [start_position]
        self.resources = {"nourriture": 10, "production": 5}
        self.gold = 50
        self.army_strength = 10
        self.tech_points = 0

    def generate_name_from_color(self):
        """Generate a name for the civilization based on its color."""
        color_names = {
            (255, 0, 0): "Red Civilization",
            (0, 255, 0): "Green Civilization",
            (0, 0, 128): "Blue Civilization",
            (255, 255, 0): "Yellow Civilization",
            (0, 255, 255): "Cyan Civilization",
            (255, 0, 255): "Magenta Civilization",
            (255, 165, 0): "Orange Civilization",
            (128, 0, 128): "Purple Civilization",
            (255, 105, 180): "Pink Civilization",
            (255, 255, 255): "White Civilization",
            (128, 128, 0): "Olive Civilization",
            (255, 20, 147): "Deep Pink Civilization",
            (255, 140, 0): "Dark Orange Civilization",
            (0, 128, 128): "Teal Civilization",
            (255, 69, 0): "Red-Orange Civilization",
        }
        return color_names.get(self.color, "Unknown Civilization")

    def expand(self, game_map):
        """La civilisation tente de coloniser un nouveau territoire adjacent."""
        if not self.territory:
            return
        x, y = random.choice(self.territory)  # Choisir un point de départ
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= x + dx < MAP_WIDTH and 0 <= y + dy < MAP_HEIGHT
        ]
        random.shuffle(neighbors)
        for nx, ny in neighbors:
            if game_map[ny][nx][1] == "":  # Si la case est libre
                game_map[ny][nx] = (game_map[ny][nx][0], self.name)
                self.territory.append((nx, ny))
                break

    def develop(self):
        """Améliorer la civilisation."""
        self.resources["nourriture"] += 2
        self.resources["production"] += 1
        self.army_strength += random.randint(1, 3)
        self.tech_points += random.randint(0, 2)

    def is_alive(self):
        """Vérifie si la civilisation est toujours en vie (si elle a un territoire)."""
        return len(self.territory) > 0

# Fonction principale avec logique de tour
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Civilization Game")

    civilizations = [Civilization(CIVILIZATION_COLORS[i], (random.randint(0, MAP_WIDTH-1), random.randint(0, MAP_HEIGHT-1))) for i in range(5)]
    game_map = generate_map(MAP_WIDTH, MAP_HEIGHT)

    clock = pygame.time.Clock()
    running = True
    turn = 0  # Compteur de tours
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Passer au tour suivant lorsque l'utilisateur appuie sur la barre d'espace
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            turn += 1
            print(f"Tour {turn}")  # Ajout d'un message pour indiquer le passage au tour suivant
            for civ in civilizations:
                if civ.is_alive():
                    civ.expand(game_map)
                    civ.develop()

        # Dessiner la carte et les civilisations
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                terrain_type, civ_name = game_map[y][x]  # Récupérer le terrain et la civilisation
                pygame.draw.rect(
                    screen, 
                    TERRAIN_COLORS.get(terrain_type, (255, 255, 255)), 
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )  # Dessiner le terrain sur la carte

                if civ_name:  # Si une civilisation occupe la case
                    color = next(civ.color for civ in civilizations if civ.name == civ_name)
                    pygame.draw.rect(
                    screen, 
                    color, 
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )  # Dessiner la civilisation sur la carte

        # Afficher les informations sur les civilisations sur le côté
        for i, civ in enumerate(civilizations):
            pygame.draw.rect(screen, civ.color, (MAP_WIDTH * TILE_SIZE + 10, 10 + i * 100, 230, 90))
            text = FONT.render(f"{civ.name} - Territoires: {len(civ.territory)} - Or: {civ.gold} - Nourriture: {civ.resources['nourriture']} - Production: {civ.resources['production']} - Technologie: {civ.tech_points} - Armée: {civ.army_strength}", True, (0, 0, 0))
            screen.blit(text, (MAP_WIDTH * TILE_SIZE + 20, 20 + i * 100))

        # Afficher le nombre de tours
        turn_text = FONT.render(f"Tour: {turn}", True, (0, 0, 0))
        screen.blit(turn_text, (MAP_WIDTH * TILE_SIZE + 10, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(10)
        
if __name__ == "__main__":
    main()
