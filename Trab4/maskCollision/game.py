import pygame
from player import Player
from enemy import Enemy
from util import EventHandler
import random

class HealthBar:
    
    def __init__(self, player):
        self.player = player
        self.max_lives = 5
        self.assets = pygame.image.load("images/assets/SpaceInvaders_Health.png").convert_alpha()
        self.sprite = self.get_health_sprite(self.player.lives)
        EventHandler().subscribe("PlayerHit", self.handle_player_hit)

    def get_health_sprite(self, life):
        life = max(0, min(life, self.max_lives))

        frame_width = 32
        frame_height = 16

        frame = self.max_lives - life

        sprite = self.assets.subsurface((0, frame * frame_height, frame_width, frame_height))
        return pygame.transform.scale(sprite,(64, 32))

    def handle_player_hit(self, player):
        self.sprite = self.get_health_sprite(player.lives)

    def draw(self, screen):
        screen.blit(self.sprite, (10, 10))

    def update(self, dt):
        pass
class ScoreDisplay:
    
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        EventHandler().subscribe("EnemyDestroyed", self.handle_enemy_hit)

    def handle_enemy_hit(self, enemy):
        self.score += 100
        print(f"Score: {self.score}")

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 50))

    def update(self, dt):
        pass
class Background:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.surface = pygame.Surface((width, height))

        self.star_tile = pygame.image.load(
            "images/assets/SpaceInvaders_Background.png"
        ).convert_alpha()

        self.building_tile = pygame.image.load(
            "images/assets/SpaceInvaders_BackgroundBuildings.png"
        ).convert_alpha()

        self.create_background()

    def create_background(self):
        self.draw_stars()
        self.draw_buildings()

    def draw_stars(self):
        tile_width = self.star_tile.get_width()
        tile_height = self.star_tile.get_height()

        for y in range(0, self.height, tile_height):
            for x in range(0, self.width, tile_width):

                tile = self.star_tile

                # ajuda a esconder a repetição do padrão
                flip_x = random.choice([True, False])
                flip_y = random.choice([True, False])

                tile = pygame.transform.flip(
                    tile,
                    flip_x,
                    flip_y
                )

                self.surface.blit(tile, (x, y))

    def draw_buildings(self):
        scale = 2

        buildings = pygame.transform.scale(
            self.building_tile,
            (
                self.building_tile.get_width() * scale,
                self.building_tile.get_height() * scale
            )
        )

        tile_width = buildings.get_width()
        tile_height = buildings.get_height()

        y = self.height - tile_height

        for x in range(0, self.width, tile_width):
            self.surface.blit(buildings, (x, y))

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def update(self, dt):
        pass
class Game:
    
    def __init__(self):
        EventHandler().subscribe("GameOver", self.game_over)
        self.objects = []
        self.is_game_over = False
        self.win = False

        self.font = pygame.font.Font(None, 64)

        self.player = Player((400,500))
        self.enemies = []
        self.score = ScoreDisplay()
        self.health = HealthBar(self.player)
        self.background = Background(800, 600)

        self.objects.append(self.background)

        
        self.spawn_enemies()
        self.objects.append(self.player)

        self.objects.append(self.health)
        self.objects.append(self.score)

    def spawn_enemies(self):
        window_width = pygame.display.get_surface().get_width()

        first_enemy = Enemy((0, 50))
        enemy_width = first_enemy.get_rect().width

        spacing = 10
        num_enemies = 2 * window_width // 3 // (enemy_width + spacing)

        for i in range(num_enemies):
            for j in range(2):  # 2 rows of enemies
                x = i * (enemy_width + spacing)
                y = 50 + j * (enemy_width + spacing)

                enemy = Enemy((x, y))

                self.enemies.append(enemy)
                self.objects.append(enemy)

    def update_enemy_formation(self):
        window_width = pygame.display.get_surface().get_width()
        hit_border = False

        for enemy in self.enemies:
            rect = enemy.get_rect()

            if rect.left <= 0 or rect.right >= window_width:
                hit_border = True
                break

        if hit_border:
            for enemy in self.enemies:
                enemy.direction.x *= -1
        

    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)

        if self.is_game_over:
            game_over_text = self.font.render("Game Over", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(400, 300))
            screen.blit(game_over_text, text_rect)
        
        if self.win:
            win_text = self.font.render("You Win!", True, (255, 255, 255))
            text_rect = win_text.get_rect(center=(400, 300))
            screen.blit(win_text, text_rect)


    def update(self, dt):
        for obj in self.objects.copy():
            obj.update(dt)

        self.update_enemy_formation()

    def handle_enemy_hit(self):
        self.score.score += 100
    
    def game_over(self, screen):
        self.is_game_over = True
