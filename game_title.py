import pygame


class GameTitle:
    """Класс для создания главной надписи игры"""
    def __init__(self, screen):
        """Инициализация атрибутов класса"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # загрузка изображения с текстом главной надписи
        self.image = pygame.image.load('images/name_game.png')
        self.image = self.image.convert_alpha()
        # получение прямоугольника изображения
        self.rect = self.image.get_rect()
        # задание расположения главной надписи
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery / 1.8

    def blitme(self):
        """Отрисовка главной надписи"""
        self.screen.blit(self.image, self.rect)
