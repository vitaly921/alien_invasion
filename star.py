import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    """Класс для создания звезды"""

    def __init__(self, screen):
        """Инициализация экземпляра звезды"""
        super().__init__()
        self.screen = screen

        # загрузка изображения звезды, установка прозрачности, конвертация и взятие прямогульной отрисовки
        self.image = pygame.image.load('images/star.png')
        self.image.set_alpha(150)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.y = float(self.rect.y)

    def check_edges(self):
        """Возвращает флаг True при достижении звездой правого/левого края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.top >= screen_rect.bottom:
            return True

    def update(self):
        """Задание скорости для перемещения звезд вниз"""
        self.y += 2.3
        self.rect.y = self.y

    def blitme(self):
        """Отрисовка звезды"""
        #self.screen.blit(self.image, self.rect)
        pass
