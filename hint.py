import pygame


class Hint:
    """Класс для создания подсказок игры"""
    def __init__(self, text_hint, screen, pos_x, pos_y):
        """Инициализация атрибутов подсказок"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # задание цвета шрифта
        self.text_color = 'white'
        # создание экземпляра объекта шрифта с заданным стилем и размером
        self.font = pygame.font.SysFont('calibri', 34)
        # создание картинки с текстом подсказки
        self.image_font = self.font.render(text_hint,True, self.text_color)
        # задание прозрачности картинки
        self.image_font.set_alpha(150)
        # получение прямоугольника картинки
        self.rect = self.image_font.get_rect()
        # задание расположения картинки
        self.rect.centerx = self.screen_rect.centerx * pos_x
        self.rect.centery = self.screen_rect.centery * pos_y

    def blitme(self):
        """Отрисовка картинки с подсказкой"""
        self.screen.blit(self.image_font, self.rect)
