import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen, number_ship = 1):
        """Создание корабля и задание его начальной позиции"""
        super(Ship, self).__init__()
        # задание объекта, на котором выводится корабль
        self.number_ship = number_ship
        self.screen = screen
        # задание настроек для конкретного корабля
        self.ai_settings = ai_settings
        # загрузка изображения корабля
        '''self.images = []
        self.filenames = ["images/ship1.png", "images/ship2.png", "images/ship3.png"]
        for filename in self.filenames:
            self.image = pygame.image.load(filename)
            self.images.append(self.image)

        self.image = self.images[number_ship-1]
        '''
        if self.number_ship == 1:
            self.image_filename = "images/ship1.png"
        elif self.number_ship == 2:
            self.image_filename = "images/ship2.png"
        elif self.number_ship == 3:
            self.image_filename = "images/ship3.png"

        self.image = pygame.image.load(self.image_filename)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.image = self.image.convert_alpha()
        # получение прямоугольника по границам изображения и экрана
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # задание позиции для прямоугольника с изображением
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # сохранение вещественной координаты X центра корабля
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.x = float(self.rect.x)
        self.y = self.rect.y

        # флаги перемещения корабля по оси X и Y
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Обновление позиции корабля при определённых событиях"""
        # условия для перемещения корабля вправо по Х до границы экрана
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # изменение вещественной координаты в положительную сторону
            self.centerx += self.ai_settings.ship_speed_factor
        # условия для перемещения корабля влево по X до границы экрана
        elif self.moving_left and self.rect.left > 0:
            # изменение вещественной координаты в отрицательную сторону
            self.centerx -= self.ai_settings.ship_speed_factor
        # условия для перемещения корабля вверх по Y до границы экрана
        elif self.moving_up and self.rect.top > 0:
            # изменение вещественной координаты в отрицательную сторону
            self.centery -= self.ai_settings.ship_speed_factor
        # условия для перемещения корабля вниз по Y до границы экрана
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            # изменение вещественной координаты в положительную сторону
            self.centery += self.ai_settings.ship_speed_factor

        # обновление координаты в виде целого числа для отображения корабля
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        """Размещение корабля снизу и в центре экрана"""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - self.rect.height/2

    def blitme(self):
        """Отрисовка корабля в текущей позиции"""
        self.screen.blit(self.image, self.rect)
