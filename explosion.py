import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """Наследуемый класс для создания экземпляра эффекта взрыва"""
    def __init__(self, ai_settings, screen, pos_x, pos_y):
        """Инициализация атрибутов"""
        super().__init__()
        self.ai_settings = ai_settings
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # загрузка изображения эффекта взрыва
        self.image = pygame.image.load('images/explotion.png')
        # задание размеров, конвертация, получение прямоугольника изображения
        self.image = pygame.transform.scale(self.image,(ai_settings.explosion_width, ai_settings.explosion_height))
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
        # подсчет координаты Х взрыва, соответствущей координате уничтоженного корабля в формате float
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        # передача посчитанной координаты Х прямоугольнику изображения взрыва в формате int
        self.rect.x = self.x

    def blitme(self):
        """Отрисовка пришельца"""
        self.screen.blit(self.image, self.rect)

