import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Базовый класс для управления пулями корабля игрока и пришельца"""
    def __init__(self, ai_settings, screen, game_ship):
        """Инициализация атрибутов базового класса"""
        # вызов родительского конструктора для инициализации объекта на основе класса Sprite
        super().__init__()
        # инициализация атрибутов экрана, игрового объекта и значения скорости пули
        self.screen = screen
        self.game_ship = game_ship
        self.ship_bullet_speed_factor = ai_settings.ship_bullet_speed_factor
        self.alien_bullet_speed_factor = ai_settings.alien_bullet_speed_factor

    def draw_bullet(self):
        """Функция для отрисовки пули на экране"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class ShipBullet(Bullet):
    """Класс для управления пулями корабля игрока"""
    def __init__(self, ai_settings, screen, ship, ship_type, shot_location, boosted=False):
        # передача аргументов родительскому классу
        super().__init__(ai_settings, screen, ship)
        # инициализация дополнительных аргументов: цвета пули, флага для усиленной пули, корабля игрока и его номера
        self.color = ai_settings.bullet_color_for_ship
        self.boosted = boosted
        self.ship = ship
        self.ship_type = ship_type

        # создание изображения пули в виде прямоугольника
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_for_ship, ai_settings.bullet_height_for_ship)

        # задание координат пули относительно корабля игрока на основе его типа и переданных флагов
        if self.ship_type == 0 and shot_location == 'center':
            self.rect.centerx = self.ship.rect.centerx
            self.rect.top = self.ship.rect.top
        elif self.ship_type == 1 and shot_location == 'left':
            self.rect.centerx = self.ship.rect.left+22
            self.rect.top = self.ship.rect.top+20
        elif self.ship_type == 1 and shot_location == 'right':
            self.rect.centerx = self.ship.rect.right-22
            self.rect.top = self.ship.rect.top+20
        elif self.ship_type == 2 and shot_location == 'left':
            self.rect.centerx = self.ship.rect.left + 2
            self.rect.top = self.ship.rect.top + 20
        elif self.ship_type == 2 and shot_location == 'right':
            self.rect.centerx = self.ship.rect.right - 2
            self.rect.top = self.ship.rect.top + 20
        elif self.ship_type == 2 and shot_location == 'center':
            self.rect.centerx = self.ship.rect.centerx
            self.rect.top = self. ship.rect.top

        # вызов функции для проверки и возможного изменения цвета пули
        self.check_bullet_color(ai_settings)
        # преобразование координаты y в вещественное число
        self.y = float(self.rect.y)

    def check_bullet_color(self, ai_settings):
        """Функция для изменения цвета пули корабля игрока в зависимости от аргумента-флага"""
        # задание цвета пули в зависимости от переданного аргумента-флага
        if self.boosted:
            self.color = ai_settings.boosted_bullet_color_for_ship

    def update(self):
        """Функция для обновления местоположения пули"""
        # закон изменения координаты y зависит от заданной скорости движения
        self.y -= self.ship_bullet_speed_factor
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
        self.y += self.alien_bullet_speed_factor
        # присвоение пули обновленной вещественной координаты y
        self.rect.y = self.y

    def draw_bullet(self):
        """Функция для отрисовки изображения пули на экране"""
        self.screen.blit(self.image, self.rect)

