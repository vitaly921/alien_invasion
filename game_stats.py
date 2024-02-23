class GameStats:
    """Сбор статистики игры"""
    def __init__(self, ai_settings):
        """Инициализация статистики"""
        # флаг состояния игры
        self.game_active = False

        self.ship_left = None
        self.ai_settings = ai_settings
        self.reset_stats()

    def reset_stats(self):
        """Задание нового доступного кол-ва кораблей для игры"""
        self.ship_left = self.ai_settings.ship_limit
        # задание счета игры
        self.score = 0

