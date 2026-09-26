import pygame
from abc import ABC, abstractmethod
import random
from util import EventHandler

class Enemy:

    def __init__(self, pos,speed = 100):
        self.pos = pygame.Vector2(pos)
        self.speed = speed
        self.direction = pygame.Vector2(1, 0)

        self.state = NormalState(self)

        self.shoot_timer = 0
        self.shoot_check_interval = 1

        self.sprite = self.state.sprite

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

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


class EnemyState(ABC):

    # Sprite é comum a classe estado
    sprite = pygame.Surface((32, 32))

    def __init__(self, enemy):
        self.E = enemy

    def draw(self, screen):
        screen.blit(self.sprite, self.E.pos)

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


class NormalState(EnemyState):
    def __init__(self, enemy):
        super().__init__(enemy)

        assets = pygame.image.load("images/assets/SpaceInvaders.png").convert_alpha()
        self.sprite = assets.subsurface((0, 0, 16, 16))
        self.sprite = pygame.transform.scale(self.sprite, (50,50))

    def get_rect(self):
        return self.sprite.get_rect(topleft=self.pos)

    def update(self, dt):
        self.E.pos += self.E.direction * self.E.speed * dt
        self.E.shoot_timer += dt

        if self.E.shoot_timer >= self.E.shoot_check_interval:  # 10% chance to shoot each frame
            self.E.shoot_timer -= self.E.shoot_check_interval

            if random.random() < 0.1:
                self.E.shoot()

    def shoot(self):
        print("Enemy shoot")
        size = self.sprite.get_size()
        EventHandler().notify("Shoot", {
            "position": self.E.pos + pygame.Vector2(size[0]//2, size[1]),  # shoot from the center bottom of the enemy
            "owner": self.E
        })
        self.E.shoot_chance = random.random()

    def hit(self):
        self.E.change_state(DestroyedState)
        
class DestroyedState(EnemyState):
    

    def __init__(self, enemy):

        super().__init__(enemy)
        self.timer = 0
        self.duration = 0.5

        assets = pygame.image.load("images/assets/SpaceInvaders.png").convert_alpha()
        self.sprite = assets.subsurface((16, 0, 16, 16))
        self.sprite = pygame.transform.scale(self.sprite, (50,50))

        EventHandler().notify(
            "EnemyDestroyed",
            self.E
        )
        

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            EventHandler().notify("DestroyObj", self.E)

    def draw(self, screen):
        screen.blit(self.sprite, self.E.pos)

    def hit(self):
        pass

    def shoot(self):
        pass
    def destroy(self):
        EventHandler().notify("DestroyObj", self.E)
