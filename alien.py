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
        #self.image.set_alpha(50)
        self.rect = self.image.get_rect()

        # задание координат для отображения корабля
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # сохранение координаты Х в вещественной форме
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает флаг True при достижении флотом правого/левого края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Обновление положения флота пришельцев при перемещении"""
        # координата по Х меняется в зависимости от флага направления и скорости
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Отрисовка пришельца"""
        #self.screen.blit(self.image, self.rect)
        pass
