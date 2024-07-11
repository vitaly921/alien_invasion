import random
import sys
import pygame
from time import sleep, time
from random import randint
from bullet import Bullet, ShipBullet, AlienBullet
from air_bomb import AirBomb
from alien import Alien, BoostedAlien
from star import Star
from ship import Ship
from explosion import Explosion, SmallExplosion
from pygame.sprite import Group


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
            check_mouse_motion_events(ai_settings, event, play_button, about_it_button, exit_button, back_button)


def check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb, pause, pause_button,
                         hint_for_pause_button, air_bombs, explosions, ship_type):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_ESCAPE:
        # запись в файл обновленного значения рекорда
        with open('record.txt', 'w') as f:
            f.write(str(stats.high_score))
        # закрытие окна программы
        sys.exit()
    elif event.key == pygame.K_RIGHT and stats.game_active:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT and stats.game_active:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # вызов функции открытия огня по противнику
        fire_bullet(ai_settings, screen, ship, bullets, stats, explosions, ship_type)
    elif event.key == pygame.K_RSHIFT:
        # вызов функции для сброса авиабомб
        drop_air_bomb(ai_settings, screen, ship, air_bombs, stats)
    elif event.key == pygame.K_UP and stats.game_active:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN and stats.game_active:
        ship.moving_down = True
        # обработка нажатия клавиши "Enter" во время неактивной игры
    elif event.key == pygame.K_RETURN and not stats.game_active:
        # вызов функции для начала игры
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)
    # обработка нажатия клавиши "p" во время активной игры
    elif event.key == pygame.K_p and stats.game_active:
        # вызов функции для задания паузы игры
        pause_game(ai_settings, ship, stats, pause, pause_button, hint_for_pause_button)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш"""
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
    check_about_it_button(mouse_x, mouse_y, about_it_button, stats)
    check_back_button(mouse_x, mouse_y, stats, back_button)
    check_exit_button(mouse_x, mouse_y, stats, exit_button)


def check_mouse_motion_events(ai_settings, event, play_button, about_it_button, exit_button, back_button):
    """Функция для обработки события движения мыши"""
    # изменение цвета кнопок Play, About It, Exit, Back
    change_color_button(ai_settings, event, play_button)
    change_color_button(ai_settings, event, about_it_button)
    change_color_button(ai_settings, event, exit_button)
    change_color_button(ai_settings, event, back_button)


def change_color_button(ai_settings, event, button):
    """Изменение цвета кнопки при наведении на неё курсором мыши"""
    # при нахождении курсора мыши в пределах кнопки
    if button.rect.collidepoint(event.pos):
        # изменение цвета фона кнопки
        button.button_color = ai_settings.active_button_color
        button.prep_msg(button.msg)
    # при выходе курсора за пределы кнопки
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
        # вызов функции настройки игровых элементов при старте
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def check_about_it_button(mouse_x, mouse_y, about_it_button, stats):
    """Проверка нажатия мышью кнопки About It"""
    # флаг нажатия кнопки мыши в пределах кнопки About It
    button_clicked = about_it_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая если нажатие происходит в пределах области кнопки
    if button_clicked:
        # переход игры в состояние, в котором отображается описание игры
        stats.press_about_it_button = True


def check_back_button(mouse_x, mouse_y, stats, back_button):
    """Проверка нажатия мышью кнопки Back"""
    # флаг нажатия кнопки мыши в пределах кнопки Back
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая если нажатие происходит в пределах области кнопки
    if button_clicked:
        # переход игры в главное меню
        stats.press_about_it_button = False


def check_exit_button(mouse_x, mouse_y, stats, exit_button):
    """Проверка нажатия мышью кнопки Exit"""
    # флаг нажатия кнопки мыши в пределах кнопки Exit
    button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая если нажатие происходит в пределах области кнопки и в главном меню игры
    if button_clicked and not stats.press_about_it_button:
        # закрытие окна игры
        pygame.quit()
        quit()


def reset_moving_flags_ship(ship):
    """Сброс флагов движения корабля"""
    ship.moving_left = False
    ship.moving_right = False
    ship.moving_up = False
    ship.moving_down = False


def pause_game(ai_settings, ship, stats, pause, pause_button, hint_for_pause_button):
    """Обработка паузы в игре"""
    # флаг паузы переходит в значение True
    pause = not pause
    # сброс флагов движения корабля
    reset_moving_flags_ship(ship)
    # отображение курсора мыши
    pygame.mouse.set_visible(True)
    # отображение подсказки во время паузы
    hint_for_pause_button.blitme()
    # основной цикл паузы
    while pause:
        # вызов функции обработки событий во время паузы с проверкой состояния флага паузы
        pause = check_events_for_pause(ai_settings, stats, pause_button, pause)
        # обновление экрана для отрисовки кнопки паузы
        pygame.display.flip()


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
            pause = check_keydown_events_for_pause(event, stats, pause)
        # обработка события нажатия любой кнопки мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # вызов функции обработки событий нажатия кнопок мыши в режиме паузы с возвратом состояния паузы
            pause = check_mouse_button_down_for_pause(stats, pause, pause_button)
        # обработка события движения мыши
        elif event.type == pygame.MOUSEMOTION:
            # вызов функции для изменения цвета кнопки
            change_color_button(ai_settings, event, pause_button)
    return pause


def check_keydown_events_for_pause(event, stats, pause):
    """Функция обработки событий нажатия клавиш в режиме паузы с возвратом состояния паузы"""
    # обработка нажатия клавиш "Enter" или "Space"
    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
        # флаг паузы переходит в состояние false, что приводит к выходу из цикла и окончанию паузы
        pause = False
        # скрытие курсора мыши
        pygame.mouse.set_visible(False)
        # переход игры в активное состояние
        stats.game_active = True
    # случай нажатия клавиши "Esc"
    elif event.key == pygame.K_ESCAPE:
        # выход из игры
        pygame.quit()
        quit()
    # обработка нажатия клавиши "Backspace"
    elif event.key == pygame.K_BACKSPACE:
        # флаг паузы переход в состояние False
        pause = False
        # сброс статистики
        stats.reset_stats()
    return pause


def check_mouse_button_down_for_pause(stats, pause, pause_button):
    """Функция обработки событий нажатия кнопок мыши в режиме паузы с возвратом состояния паузы"""
    # получение координат точки нажатия клавиши
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # получение флага нажатия кнопки мыши в пределах области кнопки паузы
    button_clicked = pause_button.rect.collidepoint(mouse_x, mouse_y)
    # для случая нажатия кнопки мыши в пределах области кнопки паузы
    if button_clicked:
        # флаг паузы переходит в состояние false, что приводит к выходу из цикла и окончанию паузы
        pause = False
        # скрытие курсора мыши
        pygame.mouse.set_visible(False)
        # переход игры в активное состояние
        stats.game_active = True
    return pause


def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):
    """Функция настройки игровых элементов при старте игры"""
    # сброс скоростей игровых элементов
    ai_settings.initialize_dynamic_settings()
    # сброс флагов движения корабля
    reset_moving_flags_ship(ship)
    # скрытие курсора мыши
    pygame.mouse.set_visible(False)
    # вызов функции для отрисовки статистических данных (счет, рекорд, уровень, оставшиеся корабли) в виде изображений
    sb.prep_images()
    # переход игры в активный режим
    stats.game_active = True
    # создание нового флота пришельцев и перемещение корабля игрока в начальное положение
    create_fleet(ai_settings, screen, ship, aliens, stats)
    #ship.center_ship()


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


def update_screen(ai_settings, screen, ship, aliens, bullets, stars, stats, play_button, about_it_button, game_title,
                  sb, hint_for_play_button, hint_for_about_it_button, back_button, exit_button, explosions, air_bombs, alien_bullets):
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

    # поочередная отрисовка пуль
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # поочередная отрисовка авиабомб
    for air_bomb in air_bombs.sprites():
        air_bomb.draw_air_bomb()

    for bullet in alien_bullets.sprites():
        bullet.draw_bullet()

    # отрисовка корабля игрока и группы пришельцев
    ship.blitme()
    aliens.draw(screen)

    # отрисовка взрывов
    explosions.draw(screen)
    # отображение рекорда
    sb.show_high_score()

    # действия во время неактивной игры
    if not stats.game_active:
        # задание расположения корабля по центру
        #ship.center_ship()
        # очистка групп пришельцев, пуль, взрывов
        aliens.empty()
        #bullets.empty()
        #air_bombs.empty()
        #explosions.empty()
        # действия во время неактивной игры при переходе в меню описания
        if stats.press_about_it_button:
            # текст описания игры
            hint_for_about_it_button.blitme()
            # отображения кнопки "Back" для возврата в главное меню
            back_button.draw_button()
        # действия во время неактивной игры при отсутствии перехода в меню описания
        else:
            # отрисовка заглавия игры
            game_title.blitme()
            # отрисовка кнопок Play, About It, Exit
            play_button.draw_button()
            exit_button.draw_button()
            about_it_button.draw_button()
            # отрисовка подсказки для начала игры
            hint_for_play_button.blitme()
    # действия во время активной игры
    else:
        # отображение текущего счёта, уровня и доступных кораблей для игры
        sb.show_score()

    # обновление окна
    pygame.display.flip()


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
    check_ship_projectiles_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions, air_bombs, alien_bullets)


def check_ship_projectiles_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions, air_bombs, alien_bullets):
    """Обработка столкновений пуль/авиабомб с пришельцами"""
    boosted_bullets = Group()
    for bullet in bullets.copy():
        if bullet.boosted:
            bullet.add(boosted_bullets)
    boosted_bullets_aliens_collisions = pygame.sprite.groupcollide(boosted_bullets, aliens, False, True)
    # обработка столкновений пуль с пришельцами: при столкновении удаляется и пуля и пришелец
    bullets_aliens_collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    # обработка столкновений авиабомб с пришельцами: при столкновении удаляются только пришельцы
    air_bombs_aliens_collisions = pygame.sprite.groupcollide(air_bombs, aliens, False, True)
    # обработка столкновения пули игрока с пулей пришельца: взаимное уничтожение
    bullets_collision = pygame.sprite.groupcollide(bullets, alien_bullets, True, True)

    # для случая столкновения пуль с пришельцами
    if bullets_aliens_collisions:
        # дальнейшая обработка
        handle_collision(bullets_aliens_collisions, ai_settings, screen, explosions, stats, sb, aliens)
    # для случая столкновения авиабомб с пришельцами
    elif air_bombs_aliens_collisions:
        # дальнейшая обработка
        handle_collision(air_bombs_aliens_collisions, ai_settings, screen, explosions, stats, sb, aliens)
    # для случая столкновения снарядов корабля и пришельца друг с другом
    elif bullets_collision:
        # обновление счёта игры
        update_score(ai_settings, stats, aliens, sb, for_bullets=True)
    elif boosted_bullets_aliens_collisions:
        # дальнейшая обработка
        handle_collision(boosted_bullets_aliens_collisions, ai_settings, screen, explosions, stats, sb, aliens)

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
            # для случая принадлежности пришельца к базовому классу
            else:
                # удаление пришельца из группы
                alien.kill()
            # вызов функции для создания эффекта взрыва конкретного корабля
            create_explosion(explosions, ai_settings, screen, alien, for_alien=True)
        # вызов функции для обновления счета игры и проверки рекорда
        update_score(ai_settings, stats, aliens, sb)


def update_alien_bullets(ai_settings, screen, aliens, last_shot_time, alien_bullets, stats, explosions):
    """Обновление позиций и кол-ва пуль пришельцев"""
    # фиксация текущего момента времени
    current_time = time()
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

        # для каждого стреляющего корабля из уникальной выборки
        for shooting_alien in shooting_aliens:
            # создание пули для с параметрами для пришельца
            new_alien_bullet = AlienBullet(ai_settings, screen, shooting_alien)
            small_explosion = SmallExplosion(ai_settings, screen, shooting_alien, ship_type=0, for_alien=True)
            # добавление новой пули в группу пуль пришельцев
            alien_bullets.add(new_alien_bullet)
            explosions.add(small_explosion)

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


def check_alien_bullet_ship_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs):
    """Функция проверки и обработки попадания пули пришельца по кораблю"""
    collide_alien_bullet = pygame.sprite.spritecollideany(ship, alien_bullets)

    if collide_alien_bullet:
        # сброс флагов движения корабля игрока в значение False
        reset_moving_flags_ship(ship)
        create_explosion(explosions, ai_settings, screen, ship)
        last_explosion = explosions.sprites()[-1]
        # отображение двух последних эффектов взрыва
        last_explosion.blitme()
        pygame.display.flip()
        #
        collide_alien_bullet.kill()
        # задание паузы игры
        sleep(1.5)
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs)
        return True


def start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship, air_bombs, explosions, alien_bullets):
    """Функция перехода игры на новый уровень"""
    # сброс флагов движения корабля в состояние False
    reset_moving_flags_ship(ship)
    # задание временной паузы
    sleep(1.5)
    # очистка списка оставшихся пуль и авиабомб
    aliens.empty()
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
    # сохранение последнего пришельца в переменной
    last_alien = aliens.sprites()[-1]
    # проверка наличия корабля игрока в месте появления нового флота пришельцев
    # если верхняя координата "y" корабля меньше нижней координаты "y" корабля в последнем ряду флота
    if ship.rect.top < last_alien.rect.bottom:
        # возвращение текущего корабля в начальное положение
        ship.center_ship()


def create_explosion(explosions, ai_settings, screen, game_ship, for_alien=False):
    """Функция создания эффекта взрыва для корабля игрока/пришельца"""
    # создание экземпляра взрыва по координатам пришельца
    if for_alien:
        explosion = Explosion(ai_settings, screen, game_ship, for_alien=True)
    # создание экземпляра взрыва по координатам корабля игрока
    else:
        explosion = Explosion(ai_settings, screen, game_ship)
    # добавление экземпляра в группу
    explosions.add(explosion)


def update_score(ai_settings, stats, aliens, sb, for_bullets=False):
    """Функция для обновления счета игры и проверки рекорда"""
    # для случая если флаг for_bullets активен
    if for_bullets:
        # фиксированное увеличение счета игры
        stats.score += ai_settings.bullet_score
    else:
        # увеличение значения счёта, который учитывает все попадания одного снаряда
        stats.score += ai_settings.alien_points * len(aliens)
    # обновление словаря со значением счёта игры на текущем уровне
    stats.score_dict[stats.level] = stats.score
    # формирование изображения с текстом обновленного счёта
    sb.prep_score()
    # проверка достижения рекордного счёта
    check_high_score(stats, sb)


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


def fire_bullet(ai_settings, screen, ship, bullets, stats, explosions, ship_type):
    """Позволяет совершить выстрел если максимум пуль еще не достигнут"""
    #print('Огонь ведет ' + str(ship_type+1) + ' корабль')
    if ship_type == 0:
        if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
            # создание новой пули и включение её в группу bullets
            new_bullet = ShipBullet(ai_settings, screen, ship, ship_type, ship.rect.centerx, ship.rect.top)
            new_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type)
            explosions.add(new_small_explosions)
            bullets.add(new_bullet)
    elif ship_type == 1:
        left_bullet = ShipBullet(ai_settings, screen, ship, ship_type, ship.rect.left+22, ship.rect.top+20)
        left_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type, left=True)
        explosions.add(left_small_explosions)
        right_bullet = ShipBullet(ai_settings, screen, ship, ship_type, ship.rect.right-22, ship.rect.top+20)
        right_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type, right=True)
        explosions.add(right_small_explosions)
        bullets.add(left_bullet)
        bullets.add(right_bullet)
    elif ship_type == 2:
        left_bullet = ShipBullet(ai_settings, screen, ship, ship_type, ship.rect.left + 2, ship.rect.top + 20)
        left_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type, left=True)
        explosions.add(left_small_explosions)
        middle_bullet = ShipBullet(ai_settings, screen, ship, ship_type, ship.rect.centerx, ship.rect.top, boosted=True)
        new_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type)
        explosions.add(new_small_explosions)
        right_bullet = ShipBullet(ai_settings, screen, ship, ship_type, ship.rect.right - 2, ship.rect.top + 20)
        right_small_explosions = SmallExplosion(ai_settings, screen, ship, ship_type, right=True)
        explosions.add(right_small_explosions)
        bullets.add(left_bullet)
        bullets.add(middle_bullet)
        bullets.add(right_bullet)


def drop_air_bomb(ai_settings, screen, ship, air_bombs, stats):
    """Функция для создания авиабомб"""
    # если во время игры бомба на экране отсутствует
    if len(air_bombs) < ai_settings.air_bombs_allowed and stats.game_active:
        # создание экземпляра новой бомбы
        new_air_bomb = AirBomb(ai_settings, screen, ship)
        # добавление бомбы в список
        air_bombs.add(new_air_bomb)


def check_high_score(stats, sb):
    """Проверка достижения нового рекорда"""
    if stats.score > int(stats.high_score):
        # обновление рекорда
        stats.high_score = stats.score
        # формирование и вывод изображения с рекордом
        sb.prep_high_score()


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
    print(index_boosted_aliens)

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


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs, collision=True):
    """Обработка столкновения корабля с флотом пришельцев / достижения флотом нижнего края экрана"""
    # для случая, если у игрока остались корабли (попытки игры)
    if stats.ship_left > 1:
        # уменьшение значения оставшихся кораблей (попыток игры)
        stats.ship_left -= 1
        print('осталось кораблей ' + str(stats.ship_left))
        # обновление изображения с доступным кол-вом кораблей
        sb.prep_ships()
        # для случая достижения пришельцами нижнего края экрана
        if not collision:
            # счёт игры сбрасывается до крайнего значения предыдущего уровня
            stats.score = stats.score_dict[stats.level - 1]
            # обновление счёта игры
            sb.prep_score()
            # очистка на экране группы пришельцев
            aliens.empty()
            # создание нового флота в начальной позиции на текущем уровне
            create_fleet(ai_settings, screen, ship, aliens, stats)

    # для случая если кораблей для игры (попыток) не осталось
    else:
        print('Кораблей не осталось')
        # переход игры в неактивное состояние
        stats.game_active = False
        # приведение флагов движения корабля к значению False
        reset_moving_flags_ship(ship)
        # сброс статистики
        stats.reset_stats()
        # отображение курсора мыши
        pygame.mouse.set_visible(True)
    # очистка пуль корабля и пришельцев
    bullets.empty()
    alien_bullets.empty()
    explosions.empty()
    air_bombs.empty()
    # задание расположения объекта корабля снизу в центре экрана
    ship.center_ship()


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs):
    """Проверка достижения флотом нижнего края экрана"""
    screen_rect = screen.get_rect()
    # при достижении кораблем флота нижнего края экрана вызывается функция обработки этого события
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # задается флаг столкновения корабля с пришельцами в состоянии False (столкновение отсутствует)
            collisions = False
            # задание паузы игры
            sleep(1.5)
            # вызов функции обработки уничтожения корабля
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs, collisions)
            return True


def check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, explosions, air_bombs, alien_bullets):
    """Проверка и реакция на столкновение корабля с флотом пришельцев"""
    collide_alien = pygame.sprite.spritecollideany(ship, aliens)
    # если существует пришелец из группы, столкнувшийся с кораблём игрока
    if collide_alien:
        # сброс флагов движения корабля игрока в значение False
        reset_moving_flags_ship(ship)
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
        # для случая если после столкновения остались пришельцы
        else:
            # задание паузы игры
            sleep(1.5)
        # вызов функции обработки уничтожения корабля
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs)
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


def update_ships(ai_settings, stats, screen, number_ship, ships, ship, aliens, bullets, alien_bullets, sb, explosions, air_bombs):
    """Обновление корабля на экране при столкновении с флотом пришельцев / достижения флотом нижнего края"""
    # обновление позиции корабля игрока
    ship.update()
    # проверка столкновения корабля игрока и пришельца
    collision_with_alien = check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, explosions, air_bombs, alien_bullets)
    # проверка достижения флотом пришельцев нижнего края экрана
    getting_bottom = check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs)
    # проверка попадания в корабль пули пришельца
    collision_with_alien_bullet = check_alien_bullet_ship_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, alien_bullets, explosions, air_bombs)

    # если столкновение случилось или пришельцы достигли низа экрана и индекс корабля не последний
    if (collision_with_alien or getting_bottom or collision_with_alien_bullet) and number_ship != ai_settings.ship_limit-1:
        # увеличение индекса корабля в группе
        number_ship += 1
    # если столкновение или достижение края экрана случилось и индекс корабля последний
    # или игра находится в неактивном состоянии
    elif ((collision_with_alien or getting_bottom or collision_with_alien_bullet) and number_ship == ai_settings.ship_limit-1) or not stats.game_active:
        # индекс списка кораблей игрока сбрасывается до нуля
        number_ship = 0

    # выбор корабля с нужным индексом из списка доступных
    ship = ships.sprites()[number_ship]
    # возврат обновлённого индекса и корабля группы
    return number_ship, ship


def update_aliens(ai_settings, aliens):
    """Обновление позиций всех пришельцев во флоте,
     обработка достижения флотом левого/правого края экрана"""
    # проверка достижения флотом левого/правого края экрана
    check_fleet_edges(ai_settings, aliens)
    # обновление позиции флота
    aliens.update()


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
