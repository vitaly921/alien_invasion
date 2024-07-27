import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс-родитель для создания обычного корабля пришельца"""

    def __init__(self, ai_settings, screen):
        """Инициализация корабля пришельца"""
        # вызов родительского конструктора для инициализации объекта на основе класса Sprite
        super().__init__()
        # инициализация атрибутов класса
        self.screen = screen
        self.ai_settings = ai_settings

        # загрузка изображения, задание его размеров, конвертация, получение прямоугольников картинки и экрана
        self.image = pygame.image.load(ai_settings.image_alien)
        self.image = pygame.transform.scale(self.image, (ai_settings.alien_width, ai_settings.alien_height))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # задание координат для отображения корабля
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def check_edges(self):
        """Возвращает флаг True при достижении флотом правого/левого края экрана"""
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Обновление положения флота пришельцев при перемещении"""
        # сохранение координат в вещественной форме
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # координата по Х меняется в зависимости от флага направления и скорости
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        # присвоение измененной координаты прямоугольнику изображения
        self.rect.x = self.x

    def blitme(self):
        """Отрисовка пришельца"""
        self.screen.blit(self.image, self.rect)


class BoostedAlien(Alien):
    """Наследуемый класс для создания усиленного пришельца"""
    def __init__(self, ai_settings, screen):
        """Инициализация усиленного корабля пришельца"""
        # передача аргументов родительскому классу
        super().__init__(ai_settings, screen)
        # дополнительные атрибуты
        # задание числа попаданий
        self.hits_count = 0
        # изображение состояний усиленного пришельца
        self.image_boosted = pygame.image.load(ai_settings.image_boosted_alien)
        self.image_damaged = pygame.image.load(ai_settings.image_damaged_alien)
        # задание размеров изображений усиленных пришельцев
        self.image_boosted = pygame.transform.scale(self.image_boosted, (ai_settings.alien_width, ai_settings.alien_height))
        self.image_damaged = pygame.transform.scale(self.image_damaged, (ai_settings.alien_width, ai_settings.alien_height))
        # конвертация изображений усиленных пришельцев
        self.image_boosted = self.image_boosted.convert_alpha()
        self.image_damaged = self.image_damaged.convert_alpha()
        # замена переменной для отрисовки усиленных пришельцев
        self.image = self.image_boosted

    def hit(self, ai_settings):
        """Обработка попаданий по усиленному пришельцу"""
        # увеличение числа попаданий на 1
        self.hits_count += 1
        # если число попаданий = 1
        if self.hits_count == 1:
            # замена переменной на изображение поврежденного пришельца
            self.image = self.image_damaged
        # если число попаданий превысило допустимое
        elif self.hits_count >= ai_settings.allowed_count_hits:
            # удаление пришельца из группы
            self.kill()
