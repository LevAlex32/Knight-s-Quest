import pygame

WIDTH = 800
HEIGHT = 640
FPS = 30

class Player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_images_walk = []
        self.sprite_images_jump = []
        #Спрайты для ходьбы
        for i in range(1, 20):
            image = pygame.image.load(f"sprites/sw{i}.png").convert()
            image.set_colorkey((0, 0, 0))
            image = pygame.transform.scale(image, (50, 100))
            self.sprite_images_walk.append(image)
        #Спрайты для прыжка
        for i in range(1, 9):
            image = pygame.image.load(f"sprites/sj{i}.png").convert()
            image.set_colorkey((0, 0, 0))
            image = pygame.transform.scale(image, (50, 100))
            self.sprite_images_jump.append(image)
        self.sprite_images = self.sprite_images_walk
        self.current_sprite_index = 0
        self.image = self.sprite_images[self.current_sprite_index]
        self.original_images = self.sprite_images.copy()  # Сохраняем оригинальные изображения спрайтов
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.direction = 1  # Направление спрайта (1 - вправо, -1 - влево)
        self.last_update = pygame.time.get_ticks()  # Переменная для отслеживания времени
        self.frame_rate = 150
        self.on_ground = True
        self.health = 100  # Начальное количество жизней
        self.health_bar_length = 100  # Длина полосы здоровья
        self.health_bar_height = 10  # Высота полосы здоровья
        self.health_ratio = self.health_bar_length / self.health  # Соотношение длины полосы к количеству жизней

    #Функция прыжка
    def jump(self):
        if self.on_ground:
            self.speedy = -10
            self.current_sprite_index = 0  # Сброс индекса анимации при прыжке
            self.sprite_images = self.sprite_images_jump
            self.update_animation()  # Обновление анимации при прыжке
            self.on_ground = False

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
            self.direction = -1
            for i in range(len(self.sprite_images)):
                self.sprite_images[i] = pygame.transform.flip(self.original_images[i], True, False)
            self.update_animation()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
            self.direction = 1
            self.sprite_images = self.original_images.copy()
            self.update_animation()
        if keystate[pygame.K_s]:
            self.jump()

        # Обновляем анимацию вне зависимости от действий пользователя
        self.update_animation()

        # Если спрайт движется, переключаем анимацию
        if self.speedx != 0:
            self.update_animation()

        # Проверяем, находится ли персонаж на земле, и переключаем анимацию прыжка
        if self.on_ground:
            self.sprite_images = self.sprite_images_walk
        else:
            self.sprite_images = self.sprite_images_jump

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Обработка гравитации
        if not self.on_ground:
            self.speedy += 0.5  # Гравитация
            if self.rect.bottom >= HEIGHT - 10:
                self.rect.bottom = HEIGHT - 10
                self.speedy = 0
                self.on_ground = True
                self.sprite_images = self.sprite_images_walk

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left > WIDTH:
            self.rect.left = WIDTH

    def draw_health_bar(self, surface):
        # Отображение полосы здоровья
        health_bar_width = int(self.health * self.health_ratio)
        health_bar_color = (255, 0, 0)  # Цвет полосы здоровья (красный)
        if self.health <= 30:
            health_bar_color = (255, 255, 0)  # Если жизней меньше 30, меняем цвет на желтый
        elif self.health > 70:
            health_bar_color = (0, 255, 0)  # Если жизней больше 70, меняем цвет на зеленый
        health_bar_rect = pygame.Rect(self.rect.left, self.rect.top - 20, health_bar_width, self.health_bar_height)
        pygame.draw.rect(surface, health_bar_color, health_bar_rect)

