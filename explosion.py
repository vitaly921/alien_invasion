import pygame
from pygame._sprite import Sprite


class Explosion(Sprite):
    """Базовый класс для создания экземпляра эффекта взрыва"""
    def __init__(self, ai_settings, screen, game_ship, for_alien=False):
        """Инициализация атрибутов"""
        super().__init__()
        self.game_ship = game_ship
        self.for_alien = for_alien
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.creation_time = pygame.time.get_ticks()
        # загрузка изображения эффекта взрыва
        self.image = pygame.image.load('images/explosion.png')
        # задание размеров, конвертация, получение прямоугольника изображения
        self.image = pygame.transform.scale(self.image, (ai_settings.explosion_width, ai_settings.explosion_height))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # сохранение координат места взрыва у корабля игрока или пришельца
        if self.for_alien:
            self.pos_x = game_ship.x
            self.pos_y = game_ship.y
        else:
            self.pos_x = game_ship.centerx - 25
            self.pos_y = game_ship.centery - 25

        # задание координат взрыва на основе полученных координат мест взрыва
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y
        # конвертация координат Х и Y в числа с плавающей точкой
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Функция обновления координат взрыва в процессе игры"""
        # подсчет координаты Х взрыва, соответствущей координате уничтоженного корабля в формате float
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        # передача посчитанной координаты Х прямоугольнику изображения взрыва в формате int
        self.rect.x = self.x


    def blitme(self):
        """Отрисовка эффекта взрыва на экране"""
        self.screen.blit(self.image, self.rect)


class SmallExplosion(Explosion):
    """Наследуемый класс для создания мини-эффекта взрыва """
    def __init__(self, ai_settings, screen, game_ship, ship_type, shot_location ,for_alien=False):
        """Инициализация атрибутов"""
        super().__init__(ai_settings, screen, game_ship, for_alien)
        self.ship_type = ship_type
        self.game_ship = game_ship
        #self.left = left
        #self.right = right
        #self.center = center
        self.shot_location = shot_location
        # изменение размеров изображения, конвертация, обновление прямоугольника
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        """Функция обновления координат мини-взрыва в процессе игры"""
        if self.for_alien:
            # закон изменения координат мини-взрыва относительно корабля пришельца
            self.x = self.game_ship.rect.centerx - 12
            self.y = self.game_ship.rect.bottom - 8
        else:
            if self.ship_type == 0 and self.shot_location == 'center':
                # закон изменения координат мини-взрыва относительно корабля игрока
                self.x = self.game_ship.centerx - 11
                self.y = self.game_ship.centery - 58
            elif self.ship_type == 1 and self.shot_location == 'left':
                self.x = self.game_ship.rect.left+12
                self.y = self.game_ship.rect.top+3
            elif self.ship_type == 1 and self.shot_location == 'right':
                self.x = self.game_ship.rect.right-32
                self.y = self.game_ship.rect.top+3
            elif self.ship_type == 2 and self.shot_location == 'center':
                self.x = self.game_ship.centerx - 10
                self.y = self.game_ship.centery - 57
            elif self.ship_type == 2 and self.shot_location == 'left':
                self.x = self.game_ship.rect.left+12
                self.y = self.game_ship.rect.top+8
            elif self.ship_type == 2 and self.shot_location == 'right':
                self.x = self.game_ship.rect.right-30
                self.y = self.game_ship.rect.top+8
        # передача посчитанных координат прямоугольнику изображения взрыва в формате int
        self.rect.x = self.x
        self.rect.y = self.y
