class Settings:
    """Файл настроек игры"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # параметры экрана
        self.screen_width = 1400
        self.screen_height = 750
        self.bg_color = (163, 102, 230)
        self.icon = 'images/ship_icon.png'
        self.game_name = 'Alien Invasion'

        # параметры корабля
        self.ship_speed_factor = 5
        self.ship_limit = 3

        # параметры пули
        self.bullet_speed_factor = 7
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (222, 164, 109)
        self.bullets_allowed = 4

        # настройки для флота пришельцев
        self.alien_speed_factor = 1.5
        self.fleet_drop_speed = 10
        # флаг задания направления (при 1 - вправо, при -1 -влево)
        self.fleet_direction = 1
