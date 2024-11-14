import random
import sys
import pygame
import math
from time import sleep, time
from random import randint

from Tools.demo.spreadsheet import center

from bullet import Bullet, ShipBullet, AlienBullet
from air_bomb import AirBomb
from alien import Alien, BoostedAlien
from star import Star
from ship import Ship
from explosion import Explosion, SmallExplosion
from pygame._sprite import Group


def create_ships(ai_settings, screen, ships):
    """Создание группы кораблей*"""
    # создание экземпляров кораблей и добавление их в группу
    for ship_number in range(ai_settings.ship_limit):
        # создание экземпляра корабля
        ship = Ship(ai_settings, screen, ship_number+1)
        # добавление экземпляра в группу
        ships.add(ship)
    # возврат группы
    return ships

def play_background_music(music_path, loop=-1):
    """Функция для проигрывания выбранной фоновой музыки"""
    # загрузка нужной фоновой музыки (аргумент содержит путь)
    pygame.mixer.music.load(music_path)
    # проигрывание фоновой музыки с бесконечным повтором
    pygame.mixer.music.play(loop)


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, pause_button, about_it_button,
                 sb, pause, hint_for_pause_button, back_button, exit_button, air_bombs, explosions, ship_type):
    """Обработка событий в игре"""
    for event in pygame.event.get():
        # обработка события закрытия окна игры
        if event.type == pygame.QUIT:
            # запись в файл обновленного значения рекорда
            with open('record.txt', 'w') as f:
                f.write(str(stats.high_score))
            sys.exit()
        # обработка события нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb, pause, pause_button,
                                 hint_for_pause_button, air_bombs, explosions, ship_type)
        # обработка события отпускания клавиш
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        # обработка события нажатия любой клавиши мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_button_down_events(stats, play_button, ship, aliens, bullets, ai_settings, screen, sb,
                                           about_it_button, back_button, exit_button)
        # обработка события движения курсора мыши
        elif event.type == pygame.MOUSEMOTION:
            check_mouse_motion_events(ai_settings, event, play_button, about_it_button, exit_button, back_button,
                                      stats)


def check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb, pause, pause_button,
                         hint_for_pause_button, air_bombs, explosions, ship_type):
    """Реагирует на нажатие клавиш"""
    # Обработка нажатия Escape
    if event.key == pygame.K_ESCAPE:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # вызов функции для сохранения рекорда игры
        save_record(stats)
        sleep(0.3)
        # закрытие окна программы
        sys.exit()

    # обработка нажатия стрелок (вверх, низ, лево, право)
    elif event.key == pygame.K_RIGHT and stats.game_active:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT and stats.game_active:
        ship.moving_left = True
    elif event.key == pygame.K_UP and stats.game_active:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN and stats.game_active:
        ship.moving_down = True

    # обработка нажатия Space
    elif event.key == pygame.K_SPACE:
        # вызов функции открытия огня по противнику
        fire_bullet(ai_settings, screen, ship, bullets, stats, explosions, ship_type)
    # обработка нажатия клавиш Shift
    elif event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
        # вызов функции для сброса авиабомб
        drop_air_bomb(ai_settings, screen, ship, air_bombs, stats)
    # обработка нажатия клавиш "Enter" во время неактивной игры
    elif ((event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and not stats.game_active and
          not stats.press_about_it_button):
        # вызов функции для начала игры
        start_game(stats, aliens, ai_settings, screen, ship, sb)
    # обработка нажатия клавиши "Backspace" во время неактивной игры в режиме просмотра информации
    elif event.key == pygame.K_BACKSPACE and not stats.game_active and stats.press_about_it_button:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # флаг состояния режима просмотра информации = False
        stats.press_about_it_button = False
    # обработка нажатия клавиши "F1" во время неактивной игры главного меню
    elif event.key == pygame.K_F1 and not stats.game_active and not stats.press_about_it_button:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # флаг состояния режима просмотра информации = True
        stats.press_about_it_button = True
    # обработка нажатия клавиши "p" во время активной игры
    elif event.key == pygame.K_p and stats.game_active:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # вызов функции для задания паузы игры
        pause_game(ai_settings, ship, stats, pause, pause_button, hint_for_pause_button)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш стрелок"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_mouse_button_down_events(stats, play_button, ship, aliens, bullets, ai_settings, screen, sb, about_it_button,
                                   back_button, exit_button):
    """Функция для обработки события при нажатии кнопок мыши"""
    # получение координат точки нажатия клавиши
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # проверка нажатия клавиш мыши в пределах кнопок Play, About It, Exit, Back
    check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, sb)
    check_about_it_button(ai_settings, mouse_x, mouse_y, about_it_button, stats, screen)
    check_back_button(ai_settings, mouse_x, mouse_y, stats, back_button)
    check_exit_button(ai_settings, mouse_x, mouse_y, stats, exit_button)


def check_mouse_motion_events(ai_settings, event, play_button, about_it_button, exit_button, back_button,
                              stats):
    """Функция для обработки события движения мыши"""
    # изменение цвета кнопок Play, About It, Exit, Back
    change_color_button(ai_settings, event, play_button)
    change_color_button(ai_settings, event, about_it_button)
    change_color_button(ai_settings, event, exit_button)
    change_color_button(ai_settings, event, back_button)
    # изменение подсказок для кнопок About It, Exit
    change_hint_button(event, exit_button, stats, exit_button.msg)
    change_hint_button(event, about_it_button, stats, about_it_button.msg)


def change_hint_button(event, button, stats, msg='Play'):
    """Функция изменения текста подсказок при наведении на кнопки"""
    if button.rect.collidepoint(event.pos):
        # если мышь наведена на кнопку "Exit"
        if msg == 'Exit':
            # изменение состояния флага движения курсора для этой кнопки
            stats.motion_in_exit_button = True
        # если мышь наведена на кнопку "About It"
        elif msg == 'About It':
            # изменение состояния флага движения курсора для этой кнопки
            stats.motion_in_about_it_button = True
    else:
        if msg == 'Exit':
            # изменение состояния флага движения курсора для этой кнопки
            stats.motion_in_exit_button = False
        # если мышь находится за пределами кнопки "About It"
        elif msg == 'About It':
            # изменение состояния флага движения курсора для этой кнопки
            stats.motion_in_about_it_button = False


def change_color_button(ai_settings, event, button):
    """Изменение цвета кнопки при наведении на неё курсором мыши и подсказки"""
    # при нахождении курсора мыши в пределах кнопки
    if button.rect.collidepoint(event.pos):
        # изменение цвета фона кнопки
        button.button_color = ai_settings.active_button_color
        button.prep_msg(button.msg)

    # при нахождении курсора за пределами кнопки
    else:
        # задание стандартного цвета фона
        button.button_color = ai_settings.button_color
        button.prep_msg(button.msg)


def check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, sb):
    """Проверка нажатия мышью кнопки Play и новый запуск игры в активном состоянии"""
    # флаг нажатия кнопки мыши в пределах кнопки Play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # запуск новой игры при нажатии мыши на область кнопки Play, текущем неактивном состоянии игры и при нахождении
    # пользователя в главном меню
    if button_clicked and not stats.game_active and not stats.press_about_it_button:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # вызов функции настройки игровых элементов при старте
        start_game(stats, aliens, ai_settings, screen, ship, sb)


def check_about_it_button(ai_settings, mouse_x, mouse_y, about_it_button, stats, screen):
    """Проверка нажатия мышью кнопки About It"""
    # флаг нажатия кнопки мыши в пределах кнопки About It
    button_clicked = about_it_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая если нажатие происходит в пределах области кнопки
    if button_clicked:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # переход игры в состояние, в котором отображается описание игры
        stats.press_about_it_button = True



def check_back_button(ai_settings, mouse_x, mouse_y, stats, back_button):
    """Проверка нажатия мышью кнопки Back"""
    # флаг нажатия кнопки мыши в пределах кнопки Back
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая если нажатие происходит в пределах области кнопки
    if button_clicked:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # переход игры в главное меню
        stats.press_about_it_button = False


def check_exit_button(ai_settings, mouse_x, mouse_y, stats, exit_button):
    """Проверка нажатия мышью кнопки Exit"""
    # флаг нажатия кнопки мыши в пределах кнопки Exit
    button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая если нажатие происходит в пределах области кнопки и в главном меню игры
    if button_clicked and not stats.press_about_it_button:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # закрытие окна игры
        sleep(0.3)
        pygame.quit()
        quit()


def save_record(stats):
    """Сохранение рекорда игры"""
    # запись в файл обновленного значения рекорда
    with open('record.txt', 'w') as f:
        f.write(str(stats.high_score))


def fire_bullet(ai_settings, screen, ship, bullets, stats, explosions, ship_type):
    """Позволяет совершить выстрел если максимум пуль еще не достигнут"""
    # если текущий корабль первый
    if ship_type == 0:
        # если кол-во пуль меньше максимально допустимого значения для первого корабля и игра в активном состоянии
        if len(bullets) < ai_settings.bullets_allowed_for_first_ship and stats.game_active:
            # вызов функции для создания эффекта выстрела в центре корабля (по-умолчанию)
            create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, play_sound=True)

    # если текущий корабль второй
    elif ship_type == 1:
        # если кол-во пуль меньше максимально допустимого значения для второго корабля и игра в активном состоянии
        if len(bullets) < ai_settings.bullets_allowed_for_second_ship and stats.game_active:
            # вызов функции для создания эффекта выстрела в левой части корабля
            create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, shot_location='left', play_sound=True)
            # вызов функции для создания эффекта выстрела в правой части корабля
            create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, shot_location='right')

    # если текущий корабль третий
    elif ship_type == 2:
        # если кол-во пуль меньше максимально допустимого значения для третьего корабля и игра в активном состоянии
        if len(bullets) < ai_settings.bullets_allowed_for_third_ship and stats.game_active:
            # вызов функции для создания эффекта выстрела в левой части корабля
            create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, shot_location='left')
            # вызов функции для создания эффекта выстрела в центре корабля (по-умолчанию)
            create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, boosted=True, play_sound=True)
            # вызов функции для создания эффекта выстрела в правой части корабля
            create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, shot_location='right')


def create_ship_bullet_and_small_explosions(ai_settings, screen, ship, ship_type, bullets, explosions, shot_location='center', boosted=False, play_sound=False):
    """Создание эффекта выстрела в заданном месте корабля"""
    # создание новой пули корабля в заданном месте
    new_bullet = ShipBullet(ai_settings, screen, ship, ship_type, shot_location, boosted)
    # создание эффекта выстрела в заданном месте
    new_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type, shot_location)
    # проверка флага для единственного воспроизведения звука
    if play_sound:
        # настройка громкости звука
        ai_settings.ship_shoot_sound.set_volume(0.25)
        # воспроизведение звука
        ai_settings.ship_shoot_sound.play()
    # добавление пули и эффекта выстрела в группы
    explosions.add(new_small_explosions)
    bullets.add(new_bullet)


def drop_air_bomb(ai_settings, screen, ship, air_bombs, stats):
    """Функция для создания авиабомб"""
    # если во время игры бомба на экране отсутствует
    if len(air_bombs) < ai_settings.air_bombs_allowed and stats.game_active:
        # создание экземпляра новой бомбы
        new_air_bomb = AirBomb(ai_settings, screen, ship)
        # добавление бомбы в список
        air_bombs.add(new_air_bomb)
        # проигрывание звука падения авиабомбы и регулировка громкости
        ai_settings.ship_aviabomb_sound.set_volume(0.15)
        ai_settings.ship_aviabomb_sound.play()


def start_game(stats, aliens, ai_settings, screen, ship, sb):
    """Функция настройки игровых элементов при старте игры"""
    # сброс скоростей игровых элементов
    ai_settings.initialize_dynamic_settings()
    # сброс флагов движения корабля
    reset_moving_flags_ship(ship)
    # скрытие курсора мыши
    pygame.mouse.set_visible(False)
    # остановка мелодии главного меню
    pygame.mixer.music.stop()
    # вызов функции для проигрывания фоновой музыки боя
    play_background_music(ai_settings.battle_music)
    # вызов функции для отрисовки статистических данных (счет, рекорд, уровень, оставшиеся корабли) в виде изображений
    sb.prep_images()
    # переход игры в активный режим
    stats.game_active = True
    # создание нового флота пришельцев
    create_fleet(ai_settings, screen, ship, aliens, stats)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисление количества пришельцев в ряду"""
    # определение доступного пространства по Х: ширина экрана - (коэфф.*ширина корабля пришельца)
    available_space_x = ai_settings.screen_width - 5 * alien_width
    # целое число пришельцев в ряду: пространство по Х / (ширина пришельца * доп. пространство его ширины) - переменная
    number_aliens_x = int(available_space_x / (1.5 * alien_width)-1)
    return number_aliens_x


def get_number_rows_aliens(ai_settings, ship_height, alien_height):
    """Вычисление количества рядов пришельцев на экране"""
    # вычисление доступного пространства по Y: высота экрана - (коэфф.*высоту пришельца) - высота корабля игрока
    available_space_y = ai_settings.screen_height - (8 * alien_height) - ship_height
    # целое количество рядов: пространство по Y / (коэфф.*высоту пришельца)
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, boosted=False):
    """Создание пришельца в ряду"""
    if boosted:
        alien = BoostedAlien(ai_settings, screen)
    else:
        # создание нового экземпляра пришельца для его отображения
        alien = Alien(ai_settings, screen)

    # вычисление ширины и высоты пришельца
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    # задание координаты Х пришельца:
    # координата по Х: половина ширины пришельца + доп.пространство (коэфф.)*ширина пришельца * номер в ряду
    alien.x = alien_width / 2 + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    # координата по Y: половина высоты пришельца + доп.пространство (коэфф.)*высоту пришельца * номер ряда
    alien.y = alien_height/2 + 1.5 * alien_height * row_number
    alien.rect.y = alien.y
    # добавление созданного пришельца в группу
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, stats):
    """Создание флота пришельцев"""
    # создание экземпляра пришельца для вычисления его ширины и высоты
    alien = Alien(ai_settings, screen)
    # вычисление количества пришельцев в ряду
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # вычисление количества рядов пришельцев
    number_rows_aliens = get_number_rows_aliens(ai_settings, ship.rect.height, alien.rect.height)

    # задание кол-ва "усиленных пришельцев"
    count_boosted_aliens = ai_settings.count_boosted_aliens
    # случайный выбор индексов для "усиленных" пришельцев
    index_boosted_aliens = random.sample(range(number_aliens_x*number_rows_aliens), count_boosted_aliens)

    # для каждого ряда из списка доступных
    for row_number in range(number_rows_aliens):
        # для каждого пришельца в ряду
        for alien_number in range(number_aliens_x):
            # если индекс пришельца входит в список индексов для "усиленных" пришельцев
            if (row_number * number_aliens_x + alien_number) in index_boosted_aliens:
                # создание "усиленного" пришельца в ряду
                create_alien(ai_settings, screen, aliens, alien_number, row_number, boosted=True)
            else:
                # создание базового пришельца в ряду
                create_alien(ai_settings, screen, aliens, alien_number, row_number)


def pause_game(ai_settings, ship, stats, pause, pause_button, hint_for_pause_button):
    """Обработка паузы в игре"""
    # флаг паузы переходит в значение True
    pause = not pause
    # сброс флагов движения корабля
    reset_moving_flags_ship(ship)
    # постановка фоновой музыки боя на паузу
    pygame.mixer.music.pause()
    # отображение курсора мыши
    pygame.mouse.set_visible(True)
    # отображение подсказки во время паузы
    hint_for_pause_button.blitme()
    # звук игры в режиме паузы и настройка громкости
    ai_settings.pause_sound.set_volume(0.3)
    ai_settings.pause_sound.play(-1)
    # основной цикл паузы
    while pause:
        # вызов функции обработки событий во время паузы с проверкой состояния флага паузы
        pause = check_events_for_pause(ai_settings, stats, pause_button, pause)
        # обновление экрана для отрисовки кнопки паузы
        pygame.display.flip()


def reset_moving_flags_ship(ship):
    """Сброс флагов движения корабля"""
    ship.moving_left = False
    ship.moving_right = False
    ship.moving_up = False
    ship.moving_down = False


def check_events_for_pause(ai_settings, stats, pause_button, pause):
    """Обработка событий игры во время паузы"""
    # отслеживание определённых событий во время паузы
    # переход игры в неактивное состояние
    stats.game_active = False
    # отрисовка кнопки паузы
    pause_button.draw_button()
    for event in pygame.event.get():
        # обработка события выхода из игры
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # обработка события нажатия клавиш
        elif event.type == pygame.KEYDOWN:
            # вызов функции обработки событий нажатия клавиш в режиме паузы с возвратом состояния паузы
            pause = check_keydown_events_for_pause(ai_settings, event, stats, pause)
        # обработка события нажатия любой кнопки мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # вызов функции обработки событий нажатия кнопок мыши в режиме паузы с возвратом состояния паузы
            pause = check_mouse_button_down_for_pause(ai_settings, stats, pause, pause_button)
        # обработка события движения мыши
        elif event.type == pygame.MOUSEMOTION:
            # вызов функции для изменения цвета кнопки
            change_color_button(ai_settings, event, pause_button)
    return pause


def check_keydown_events_for_pause(ai_settings, event, stats, pause):
    """Функция обработки событий нажатия клавиш в режиме паузы с возвратом состояния паузы"""
    # обработка нажатия клавиш "Enter" или "Space"
    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_KP_ENTER:
        # вызов функции окончания паузы
        pause = exit_from_pause_to_active_game(pause, stats)
        # остановка проигрывания звука для паузы
        ai_settings.pause_sound.stop()
    # случай нажатия клавиши Escape
    elif event.key == pygame.K_ESCAPE:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        sleep(0.3)
        # выход из игры
        pygame.quit()
        quit()
    # обработка нажатия клавиши Backspace
    elif event.key == pygame.K_BACKSPACE:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # флаг паузы переход в состояние False
        pause = False
        # изменение флага для разрешения проигрывания мелодии достижения рекорда игры
        stats.new_high_score_reached = False
        # остановка фоновой музыки для боя
        pygame.mixer.music.stop()
        # остановка проигрывания звука для паузы
        ai_settings.pause_sound.stop()
        # вызов функции для проигрывания фоновой музыки главного меню
        play_background_music(ai_settings.main_menu_music)
        # проигрывание музыки для главного меню
        pygame.mixer.music.play()
        # сброс статистики
        stats.reset_stats()
    return pause


def check_mouse_button_down_for_pause(ai_settings, stats, pause, pause_button):
    """Функция обработки событий нажатия кнопок мыши в режиме паузы с возвратом состояния паузы"""
    # получение координат точки нажатия клавиши
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # получение флага нажатия кнопки мыши в пределах области кнопки паузы
    button_clicked = pause_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая нажатия кнопки мыши в пределах области кнопки паузы
    if button_clicked:
        # звук нажатия на кнопку
        ai_settings.button_clicked_sound.play()
        # вызов функции окончания паузы
        pause = exit_from_pause_to_active_game(pause, stats)
        # остановка проигрывания звука для паузы
        ai_settings.pause_sound.stop()
    return pause


def exit_from_pause_to_active_game(pause, stats):
    """Функция окончания паузы"""
    # флаг паузы переходит в состояние false, что приводит к выходу из цикла и окончанию паузы
    pause = False
    # скрытие курсора мыши
    pygame.mouse.set_visible(False)
    # переход игры в активное состояние
    stats.game_active = True
    # снятие с паузы фоновой музыки боя
    pygame.mixer.music.unpause()
    return pause



def update_screen(ai_settings, screen, ship, aliens, bullets, stars, stats, play_button, about_it_button, game_title,
                  sb, hint_for_play_button, hint_for_about_it_button, back_button, exit_button, explosions, air_bombs,
                  alien_bullets, description_text_surfaces, description_image_ships_surface, hint_for_exit_button,
                  description_title_surface):
    """Обновляет экран и показывает всё содержимоё на нём"""
    # вариант заполнения экрана сплошным цветом фона
    # screen.fill(ai_settings.bg_color)

    # создание и конвертация поверхности градиента
    gradient_surface = create_gradient(ai_settings.screen_width, ai_settings.screen_height)
    gradient_surface = gradient_surface.convert()
    # отрисовка поверхности градиента как цвета фона
    screen.blit(gradient_surface, (0, 0))
    # отрисовка группы звезд
    stars.draw(screen)

    # поочередная отрисовка пуль корабля игрока
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # поочередная отрисовка авиабомб
    for air_bomb in air_bombs.sprites():
        air_bomb.draw_air_bomb()
    # поочередная отрисовка пуль корабля пришельца
    for bullet in alien_bullets.sprites():
        bullet.draw_bullet()

    # отрисовка корабля игрока
    ship.blitme()
    #aliens.draw(screen)
    # отображение рекорда
    sb.show_high_score()
    # отрисовка взрывов
    #explosions.draw(screen)

    # действия во время неактивной игры
    if not stats.game_active:
        # действия во время неактивной игры при переходе в меню описания
        if stats.press_about_it_button:
            # вызов функции для отображения описания игры
            show_game_description(screen, description_title_surface, description_text_surfaces,
                                  description_image_ships_surface)
            # отображения кнопки "Back" для возврата в главное меню
            back_button.draw_button()
        # действия во время неактивной игры при отсутствии перехода в меню описания
        else:
            if not stats.motion_in_about_it_button and not stats.motion_in_exit_button:
                hint_for_play_button.blitme()
            elif stats.motion_in_exit_button:
                hint_for_exit_button.blitme()
            elif stats.motion_in_about_it_button:
                hint_for_about_it_button.blitme()

            # очистка групп пришельцев, пуль, взрывов, центровка корабля
            aliens.empty()
            bullets.empty()
            alien_bullets.empty()
            air_bombs.empty()
            explosions.empty()
            ship.center_ship()

            # отрисовка заглавия игры
            game_title.blitme()
            # отрисовка кнопок Play, About It, Exit
            play_button.draw_button()
            exit_button.draw_button()
            about_it_button.draw_button()

    # действия во время активной игры
    else:
        # отображение текущего счёта
        sb.show_score()
        # отрисовка взрывов
        explosions.draw(screen)
        # отрисовка группы пришельцев
        aliens.draw(screen)

    # обновление окна
    pygame.display.flip()


def show_game_description(screen, description_title_surface, description_text_surfaces, description_image_ships_surface):
    """Функция для отображения готовых блоков описания игры в меню описания"""
    # отображение и задание расположения поверхности с текстом заглавия описания
    screen.blit(description_title_surface, (500,15))
    # отображение и задание расположения поверхности с основным текстом описания игры
    screen.blit(description_text_surfaces, (50, 100))
    # отображение и задание расположения поверхности с изображениями и текстом описания кораблей игрока
    screen.blit(description_image_ships_surface, (150, 350))


def prepare_title_surfaces():
    """Функция создания блока заглавия описания"""
    # задание размера и шрифта
    title_font = pygame.font.SysFont('arialblack', 48)
    # задание надписи
    title_text = "Правила игры"
    # формирование изображения с белым текстом
    title_surface = title_font.render(title_text, True, 'white')
    # регулировка прозрачности
    title_surface.set_alpha(255)
    # возврат поверхности
    return title_surface


def prepare_text_surfaces():
    """Функция создания блока основного текста описания"""
    # задание стиля текста строк
    line_font = pygame.font.SysFont('arial', 24)
    # создание пустого массива для готовых изображений строк
    line_surfaces =[]
    # задание переменной для подсчета максимальной длины строки
    max_line_width = 0
    # подсчет высоты строки
    max_line_height = line_font.get_height()+10

    # открытие файла с текстом описания игры
    with open('description.txt', 'r', encoding='utf-8') as file:
        # чтение текста из файла по строкам
        game_description = file.readlines()
    # перебор каждой строки
    for line in game_description:
        # создание изображения строки без лишних пробелов белого цвета
        line_surface = line_font.render(line.strip(), True, 'white')
        # добавление изображения строки в массив
        line_surfaces.append(line_surface)
        # проверка длины изображения строки для поиска максимальной
        if line_surface.get_width() > max_line_width:
            # обновление максимальной длины изображения строки
            max_line_width = line_surface.get_width()

    # подсчет высоты для общей поверхности, вмещающей все строки
    surface_height = max_line_height*len(line_surfaces)
    # создание общей поверхности длиной максимальной строки текста и вычисленной высоты
    text_surface = pygame.Surface((max_line_width, surface_height), pygame.SRCALPHA)
    text_surface = text_surface.convert_alpha()

    # задание отступа по оси Y относительно новой поверхности
    y_offset = 0
    # для каждого изображения строки из массива изображений
    for line_surface in line_surfaces:
        # отрисовка каждой строки на заданной поверхности
        text_surface.blit(line_surface, (0, y_offset))
        # задание нового отступа
        y_offset += max_line_height
    # возврат готовой поверхности с текстом
    return text_surface


def prepare_images_ships_surface(ai_settings, ships):
    """Функция создания блока изображений кораблей с их текстовым описанием"""
    # задание начальной длины общей поверхности
    images_surface_width = 0
    # задание начальной высоты общей поверхности
    images_surface_height = 0
    # задание начальной длины поверхности текста описания изображения
    description_image_surface_max_width = 0
    # задание стиля для текста описания изображения
    description_line_image = pygame.font.SysFont('arial', 26)
    #print(pygame.font.get_fonts())
    # создание пустого массива для хранения изображений текстов описания кораблей
    description_line_image_surfaces = []

    # загрузка в словарь данных кораблей игрока (изображения и текста описания)
    ships_info = {
        'ship1' : {'image' : ships.sprites()[0].image, 'description' : ai_settings.description_first_ship},
        'ship2': {'image': ships.sprites()[1].image, 'description': ai_settings.description_second_ship},
        'ship3': {'image': ships.sprites()[2].image,'description': ai_settings.description_third_ship}
    }
    # подсчёт длины изображения корабля игрока (одинаков для всех изображений)
    images_surface_width = ships_info['ship1']['image'].get_width()
    # для каждого ключа и значения словаря
    for ship_key, ship_data in ships_info.items():
        # обновление высоты общей поверхности: высота изображения плюс отступ
        images_surface_height += ship_data['image'].get_height() + 20
        # создания изображения текста описания корабля
        description_line_image_surface = description_line_image.render(ship_data['description'].strip(), True, 'white')
        # добавление в массив изображений текстов описания кораблей
        description_line_image_surfaces.append(description_line_image_surface)
        # проверка и обновление максимальной длины изображения текста описания корабля
        if description_line_image_surface.get_width() > description_image_surface_max_width:
            description_image_surface_max_width = description_line_image_surface.get_width()
    # обновление длины общей поверхности с учетом отступа от изображения и максимальной длины текста описания
    images_surface_width +=  description_image_surface_max_width + 20
    # формирование основной поверхности
    images_surface = pygame.Surface((images_surface_width, images_surface_height), pygame.SRCALPHA)
    images_surface = images_surface.convert_alpha()

    # задание отступа по y
    y_offset = 0
    # для каждого ключа и значения в словаре
    for ship_key, ship_image in ships_info.items():
        # добавление на общую поверхность изображения кораблей с некоторым отступом
        images_surface.blit(ship_image['image'], (0, y_offset))
        # увеличение отступа по y
        y_offset += 100

    # обновление отступа по y для изображений текста описания
    y_offset = ships_info['ship1']['image'].get_height()/2
    # для каждого текста описания из массива
    for description_line_image_surface in description_line_image_surfaces:
        # добавление на общую поверхность изображения текста описания с некоторым отступом
        images_surface.blit(description_line_image_surface, (100,y_offset))
        # увеличение отступа по y
        y_offset += 100
    # возврат общей поверхности
    return images_surface


def create_gradient(width, height):
    """Создание поверхности градиента из двух цветов"""
    gradient_surface = pygame.Surface((width, height))
    # начальный/конечный цвета градиента фона
    start_color = (7, 16, 40)
    end_color = (9, 114, 167)
    # использование линейной интерполяции для нахождения промежуточного цвета для каждой строки
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
        # заполнение каждой строки поверхности промежуточным цветом
        gradient_surface.fill((r, g, b), (0, y, width, 1))
    # возврат градиентной поверхности
    return gradient_surface


def update_ship_projectiles(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions, air_bombs, alien_bullets):
    """Обновление позиций пуль/авиабомб, проверка их столкновения с пришельцами"""
    # обновление позиции пуль/авиабомб
    bullets.update()
    air_bombs.update()
    # для каждой пули из списка
    for bullet in bullets.copy():
        # для случая достижения нижней части пули верхней части экрана
        if bullet.rect.bottom <= 0:
            # удаление пули
            bullets.remove(bullet)
    # для каждой авиабомбы из списка
    for air_bomb in air_bombs.copy():
        # для случая достижения верхней части авиабомбы нижней части экрана
        if air_bomb.rect.top > air_bomb.screen_rect.bottom:
            # удаление авиабомбы
            air_bombs.remove(air_bomb)

    # функция проверки и обработки столкновения авиабомб/пуль с флотом пришельцев
    check_ship_projectiles_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions, air_bombs,
                                           alien_bullets)


def check_ship_projectiles_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions, air_bombs,
                                           alien_bullets):
    """Обработка столкновений пуль/авиабомб игрока с пришельцами и их пулями"""
    # создание группы усиленных пуль корабля игрока
    boosted_bullets = Group()
    # проверка каждой пули и добавление усиленных пуль в группу
    for bullet in bullets.copy():
        if bullet.boosted:
            bullet.add(boosted_bullets)

    # обработка столкновения усиленных пуль игрока с пришельцами: при столкновении удаляются только пришельцы
    boosted_bullets_aliens_collisions = pygame.sprite.groupcollide(boosted_bullets, aliens, False, True)
    # обработка столкновений пуль с пришельцами: при столкновении удаляется и пуля и пришелец
    bullets_aliens_collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    # обработка столкновений авиабомб с пришельцами: при столкновении удаляются только пришельцы
    air_bombs_aliens_collisions = pygame.sprite.groupcollide(air_bombs, aliens, True, True)
    # обработка столкновения пули игрока с пулей пришельца: взаимное уничтожение
    bullets_collision = pygame.sprite.groupcollide(bullets, alien_bullets, True, True)

    # для случая столкновения пуль с пришельцами
    if bullets_aliens_collisions:
        # дальнейшая обработка
        handle_collision(bullets_aliens_collisions, ai_settings, screen, explosions, stats, sb, aliens)
    # для случая столкновения авиабомб с пришельцами
    elif air_bombs_aliens_collisions:
        for air_bomb, collide_alien in air_bombs_aliens_collisions.items():
            explosion_center_x = air_bomb.rect.centerx
            explosion_center_y = air_bomb.rect.centery
            print(f'Center Explosion: ({explosion_center_x}, {explosion_center_y})')

            for alien in aliens:
                alien_center_x = alien.rect.centerx
                alien_center_y = alien.rect.centery

                distance = math.sqrt((alien_center_x - explosion_center_x)**2 + (alien_center_y - explosion_center_y)**2)
                if distance <= 100:
                    create_explosion(explosions, ai_settings, screen, alien, for_alien=True)
                    aliens.remove(alien)
        # дальнейшая обработка
        handle_collision(air_bombs_aliens_collisions, ai_settings, screen, explosions, stats, sb, aliens)
    # для случая столкновения снарядов корабля и пришельца друг с другом
    elif bullets_collision:
        # обновление счёта игры
        update_score(ai_settings, stats, aliens, sb, for_bullets=True)
    # для случая столкновения усиленных пуль с пришельцами
    elif boosted_bullets_aliens_collisions:
        # дальнейшая обработка
        handle_collision(boosted_bullets_aliens_collisions, ai_settings, screen, explosions, stats, sb, aliens)

    # проверка полного уничтожения флота пришельцев
    check_destroy_aliens(aliens, bullets, ai_settings, stats, sb, screen, ship, air_bombs, explosions, alien_bullets,
                         bullets_aliens_collisions, air_bombs_aliens_collisions, boosted_bullets_aliens_collisions)

def handle_collision(collisions, ai_settings, screen, explosions, stats, sb, aliens):
    """Функция для создания эффекта взрыва в месте столкновения и обновления счета"""
    # для каждой пули / авиабомбы при столкновении
    for bullet in collisions.copy():
        # сохранение списка пришельцев, по которым попала пуля / авиабомба игрока
        aliens = collisions[bullet]
        # для каждого пришельца с которым столкнулась пуля / авиабомба
        for alien in aliens:
            # проверка пришельца на принадлежность к классу "усиленных"
            if isinstance(alien, BoostedAlien):
                # уменьшение прочности "усиленного" корабля пришельца
                alien.hit(ai_settings)
                # проигрывание звука попадания по "усиленному" кораблю
                ai_settings.damage_alien_sound.play()
            # для случая принадлежности пришельца к базовому классу
            else:
                # удаление пришельца из группы
                alien.kill()
            # вызов функции для создания эффекта взрыва конкретного корабля
            create_explosion(explosions, ai_settings, screen, alien, for_alien=True)
        # вызов функции для обновления счета игры и проверки рекорда
        update_score(ai_settings, stats, aliens, sb)


def create_explosion(explosions, ai_settings, screen, game_ship, for_alien=False):
    """Функция создания эффекта взрыва для корабля игрока/пришельца"""
    # создание экземпляра взрыва по координатам пришельца
    if for_alien:
        explosion = Explosion(ai_settings, screen, game_ship, for_alien=True)
    # создание экземпляра взрыва по координатам корабля игрока
    else:
        explosion = Explosion(ai_settings, screen, game_ship)
    # проигрывание звука выстрела пришельца
    ai_settings.explosion_sound.set_volume(0.5)
    ai_settings.explosion_sound.play()
    # добавление экземпляра в группу
    explosions.add(explosion)


def update_score(ai_settings, stats, aliens, sb, for_bullets=False):
    """Функция для обновления счета игры и проверки рекорда"""
    # для случая если флаг for_bullets активен
    if for_bullets:
        # фиксированное увеличение счета игры
        stats.score += ai_settings.bullet_score
        # проигрывание звука попадания снарядов друг в друга
        ai_settings.bullet_shot_bullet_sound.play()
    else:
        # увеличение значения счёта, который учитывает все попадания одного снаряда
        stats.score += ai_settings.alien_points * len(aliens)
    # обновление словаря со значением счёта игры на текущем уровне
    stats.score_dict[stats.level] = stats.score
    # формирование изображения с текстом обновленного счёта
    sb.prep_score()
    # проверка достижения рекордного счёта
    check_high_score(ai_settings, stats, sb)


def check_high_score(ai_settings, stats, sb):
    """Проверка достижения нового рекорда"""
    if stats.score > int(stats.high_score):
        # обновление рекорда
        stats.high_score = stats.score
        # проверка флага для одноразового проигрывания мелодии достижения рекорда
        if not stats.new_high_score_reached:
            # проигрывание мелодии достижения рекорда игры и настройка громкости
            ai_settings.record_sound.set_volume(0.8)
            ai_settings.record_sound.play()
            # изменение флага для запрета дальнейшего проигрывания мелодии
            stats.new_high_score_reached = True

        # формирование и вывод изображения с рекордом
        sb.prep_high_score()


def check_destroy_aliens(aliens, bullets, ai_settings, stats, sb, screen, ship, air_bombs, explosions, alien_bullets,
                         bullets_aliens_collisions, air_bombs_aliens_collisions, boosted_bullets_aliens_collisions):
    """Функция для проверки полного уничтожения флота пришельцев и перехода на новый уровень игры"""
    # для случая отсутствия флота пришельцев после его уничтожения
    if len(aliens) == 0 and (bullets_aliens_collisions or air_bombs_aliens_collisions or boosted_bullets_aliens_collisions):
        # вызов функции для отображения взрыва последнего корабля пришельца
        show_last_alien_explosion(explosions)
        # функция перехода на новый уровень игры
        start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship, air_bombs, explosions, alien_bullets)


def show_last_alien_explosion(explosions):
    """Функция для отображения эффекта взрыва последнего пришельца
    при попадании по нему пули/авиабомбы"""
    # сохранение последнего эффекта взрыва
    last_explosion = explosions.sprites()[-1:]
    # отображение последнего эффекта взрыва
    last_explosion[0].blitme()
    # обновление экрана
    pygame.display.flip()


def start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship, air_bombs, explosions, alien_bullets):
    """Функция перехода игры на новый уровень"""
    # сброс флагов движения корабля в состояние False
    reset_moving_flags_ship(ship)
    # задание временной паузы
    sleep(1.5)
    # очистка списка оставшихся пуль, авиабомб, взрывов
    bullets.empty()
    air_bombs.empty()
    explosions.empty()
    alien_bullets.empty()

    # вызов функции увеличения скорости игровых объектов
    ai_settings.increase_speed()
    # увеличение уровня игры
    stats.level += 1
    # обновление изображения с уровнем игры
    sb.prep_level()

    # создание нового флота пришельцев
    create_fleet(ai_settings, screen, ship, aliens, stats)
    # вызов функции проверки нахождения корабля игрока в месте появления нового флота пришельцев
    check_location_ship(ship, aliens)


def check_location_ship(ship, aliens):
    """Функция проверки местонахождения корабля игрока"""
    # сохранение последнего пришельца (который в самом низу флота) в переменной
    last_alien = aliens.sprites()[-1]
    # проверка наличия корабля игрока в месте появления нового флота пришельцев
    # если верхняя координата "y" корабля меньше нижней координаты "y" корабля в последнем ряду флота
    if ship.rect.top < last_alien.rect.bottom:
        # возвращение текущего корабля в начальное положение
        ship.center_ship()


def update_alien_bullets(ai_settings, screen, aliens, last_shot_time, alien_bullets, stats, explosions):
    """Обновление позиций и кол-ва пуль пришельцев"""
    # вызов функции для выбора стреляющих кораблей пришельцев каждые n-секунд из оставшейся группы
    last_shot_time, shooting_aliens = choice_shooting_aliens(stats, last_shot_time, aliens)

    # если определены стреляющие корабли пришельцев
    if shooting_aliens:
        # создание пуль и эффекта выстрела для пришельцев
        create_alien_bullets_and_small_explosions(ai_settings, screen, shooting_aliens, alien_bullets, explosions)

    # обновление позиций пуль пришельцев
    alien_bullets.update()
    # для каждой пули из группы пуль пришельцев
    for bullet in alien_bullets.copy():
        # если верхняя часть пули переходит через нижнюю часть экрана
        if bullet.rect.top > screen.get_rect().bottom:
            # уничтожение пули пришельца из группы
            alien_bullets.remove(bullet)

    # обновление окна
    pygame.display.flip()
    # возвращение времени последнего выстрела
    return last_shot_time


def choice_shooting_aliens(stats, last_shot_time, aliens):
    """Выбор стреляющих кораблей каждые n-секунд"""
    # фиксация текущего момента времени
    current_time = time()
    shooting_aliens=None
    # если разница между зафиксированным временем и временем последнего выстрела больше 3 сек
    if current_time - last_shot_time > 3:
        # время последнего выстрела равно фиксированному текущему времени
        last_shot_time = current_time
        # подсчет кол-ва одновременно стреляющих кораблей с учетом текущего уровня игры
        num_shooting_aliens = (stats.level // 2) + 1
        # уточнение кол-ва стреляющих кораблей с учётом их уничтожения игроком
        # (кол-во стреляющих кораблей не может быть больше оставшихся кораблей)
        num_shooting_aliens = min(num_shooting_aliens, len(aliens))
        # случайный выбор нужного кол-ва уникальных пришельцев из группы
        shooting_aliens = random.sample(aliens.sprites(), num_shooting_aliens)
    # возврат времени последнего выстрела и стреляющих кораблей
    return last_shot_time, shooting_aliens


def create_alien_bullets_and_small_explosions(ai_settings, screen, shooting_aliens, alien_bullets, explosions):
    """Функция для создания пуль пришельцев"""
    # для каждого стреляющего корабля из уникальной выборки
    for shooting_alien in shooting_aliens:
        # создание пули для с параметрами для пришельца
        new_alien_bullet = AlienBullet(ai_settings, screen, shooting_alien)
        # создание мини взрыва в месте возникновения пули
        small_explosion = SmallExplosion(ai_settings, screen, shooting_alien, ship_type=0, shot_location=None,
                                         for_alien=True)
        # добавление новой пули в группу пуль пришельцев
        alien_bullets.add(new_alien_bullet)
        # добавление мини взрыва в группу взрывов
        explosions.add(small_explosion)

    # проигрывание звука выстрела пришельца
    ai_settings.alien_shoot_sound.set_volume(0.8)
    ai_settings.alien_shoot_sound.play()


def update_explosions(ai_settings, explosions):
    """Функция для обновления координат, продолжительности и прозрачности эффекта взрыва"""
    # вычисление текущего времени
    current_time = pygame.time.get_ticks()
    # для каждого эффекта взрыва в группе взрывов
    for explosion in explosions.sprites():
        # если разница между текущем временем и временем создания эффекта взрыва больше или равна запланированной
        # продолжительности эффекта взрыва
        if current_time - explosion.creation_time >= ai_settings.explosion_duration:
            # удаление эффекта взрыва из группы и освобождение памяти
            explosion.kill()
            #explosions.remove(explosion)
        else:
            # подсчет переменной для задания эффекта прозрачности с течением времени
            alpha = ((pygame.time.get_ticks() - explosion.creation_time) / ai_settings.explosion_duration *
                     ai_settings.explosion_alpha)
            # задание прозрачности до окончания времени отображения эффекта
            explosion.image.set_alpha(255 - alpha)
    # обновление координат эффекта, зависящих от координат уничтожаемого объекта
    explosions.update()


def update_aliens(ai_settings, aliens):
    """Обновление позиций всех пришельцев во флоте,
     обработка достижения флотом левого/правого края экрана"""
    # проверка достижения флотом левого/правого края экрана
    check_fleet_edges(ai_settings, aliens)
    # обновление позиции флота
    aliens.update()


def check_fleet_edges(ai_settings, aliens):
    """Проверка достижения флотом края экрана"""
    # при достижении пришельцем из группы края экрана происходит смещение флота и изменение флага направления
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает флот вниз и меняет направление его движения"""
    for alien in aliens.sprites():
        # смещение вниз по Y на заданное расстояние для каждого пришельца в группе
        alien.rect.y += ai_settings.fleet_drop_speed
    # изменение флага направления
    ai_settings.fleet_direction *= -1


def update_ships(ai_settings, stats, screen, number_ship, ships, ship, aliens, bullets, alien_bullets, sb, explosions, air_bombs):
    """Обновление корабля на экране при столкновении с флотом пришельцев / достижения флотом нижнего края"""
    # обновление позиции корабля игрока
    ship.update()
    # проверка столкновения корабля игрока и пришельца
    collision_with_alien = check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, explosions, air_bombs, alien_bullets)
    # проверка достижения флотом пришельцев нижнего края экрана
    getting_bottom = check_aliens_bottom(ai_settings, stats, screen, ship, aliens, sb)
    # проверка попадания в корабль пули пришельца
    collision_with_alien_bullet = check_alien_bullet_ship_collision(ai_settings, screen, ship, alien_bullets, explosions)

    # если столкновение случилось или пришельцы достигли низа экрана и индекс корабля не последний
    if (collision_with_alien or getting_bottom or collision_with_alien_bullet) and number_ship != ai_settings.ship_limit-1:
        # сброс флагов движения корабля игрока в значение False
        reset_moving_flags_ship(ship)
        # задание паузы игры
        sleep(1.5)
        # вызов функции обработки уничтожения корабля
        ship_hit(ai_settings, stats, ship, bullets, sb, alien_bullets, explosions, air_bombs)
        # увеличение индекса корабля в группе
        number_ship += 1
    # если столкновение или достижение края экрана случилось и индекс корабля последний
    # или игра находится в неактивном состоянии
    elif ((collision_with_alien or getting_bottom or collision_with_alien_bullet) and number_ship == ai_settings.ship_limit-1) or not stats.game_active:
        if stats.game_active:
            # сброс флагов движения корабля игрока в значение False
            reset_moving_flags_ship(ship)
            # остановка фоновой музыки для боя
            pygame.mixer.music.stop()
            # проигрывание звука окончания игры
            ai_settings.game_over_sound.play()
            # задание паузы игры
            sleep(3)
            # вызов функции обработки уничтожения корабля
            ship_hit(ai_settings, stats, ship, bullets, sb, alien_bullets, explosions, air_bombs)
        # индекс списка кораблей игрока сбрасывается до нуля
        number_ship = 0

    # выбор корабля с нужным индексом из списка доступных
    ship = ships.sprites()[number_ship]
    # возврат обновлённого индекса и корабля группы
    return number_ship, ship


def check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, explosions, air_bombs, alien_bullets):
    """Проверка и реакция на столкновение корабля с флотом пришельцев"""
    collide_alien = pygame.sprite.spritecollideany(ship, aliens)
    # если существует пришелец из группы, столкнувшийся с кораблём игрока
    if collide_alien:
        # уничтожение пришельца из группы
        collide_alien.kill()
        # отображение эффекта взрыва корабля и пришельца при столкновении
        show_ship_alien_explosion(explosions, ai_settings, screen, collide_alien, ship)
        # обновление счета после столкновения кораблей
        update_score(ai_settings, stats, [collide_alien], sb)
        # для случая если после столкновения пришельцев не осталось
        if len(aliens) == 0:
            # старт нового уровня игры
            start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship, air_bombs, explosions, alien_bullets)
        return True


def show_ship_alien_explosion(explosions, ai_settings, screen, collide_alien, ship):
    """Функция для отображения эффекта взрыва корабля и пришельца при столкновении"""
    # создание эффекта взрыва на месте пришельца и корабля игрока
    create_explosion(explosions, ai_settings, screen, collide_alien, for_alien=True)
    create_explosion(explosions, ai_settings, screen, ship)
    # сохранение двух последних эффектов в переменной
    last_two_explosions = explosions.sprites()[-2:]
    # отображение двух последних эффектов взрыва
    for explosion in last_two_explosions:
        explosion.blitme()
        pygame.display.flip()


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, sb):
    """Проверка достижения флотом нижнего края экрана"""
    screen_rect = screen.get_rect()
    # при достижении кораблем флота нижнего края экрана вызывается функция обработки этого события
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # счёт игры сбрасывается до крайнего значения предыдущего уровня
            stats.score = stats.score_dict[stats.level - 1]
            # обновление счёта игры
            sb.prep_score()
            # очистка на экране группы пришельцев
            aliens.empty()
            # создание нового флота в начальной позиции на текущем уровне
            create_fleet(ai_settings, screen, ship, aliens, stats)
            return True


def check_alien_bullet_ship_collision(ai_settings, screen, ship, alien_bullets, explosions):
    """Функция проверки и обработки попадания пули пришельца по кораблю"""
    collide_alien_bullet = pygame.sprite.spritecollideany(ship, alien_bullets)

    if collide_alien_bullet:
        create_explosion(explosions, ai_settings, screen, ship)
        last_explosion = explosions.sprites()[-1]
        # отображение двух последних эффектов взрыва
        last_explosion.blitme()
        pygame.display.flip()
        # уничтожение пули пришельца
        collide_alien_bullet.kill()
        return True


def ship_hit(ai_settings, stats, ship, bullets, sb, alien_bullets, explosions, air_bombs):
    """Обработка столкновения корабля с флотом пришельцев / достижения флотом нижнего края экрана"""
    # для случая, если у игрока остались корабли (попытки игры)
    if stats.ship_left > 1:
        # уменьшение значения оставшихся кораблей (попыток игры)
        stats.ship_left -= 1
        #print('осталось кораблей ' + str(stats.ship_left))
        # обновление изображения с доступным кол-вом кораблей
        sb.prep_ships()

    # для случая если кораблей для игры (попыток) не осталось
    else:
        #print('Кораблей не осталось')
        # переход игры в неактивное состояние
        stats.game_active = False
        # изменение флага для разрешения проигрывания мелодии достижения рекорда игры
        stats.new_high_score_reached = False
        # сброс статистики
        stats.reset_stats()
        # отображение курсора мыши
        pygame.mouse.set_visible(True)
        # вызов функции для проигрывания фоновой музыки главного меню
        play_background_music(ai_settings.main_menu_music)
        # проигрывание музыки для главного меню
        pygame.mixer.music.play()

    # очистка пуль корабля и пришельцев
    bullets.empty()
    alien_bullets.empty()
    explosions.empty()
    air_bombs.empty()
    # задание расположения объекта корабля снизу в центре экрана
    ship.center_ship()


def get_number_stars_x(ai_settings, star_width):
    """Вычисление кол-ва звёзд в ряду"""
    # доступное пространство по Х: длина экрана - (коэфф.)*длину изобр. звезды
    available_space_x = ai_settings.screen_width - 2 * star_width
    # целое число звезд в ряду: пространство по X / (коэфф.*длину изобр. звезды)
    number_stars_x = int(available_space_x / (1 * star_width))
    return number_stars_x


def get_number_rows_stars(ai_settings, star_height):
    """Вычисление кол-ва рядов для звёзд"""
    # доступное пространство по Y: ширина экрана - (коэфф.)*ширину изобр. звезды
    available_space_y = ai_settings.screen_height - 2 * star_height
    # целое число рядов: пространство по Y / (коэфф.)*ширину изобр. звезды
    number_rows = int(available_space_y / (3 * star_height))
    return number_rows


def create_star(screen, stars, star_number, row_number):
    """Создание звезды в ряду"""
    star = Star(screen)
    # координата звезды по X со случайным отклонением
    star.x = randint(0, star.rect.width * 3) + randint(100, 250) * star_number
    star.rect.x = star.x
    # координата звезды по Y со случайным отклонением
    star.y = randint(0, star.rect.height * 4) + randint(130, 200) * row_number
    star.rect.y = star.y
    # добавление звезды в группу
    stars.add(star)


def create_stars(ai_settings, screen, stars):
    """Создание набора звёзд на экране"""
    # создание экземпляра звезды для вычисления его параметров высоты и ширины
    star = Star(screen)
    # вычисление кол-ва звезд в ряду по Х
    number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
    # вычисление рядов для звёзд по Y
    number_rows_stars = get_number_rows_stars(ai_settings, star.rect.height)
    # перебор рядов для звёзд
    for row_number in range(number_rows_stars):
        # создание ряда звёзд
        for star_number in range(number_stars_x):
            # создание звезды в ряду
            create_star(screen, stars, star_number, row_number)


def check_stars_edges(stars):
    """Проверка достижения звездой из группы края экрана"""
    # при достижении пришельцем из группы края экрана происходит смещение флота и изменение флага направления
    for star in stars.sprites():
        # при достижении верха звезды нижнего края экрана происходит перемещение звезды наверх
        if star.check_edges():
            star.rect.top -= star.rect.bottom
            star.y = star.rect.top
            break


def update_stars(stars):
    """Обновление позиции звезд"""
    check_stars_edges(stars)
    stars.update()
