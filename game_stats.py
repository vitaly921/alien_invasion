class GameStats:
    """Сбор статистики игры"""
    def __init__(self, ai_settings):
        """Инициализация статистики"""
        # инициализация настроек и функции сброса статистики
        self.score = None
        self.level = None
        self.ai_settings = ai_settings
        self.reset_stats()

        # флаг (не)активного состояния игры
        self.game_active = False
        # флаг нажатия кнопки "About It"
        self.press_about_it_button = False
        # флаг движения в границах кнопки "About It"
        self.motion_in_about_it_button = False
        # флаг движения в границах кнопки "Exit"
        self.motion_in_exit_button = False
        # флаг движения в границах кнопки "Play"
        self.motion_in_play_button = True
        # флаг достижения нового рекорда
        self.new_high_score_reached = False
        # получение значения рекорда из файла
        with open('record.txt', 'r') as f:
            self.high_score = f.read()

    def reset_stats(self):
        """Сброс некоторых статистических данных игры"""
        # установка кол-ва попыток по умолчанию
        self.ship_left = self.ai_settings.ship_limit
        # сброс счёта и уровня игры
        self.score = 0
        self.level = 1
        # сброс словаря с уровнем и значением счёта
        self.score_dict = {0: 0}
