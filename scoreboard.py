import pygame.font


class Scoreboard:
    """Класс для вывода игровой информации"""
    def __init__(self, ai_settings, screen, stats):
        """Инициализация атрибутов подсчёта очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # настройки шрифта для вывода счёта игры
        self.text_color = (30, 30, 30)
        # создание экземпляра объекта шрифта
        self.font = pygame.font.SysFont(None, 48)

        # подготовка исходного изображения счёта
        self.prep_score()

    def prep_score(self):
        """Преобразование текста в изображение"""
        # преобразование числового значения счёта в строку
        score_str = str(self.stats.score)
        # генерация изображения
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # задание расположения изображения с текстом счета
        self.scrore_rect = self.score_image.get_rect()
        self.scrore_rect.right = self.screen_rect.right - 20
        self.scrore_rect.top = 20

    def show_score(self):
        """Вывод счёта игры на экран"""
        self.screen.blit(self.score_image, self.scrore_rect)