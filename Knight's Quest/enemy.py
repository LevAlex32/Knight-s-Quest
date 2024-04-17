import pygame
import random
import os

WIDTH = 800
HEIGHT = 640
GRAVITY = 0.5

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(os.path.join('sprites/enemy/Goomba', 'Goomba1.png')), (100, 100)),
                       pygame.transform.scale(pygame.image.load(os.path.join('sprites/enemy/Goomba', 'Goomba2.png')), (100, 100))]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.speedx = 2
        self.speedy = 0  # Добавляем переменную для скорости по оси Y
        self.damage = 20
        self.animation_timer = 0
        self.animation_delay = 10  # Задержка между сменой кадров анимации

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy  # Применяем скорость по оси Y
        self.speedy += GRAVITY  # Добавляем гравитацию

        # Если дошел до края экрана, развернуть
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speedx *= -1

        # Анимация ходьбы
        self.animation_timer += 1
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def collide_with_player(self, player):
        player.health -= self.damage
