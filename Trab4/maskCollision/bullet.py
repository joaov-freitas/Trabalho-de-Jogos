import pygame
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler


class Bullet (ABC):

    def __init__(self, pos, velocity, radius = 16, life_time = None):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(velocity)
        self.life_time = life_time
        self.elapsed = 0
        self.radius = radius

    def get_rect(self):
        return self.sprite.get_rect(topleft=self.pos)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.sprite)

    @abstractmethod
    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.sprite, self.pos)

    def hit(self):
        pass

    def destroy(self): # pede para deletar
        EventHandler().notify("DestroyObj", self) # avisa o mundo que saiu da tela

class PlayerBullet(Bullet):
    frames = None

    def __init__(self, pos):
        super().__init__(
            pos,
            velocity=(0, -500),
            life_time=5
        )

        if PlayerBullet.frames is None:
            PlayerBullet.load_frames()

        self.sprite = self.frames["straight"]

        self.animation_timer = 0
        self.frame_time = 0.08

        self.frame_index = 0

        # pequeno tempo inicial usando o tiro reto
        self.spawn_timer = 0
        self.spawn_duration = 0.08

        self.impacting = False
        self.impact_timer = 0
        self.impact_duration = 0.15

    @classmethod
    def load_frames(cls):
        assets = pygame.image.load(
            "images/assets/SpaceInvaders.png"
        ).convert_alpha()

        def cut_and_scale(assets, rect, scale=3):
            sprite = assets.subsurface(rect)

            return pygame.transform.scale(
                sprite,
                (
                    sprite.get_width() * scale,
                    sprite.get_height() * scale
                )
            )

        cls.frames = {
            "straight": cut_and_scale(assets, (32, 0, 16, 16),3),

            "left": cut_and_scale(assets, (32, 16, 16, 16),3),

            "right": cut_and_scale(assets,(80, 16, 16, 16),3),

            "impact1": cut_and_scale(assets,(32, 48, 16, 16),3),

            "impact2": cut_and_scale(assets, (32, 64, 16, 16), 3)
        }
    def update_impact(self, dt):
        self.impact_timer += dt

        if self.impact_timer < self.impact_duration / 2:
            self.sprite = self.frames["impact1"]

        elif self.impact_timer < self.impact_duration:
            self.sprite = self.frames["impact2"]

        else:
            self.destroy()
    def update(self, dt):
        
        self.elapsed += dt

        if self.life_time and self.elapsed >= self.life_time:
            self.destroy()
            return

        # Se está mostrando o impacto
        if self.impacting:
            self.update_impact(dt)
            return

        # Movimento normal
        self.pos += self.velocity * dt

        # Primeiro frame reto
        self.spawn_timer += dt

        if self.spawn_timer < self.spawn_duration:
            self.sprite = self.frames["straight"]
            return

        # Depois alterna os raios
        self.animation_timer += dt

        if self.animation_timer >= self.frame_time:
            self.animation_timer -= self.frame_time

            self.frame_index = (self.frame_index + 1) % 2

            if self.frame_index == 0:
                self.sprite = self.frames["left"]
            else:
                self.sprite = self.frames["right"]
    def hit(self):
        self.impacting = True

        self.velocity = pygame.Vector2(0, 0)

        self.impact_timer = 0
        self.sprite = self.frames["impact1"]

class EnemyBullet(Bullet):

    def __init__(self, pos):
        super().__init__(pos,velocity=(0, 300), life_time=5)
        self.sprite = colored_sprite((255, 255, 255), (self.radius, self.radius))

    def update(self, dt):
        self.elapsed += dt
        if self.life_time and self.elapsed >= self.life_time:
            self.destroy()
            return

        self.pos.y += self.velocity.y * dt
