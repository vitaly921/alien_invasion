import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления пулями, выхпущенными кораблём"""
    def __init__(self, ai_settings, screen, ship):
        """Создание объекта пули в текущей позиции корабля"""
        super().__init__()
        self.screen = screen
        # создание прямоугольника пули и определение его положения относительно корабля
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # сохранение y-координаты пули в вещественной форме
        self.y = float(self.rect.y)
        # импортирование цвета и скорости пули из файла настроек
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Обновление положения пули во время её смещения"""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Отрисовка пули на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)
