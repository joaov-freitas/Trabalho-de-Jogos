import pygame
from abc import ABC, abstractmethod
from util import EventHandler

class Player:

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 300
        self.lives = 5
        self.state = NormalState(self)
        self.sprite = self.state.sprite

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

    def set_direction(self, direction):
        self.direction = direction

    def shoot(self):
        self.state.shoot()
    
    def hit(self):
        self.state.hit()

    def get_rect(self):
        return self.sprite.get_rect(topleft=self.pos)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.state.sprite)

    def destroy(self):
        EventHandler().notify("DestroyObj", self)


class PlayerState(ABC):

    # Sprite é comum a classe estado
    sprite = pygame.Surface((32, 32))

    def __init__(self, player):
        self.P = player

    def draw(self, screen):
        screen.blit(self.sprite, self.P.pos)

    def delete(self):
        pass  # se precisar apagar algo na mudança de estados

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def shoot(self):
        pass

    @abstractmethod
    def hit(self):
        pass


class NormalState(PlayerState):

    # Sempre aqui para o estados, mesmo que descarregue

    def __init__(self, player):
        super().__init__(player)

        assets = pygame.image.load("images/assets/SpaceInvaders.png").convert_alpha()
        self.sprite = assets.subsurface((64, 0, 16, 16))
        self.sprite = pygame.transform.scale(self.sprite, (50,50))

    def update(self, dt):
        self.P.pos += self.P.direction * self.P.speed * dt
        # Limita a posição do jogador para não sair da tela
        self.P.pos.x = max(0, min(self.P.pos.x, 800 - self.sprite.get_width()))
        self.P.pos.y = max(0, min(self.P.pos.y, 600 - self.sprite.get_height()))

    def shoot(self):
        print("Player shoot")
        EventHandler().notify("Shoot", {
            "position": self.P.pos,
            "owner": self.P
        })

    def hit(self):
        self.P.lives -= 1
        print(f"Player hit! Lives left: {self.P.lives}")

        EventHandler().notify("PlayerHit", self.P)

        if self.P.lives <= 0:
            EventHandler().notify("GameOver", self.P)
        else:
            self.P.change_state(InvincibleState)
        
class InvincibleState(PlayerState):
    
    def __init__(self, player):
        super().__init__(player)
        self.invincible_time = 2.0  # Tempo de invencibilidade em segundos
        self.elapsed_time = 0.0

        assets = pygame.image.load("images/assets/SpaceInvaders.png").convert_alpha()
        self.sprite = assets.subsurface((64, 0, 16, 16))
        self.sprite = pygame.transform.scale(self.sprite, (50,50))

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.invincible_time:
            self.P.change_state(NormalState)

    def shoot(self):
        pass

    def hit(self):
        pass