import pygame.font


class Button:
    """Класс для создания кнопки Play"""
    def __init__(self, ai_settings, screen, msg, pos_x, pos_y):
        """Инициализирует атрибуты кнопки"""
        self.msg = msg
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # задание размеров, цветов кнопки и текста
        self.width, self.height = ai_settings.button_width, ai_settings.button_height
        self.button_color = ai_settings.button_color
        self.text_color = ai_settings.button_text_color
        self.font = pygame.font.SysFont(ai_settings.button_text_type, ai_settings.button_text_size)

        # построение прямоугольника кнопки, задание размеров и расположения
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx * pos_x
        self.rect.centery = self.screen_rect.centery * pos_y

        # вывод текста на кнопке
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Функция задания текста на кнопке"""
        # преобразование текста в изображение
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # получение прямоугольника с изображением текста
        self.msg_image_rect = self.msg_image.get_rect()
        # задание расположения изображения текста относительно кнопки
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Функция отображения кнопки на экране"""
        # отрисовка прямоугольной области кнопки с заданным цветом фона
        self.screen.fill(self.button_color, self.rect)
        # отрисовка изображения текста кнопки
        self.screen.blit(self.msg_image, self.msg_image_rect)
