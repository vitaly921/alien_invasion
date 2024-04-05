import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from hint import Hint
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

    # создание кнопки Play, Pause, About It
    play_button = Button(ai_settings, screen, 'Play', 1, 1.1)
    pause_button = Button(ai_settings, screen, 'Pause', 1, 1.25)
    about_it_button = Button(ai_settings, screen, 'About It', 1, 1.35)
    back_button = Button(ai_settings, screen, 'Back', 0.5, 1.85)
    exit_button = Button(ai_settings, screen, 'Exit', 1, 1.6)

    # создание экземпляра надписи игры
    game_title = GameTitle(screen)

    hint_for_play_button = Hint(ai_settings.hint_for_play_button, screen, 1, 0.9)
    hint_for_pause_button = Hint(ai_settings.hint_for_pause_button, screen, 1, 1.5)
    hint_for_about_it_button = Hint('Это игра про какую-то дич', screen, 1, 1)

    # создание группы для хранения пуль, кораблей игрока, флота пришельцев и звезд
    bullets = Group()
    aliens = Group()
    stars = Group()
    ships = Group()
    explosions = Group()

    # наполнение группы кораблей различными экземплярами
    ships = gf.create_ships(ai_settings, screen, ships)
    # индекс для корабля группы
    number_ship = 0
    # получение экземпляра корабля из группы с определенным индексом
    ship = ships.sprites()[number_ship]

    # создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # создание группы звезд на экране
    gf.create_stars(ai_settings, screen, stars)

    # состояние паузы
    pause = False

    clock = pygame.time.Clock()
    # основной цикл программы
    while True:
        # обработка событий
        gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, pause_button, about_it_button,
                        sb, pause, hint_for_pause_button, back_button, exit_button)

        # действия только во время активного состояния игры
        if stats.game_active:
            # обновление позиций пуль и удаление пуль вышедших за верхний край экрана
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions)
            # обновление позиции флота пришельцев
            gf.update_aliens(ai_settings, aliens)
            # обновление координат, продолжительности и прозрачности эффекта взрыва
            gf.update_explosions(ai_settings, explosions)

        # обновление кораблей игрока (в т.ч. позиций) в различных состояниях игры
        number_ship, ship = gf.update_ships(ai_settings, stats, screen, number_ship, ships, ship, aliens, bullets, sb)
        # обновление позиции фона звёзд
        gf.update_stars(stars)
        # обновления экрана
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stars, stats, play_button, about_it_button,
                         game_title, sb, hint_for_play_button, hint_for_about_it_button, back_button, exit_button, explosions)
        #clock.tick(300)

# запуск игры
run_game()
