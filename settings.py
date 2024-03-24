class Settings:
    """Класс настроек игры"""
    def __init__(self):
        """Инициализирует настройки игры"""
        # задание настроек игровых элементов, не изменяющихся по ходу игры
        # параметры экрана
        self.screen_width = 1400
        self.screen_height = 750
        self.bg_color = (163, 102, 230)
        self.icon = 'images/ship_icon.png'
        self.game_name = 'Alien Invasion'

        # параметры корабля (кроме скорости)
        #self.ship_speed_factor = 5
        self.ship_limit = 3

        # параметры пули (кроме скорости)
        #self.bullet_speed_factor = 7
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (222, 164, 109)
        self.bullets_allowed = 4

        # настройки для флота пришельцев (кроме скорости)
        #self.alien_speed_factor = 1.5
        self.fleet_drop_speed = 20

        # темп ускорения игры
        self.speedup_scale = 1.2
        self.score_scale = 2

        # вызов функции, задающей динамически изменяющиеся настройки в начале игры
        self.initialize_dynamic_settings()

        # параметры кнопок игры
        self.button_width = 250
        self.button_height = 65
        self.button_color = (30, 120, 20)
        self.active_button_color = (210, 55, 75)
        self.button_text_color = (240, 255, 250)
        self.button_text_size = 70
        self.button_text_type = None

        # тексты подсказок
        self.hint_for_play_button = 'To start the game, press "Enter" on the keyboard or mouse on the "Play" button'
        self.hint_for_pause_button = 'To continue the game, press "Space"/ "Enter" on the keyboard or click on the Pause button'

    def initialize_dynamic_settings(self):
        """Инициализация настроек, изменяющихся по ходу игры"""
        # задание начальной скорости корабля игрока
        self.ship_speed_factor = 5
        # задание начальной скорости пуль
        self.bullet_speed_factor = 7
        # задание начальной скорости кораблей пришельцев
        self.alien_speed_factor = 8.5
        # стартовые очки за пришельца
        self.alien_points = 200
        # начальный флаг задания направления (при 1 - вправо, при -1 -влево)
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличение значений скорости игровых объектов"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= self.score_scale


