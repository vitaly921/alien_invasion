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
        self.text_color = 'white'
        # создание экземпляра объекта шрифта
        self.font = pygame.font.SysFont('calibri', 36)
        self.font.set_bold(False)


        # подготовка исходного изображения счёта, рекорда, текущего уровня
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_level(self):
        """Преобразование уровня игры в изображение"""
        level_str = 'Level: ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 1

    def prep_score(self):
        """Преобразование значения счёта в изображение"""
        # преобразование числового значения счёта в строку
        score_str = 'Score: ' + '{:,}'.format(self.stats.score).replace(',', ' ')
        # генерация изображения
        self.score_image = self.font.render(score_str, True, self.text_color)
        # задание расположения изображения с текстом счета
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 0

    def prep_high_score(self):
        """Преобразование рекордного значения счёта в изображение"""
        # сохранение максимального значения счёта
        high_score = self.stats.high_score
        # задание текстового формата рекорда
        high_score_str = 'Record: ' + '{:,}'.format(high_score).replace(',', ' ')
        # генерация изображения с текстом рекорда
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        # задание расположения изображения с текстом рекорда
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def show_score(self):
        """Вывод счёта игры на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)