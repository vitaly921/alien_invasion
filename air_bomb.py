import pygame
from pygame.sprite import Sprite


class AirBomb(Sprite):
    """Класс для создания авиабомб для корабля игрока"""
    def __init__(self, ai_settings, screen, ship):
        """Создание объекта авиабомбы"""
        # вызов родительского конструктора для инициализации объекта на основе класса Sprite
        super().__init__()
        # инициализация атрибутов класса
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # загрузка изображения авиабомбы
        self.image = pygame.image.load('images/air_bomb.png')
        # задание размеров, конвертация, получение прямоугольника изображения
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # задание начального местоположения объекта в нижней части корабля игрока
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.bottom
        # преобразование координаты y объекта в вещественное число
        self.y = float(self.rect.y)
        # задание скорости объекта
        self.speed_factor = 7

    def update(self):
        """Обновление позиции объекта"""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_air_bomb(self):
        """Отрисовка пули на экране"""
        self.screen.blit(self.image, self.rect)
