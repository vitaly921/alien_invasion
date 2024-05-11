import pygame
from pygame.sprite import Sprite


class AirBomb(Sprite):
    """"""

    def __init__(self, ai_settings, screen, ship):
        """"""
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load('images/air_bomb.png')
        # задание размеров, конвертация, получение прямоугольника изображения
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.bottom

        self.y = float(self.rect.y)
        self.speed_factor = 7

    def update(self):
        """"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_air_bomb(self):
        """Отрисовка пули на экране"""
        self.screen.blit(self.image, self.rect)
