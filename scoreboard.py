import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """Класс для вывода игровой информации"""
    def __init__(self, ai_settings, screen, stats):
        """Инициализация атрибутов подсчёта очков"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # задание цвета шрифт
        self.text_color = 'white'
        # создание экземпляра объекта шрифта с заданным стилем и размером
        self.font = pygame.font.SysFont('calibre', 36)
        # настройки жирности шрифта
        self.font.set_bold(False)
        # вызов функции для создания изображений с характеристиками игры
        self.prep_images()

    def prep_images(self):
        """Функция подготовки изображений с характеристиками игры"""
        # подготовка исходного изображения счёта, рекорда, текущего уровня, кол-ва оставшихся кораблей
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """Отображает кол-во оставшихся кораблей у игрока"""
        # создание группы для хранения экземпляров кораблей
        self.ships = Group()
        # заолнение группы доступным кол-вом кораблей
        self.number_ship = 3
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen, self.number_ship)
            # установка нового размера для текущего экземпляра
            ship.image = pygame.transform.scale(ship.image, (50, 50))
            # действия для крайнего корабля в списке
            if ship_number == self.stats.ship_left-1:
                # установка меньшей прозрачности экземпляра
                ship.image.set_alpha(200)
            else:
                # установка большей прозрачности экземпляра
                ship.image.set_alpha(125)
            # задание расположения для каждого корабля группы
            ship.rect.x = 10 + ship_number * 60
            ship.rect.y = 0
            # добавление в группу
            self.ships.add(ship)
            self.number_ship -= 1

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
        high_score = int(self.stats.high_score)
        # задание текстового формата рекорда
        high_score_str = 'Record: ' + '{:,}'.format(high_score).replace(',', ' ')
        # генерация изображения с текстом рекорда
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        # задание расположения изображения с текстом рекорда
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_high_score(self):
        """Вывод рекорда игры"""
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def show_score(self):
        """Вывод счёта игры, уровня, кол-ва доступных кораблей на экране"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
