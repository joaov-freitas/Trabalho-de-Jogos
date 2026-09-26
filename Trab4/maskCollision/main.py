import pygame
from game import Game
from player import Player
from bullet import PlayerBullet,EnemyBullet
from util import EventHandler
from enemy import Enemy
from collision import Collider

#inicialização
pygame.init()
WIDTH   =  800; HEIGHT =  600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game()

# funções auxiliares

def handle_input(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE and not game.is_game_over:
                player.shoot()

def handle_movement(player):
    direction = pygame.Vector2(0, 0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction.x -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction.x += 1
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        direction.y -= 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        direction.y += 1
    player.set_direction(direction)

def create_bullet(bullet_info):
    owner = bullet_info["owner"]
    pos = bullet_info["position"]

    if isinstance(owner, Player):
        bullet = PlayerBullet(pos)

    elif isinstance(owner, Enemy):
        bullet = EnemyBullet(pos)
    else:
        return

    game.objects.append(bullet)

def remove_obj(obj):
    #variavel global é feio, mas serve como um exemplo
    if obj in game.objects:
        game.objects.remove(obj) 

EventHandler().subscribe("Shoot", create_bullet)
EventHandler().subscribe("DestroyObj", remove_obj)

# loop principal

running = True
while running:
    dt = clock.tick(60) / 1000.0

    handle_input(game.player)

    if not game.is_game_over or not game.win:
        handle_movement(game.player)
        game.update(dt)

        for obj in game.objects.copy():
            obj.update(dt)
        
        enemies = [
            obj for obj in game.objects.copy()
            if isinstance(obj, Enemy)
        ]
        if not enemies:
            game.win = True
        Collider().check_collisions(game.objects, game.player)

    screen.fill((30,30,30))

    game.draw(screen)
    
    pygame.display.flip()
    