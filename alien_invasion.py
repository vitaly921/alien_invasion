import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from game_title import GameTitle
from scoreboard import Scoreboard


def run_game():
    # инициализация библиотеки Pygame
    pygame.init()
    # создание экземпляра класса с настройками
    ai_settings = Settings()
    # создание окна для игры
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    # установка заголовка окна
    pygame.display.set_caption(ai_settings.game_name)
    # загрузка изображения для иконки окна
    icon = pygame.image.load(ai_settings.icon)
    # установка иконки окна
    pygame.display.set_icon(icon)

    # создание корабля
    #ship = Ship(ai_settings, screen)

    # создание экземпляров для хранения и вывода некоторой статистики
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # создание кнопки Play и Pause
    play_button = Button(ai_settings, screen, 'Play')
    pause_button = Button(ai_settings, screen, 'Pause')
    # создание экземпляра надписи игры
    game_title = GameTitle(screen)

    # создание группы для хранения пуль, флота пришельцев и звезд
    bullets = Group()
    aliens = Group()
    stars = Group()
    ships = Group()

    for ship_number in range(3):
        ship = Ship(ai_settings, screen, ship_number+1)
        ships.add(ship)

    print(ships)
    i = 0
    print(i)
    ship = ships.sprites()[i]
    # создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # создание группы звезд на экране
    gf.create_stars(ai_settings, screen, stars)

    pause = False

    clock = pygame.time.Clock()
    # основной цикл программы
    while True:
        # обработка событий
        gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, pause_button, sb, pause)

        # проверка флага состояния игры
        if stats.game_active:
            # обновление позиций пуль и удаление пуль вышедших за верхний край экрана
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb)
            # обновление позиции флота пришельцев
            i, ship = gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb, i, ships)
            # обновление позиции корабля
            ship.update()


        # обновление позиции фона звёзд
        gf.update_stars(stars)
        # обновления экрана
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars, stats, play_button, game_title, sb)
        #clock.tick(300)

# запуск игры
run_game()
