import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Базовый класс для управления пулями корабля игрока и пришельца"""
    def __init__(self, ai_settings, screen, game_ship):
        """Инициализация атрибутов базового класса"""
        super().__init__()
        self.screen = screen
        self.game_ship = game_ship
        self.speed_factor = ai_settings.bullet_speed_factor
        self.color = None
        self.rect = None

    def draw_bullet(self):
        """Функция для отрисовки пули на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class ShipBullet(Bullet):
    """Класс для управления пулями корабля игрока"""
    def __init__(self, ai_settings, screen, ship):
        super().__init__(ai_settings, screen, ship)
        # создание изображения пули в виде прямоугольника
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_for_ship, ai_settings.bullet_height_for_ship)
        # задание расположения пули относительно корабля игрока
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # задание цвета пули
        self.color = ai_settings.bullet_color_for_ship
        # преобразование координаты y в вещественное число
        self.y = float(self.rect.y)

    def update(self):
        """Функция для обновления местоположения пули"""
        # закон изменения координаты y
        self.y -= self.speed_factor
        # присвоение пули обновленной вещественной координаты y
        self.rect.y = self.y


class AlienBullet(Bullet):
    """Класс для управления пулями кораблей пришельцев"""
    def __init__(self, ai_settings, screen, alien):
        super().__init__(ai_settings, screen, alien)
        # задание изображения пули пришельца, его размера и конвертация
        self.image = pygame.image.load('images/alien_bullet.png')
        self.image = pygame.transform.scale(self.image, (22, 45))
        self.image = self.image.convert_alpha()
        # получение прямоугольника изображения
        self.rect = self.image.get_rect()
        # задание расположения пули относительно корабля пришельца
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        # преобразование координаты y в вещественное число
        self.y = float(self.rect.y)

    def update(self):
        """Функция для обновления местоположения пули"""
        # закон изменения координаты y
        self.y += self.speed_factor / 2
        # присвоение пули обновленной вещественной координаты y
        self.rect.y = self.y

    def draw_bullet(self):
        """Функция для отрисовки изображения пули на экране"""
        self.screen.blit(self.image, self.rect)

