import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления пулями, выхпущенными кораблём"""
    def __init__(self, ai_settings, screen, game_object, for_alien=False):
        """Создание объекта пули в текущей позиции корабля"""
        super().__init__()
        self.screen = screen
        self.for_alien = for_alien
        # создание прямоугольника пули и определение его положения относительно корабля
        if self.for_alien:
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_for_alien, ai_settings.bullet_height_for_alien)
            self.rect.centerx = game_object.rect.centerx
            self.rect.bottom = game_object.rect.bottom
            self.color = ai_settings.bullet_color_for_alien
        else:
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_for_ship, ai_settings.bullet_height_for_ship)
            self.rect.centerx = game_object.rect.centerx
            self.rect.top = game_object.rect.top
            self.color = ai_settings.bullet_color_for_ship
        # сохранение y-координаты пули в вещественной форме
        self.y = float(self.rect.y)
        # импортирование цвета и скорости пули из файла настроек

        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Обновление положения пули во время её смещения"""
        if self.for_alien:
            self.y += self.speed_factor/2
            self.rect.y = self.y
        else:
            self.y -= self.speed_factor
            self.rect.y = self.y

    def draw_bullet(self):
        """Отрисовка пули на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)
