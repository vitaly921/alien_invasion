class GameStats:
    """Сбор статистики игры"""
    def __init__(self, ai_settings):
        """Инициализация статистики"""
        # флаг состояния игры
        self.game_active = False
        # получение значения рекорда из файла
        with open('record.txt', 'r') as f:
            self.high_score = f.read()
        # инициализация настроек и функции сброса статистики
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self):
        """Сброс некоторых статистических данных игры"""
        # установка кол-ва попыток по умолчанию
        self.ship_left = self.ai_settings.ship_limit
        # сброс счёта и уровня игры
        self.score = 0
        self.level = 1
        # сброс словаря с уровнем и значением счёта
        self.score_dict = {0: 0}
