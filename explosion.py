import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Наследуемый класс для создания экземпляра эффекта взрыва"""

    def __init__(self, ai_settings, screen, game_ship, for_alien=False):
        """Инициализация атрибутов"""
        super().__init__()
        self.game_ship = game_ship
        self.for_alien = for_alien
        self.ai_settings = ai_settings
        if self.for_alien:
            self.pos_x = game_ship.x
            self.pos_y = game_ship.y
        else:
            self.pos_x = game_ship.centerx - 25
            self.pos_y = game_ship.centery - 25
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # загрузка изображения эффекта взрыва
        self.image = pygame.image.load('images/explosion.png')
        # задание размеров, конвертация, получение прямоугольника изображения
        self.image = pygame.transform.scale(self.image, (ai_settings.explosion_width, ai_settings.explosion_height))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.creation_time = pygame.time.get_ticks()
        #self.explosion_duration = 350

        # задание координат для прямоугольника изображения
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        # конвертация координаты Х в число с плавающей точкой
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Функция обновления координат взрыва"""
        if self.for_alien:
            # подсчет координаты Х взрыва, соответствущей координате уничтоженного корабля в формате float
            self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
            # передача посчитанной координаты Х прямоугольнику изображения взрыва в формате int
            self.rect.x = self.x
        else:
            self.pos_x = self.game_ship.centerx
            self.pos_y = self.game_ship.centery + 45

    def blitme(self):
        """Отрисовка пришельца"""
        self.screen.blit(self.image, self.rect)


class SmallExplosion(Explosion):
    """"""

    def __init__(self, ai_settings, screen, game_ship, for_alien=False):
        """"""
        super().__init__(ai_settings, screen, game_ship, for_alien)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        if self.for_alien:
            self.pos_x = game_ship.x
            self.pos_y = game_ship.y
        else:
            self.pos_x = game_ship.centerx
            self.pos_y = game_ship.centery + 45

        # задание координат для прямоугольника изображения
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        # конвертация координаты Х в число с плавающей точкой
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        if self.for_alien:
            # подсчет координаты Х взрыва, соответствущей координате уничтоженного корабля в формате float
            self.x = self.game_ship.rect.centerx - 12
            # передача посчитанной координаты Х прямоугольнику изображения взрыва в формате int
            self.y = self.game_ship.rect.bottom - 8
            self.rect.x = self.x
            self.rect.y = self.y

        else:
            self.x = self.game_ship.centerx - 13
            self.y = self.game_ship.centery - 60
            self.rect.x = self.x
            self.rect.y = self.y