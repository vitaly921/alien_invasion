import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс создания корабля пришельца"""

    def __init__(self, ai_settings, screen):
        """Инициализация корабля пришельца"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # загрузка изображения, задание его размеров, конвертация и получение прямоугольника
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.scale(self.image, (60, 40))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()


        # задание координат для отображения корабля
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # сохранение координаты Х в вещественной форме

    def check_edges(self):
        """Возвращает флаг True при достижении флотом правого/левого края экрана"""
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Обновление положения флота пришельцев при перемещении"""
        # координата по Х меняется в зависимости от флага направления и скорости
        self.x = float(self.rect.x)
        self.y = self.rect.y
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.y = self.rect.y

    def blitme(self):
        """Отрисовка пришельца"""
        self.screen.blit(self.image, self.rect)


class BoostedAlien(Alien):
    """Класс для создания усиленного пришельца"""
    def __init__(self, ai_settings, screen):
        super().__init__(ai_settings, screen)
        # дополнительные атрибуты
        # число попаданий
        self.hit_count = 0
        # изображение состояний усиленного пришельца
        self.image_boosted = pygame.image.load('images/boosted_alien.png')
        self.image_damaged = pygame.image.load('images/damaged_alien.png')

        self.image_boosted = pygame.transform.scale(self.image_boosted, (60, 40))
        self.image_damaged = pygame.transform.scale(self.image_damaged, (60, 40))

        self.image = self.image_boosted

    def hit(self):
        """Обработка попаданий по усиленному пришельцу"""
        self.hit_count += 1
        if self.hit_count == 1:
            self.image = self.image_damaged
        elif self.hit_count >= 2:
            self.kill()
