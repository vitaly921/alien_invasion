class Settings:
    """Класс настроек игры"""
    def __init__(self):
        """Инициализирует настройки игры"""
        # задание настроек игровых элементов, не изменяющихся по ходу игры
        # параметры экрана
        self.screen_width = 1400
        self.screen_height = 750
        self.bg_color = (163, 102, 230)
        self.icon = 'images/icon.png'
        self.game_name = 'Alien Invasion'

        # параметры корабля (кроме скорости)
        #self.ship_speed_factor = 5
        self.ship_limit = 3

        # параметры пришельца
        self.image_alien = 'images/alien.png'
        self.image_boosted_alien = 'images/boosted_alien.png'
        self.image_damaged_alien = 'images/damaged_alien.png'
        self.alien_width = 60
        self.alien_height = 40
        # кол-во очков прочности "усиленного" пришельца
        self.allowed_count_hits = 4

        # параметры корабля игрока
        self.image_first_ship = 'images/ship1.png'
        self.image_second_ship = 'images/ship2.png'
        self.image_third_ship = 'images/ship3.png'
        self.ship_width = 80
        self.ship_height = 80


        # параметры пули (кроме скорости)
        #self.bullet_speed_factor = 7
        self.bullet_width_for_ship = 5
        self.bullet_height_for_ship = 15
        self.bullet_width_for_alien = 7
        self.bullet_height_for_alien = 25
        self.bullet_color_for_ship = (222, 164, 109)
        self.boosted_bullet_color_for_ship = (255, 0, 0)
        self.bullet_color_for_alien = (255, 55, 0)
        self.bullets_allowed_for_first_ship = 4
        self.bullets_allowed_for_second_ship = 6
        self.bullets_allowed_for_third_ship =6
        self.bullet_score = 500

        # параметры авиабомбы
        self.air_bomb_width = 40
        self.air_bomb_height = 30
        self.air_bombs_allowed = 1

        # параметры для эффекта взрыва
        self.explosion_width = 50
        self.explosion_height = 50
        self.explosion_duration = 500
        self.explosion_alpha = 200

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
        self.ship_speed_factor = 4
        # задание начальной скорости пули корабля игрока
        self.ship_bullet_speed_factor = 10
        # задание начальной скорости пули пришельца
        self.alien_bullet_speed_factor = 5
        # задание начальной скорости полета авиабомбы
        self.air_bomb_speed_factor = 7
        # задание начальной скорости кораблей пришельцев
        self.alien_speed_factor = 5
        # стартовые очки за пришельца
        self.alien_points = 200
        # начальное кол-во "усиленных" пришельцев
        self.count_boosted_aliens = 2
        # начальный флаг задания направления (при 1 - вправо, при -1 -влево)
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличение значений скорости игровых объектов"""
        self.ship_speed_factor *= self.speedup_scale
        self.ship_bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= self.score_scale
        self.count_boosted_aliens += 2
        self.air_bomb_speed_factor *= 1

