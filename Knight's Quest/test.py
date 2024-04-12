#Тестовый файл
import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

#Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#создание игры и окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_images = []
        for i in range(1, 20):
            image = pygame.image.load(f"sprites/sw{i}.png").convert()
            image.set_colorkey(BLACK)
            image = pygame.transform.scale(image, (50, 100))
            self.sprite_images.append(image)
        self.current_sprite_index = 0
        self.image = self.sprite_images[self.current_sprite_index]
        self.original_images = self.sprite_images.copy()  # Сохраняем оригинальные изображения спрайтов
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.direction = 1  # Направление спрайта (1 - вправо, -1 - влево)
        self.last_update = pygame.time.get_ticks()  # Переменная для отслеживания времени
        self.frame_rate = 150

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprite_images)
            self.image = self.sprite_images[self.current_sprite_index]

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
            self.direction = -1  # Устанавливаем направление влево
            for i in range(len(self.sprite_images)):
                self.sprite_images[i] = pygame.transform.flip(self.original_images[i], True, False)  # Разворачиваем все спрайты зеркально по горизонтали
            self.update_animation()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
            self.direction = 1  # Устанавливаем направление вправо
            self.sprite_images = self.original_images.copy()  # Возвращаем спрайты к оригинальным изображениям
            self.update_animation()

        # Если спрайт движется, переключаем анимацию
        if self.speedx != 0:
            self.update_animation()

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left > WIDTH:
            self.rect.left = WIDTH

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

#Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    #render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()