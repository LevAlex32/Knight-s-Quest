import pygame
from player import Player
from enemy import Enemy

WIDTH = 800
HEIGHT = 640
FPS = 30

#Цвета
BLACK = (0, 0, 0)

#создание игры и окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player(WIDTH, HEIGHT)
all_sprites.add(player)
player.draw_health_bar(screen)

for _ in range(0):
    enemy = Enemy(WIDTH, HEIGHT)
    all_sprites.add(enemy)

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
