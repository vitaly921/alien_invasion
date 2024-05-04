import sys
import pygame
from time import sleep
from random import randint
from bullet import Bullet
from alien import Alien
from star import Star
from ship import Ship
from explosion import Explosion


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, pause_button, about_it_button,
                 sb, pause, hint_for_pause_button, back_button, exit_button):
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
                                 hint_for_pause_button)
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
                         hint_for_pause_button):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_ESCAPE:
        # запись в файл обновленного значения рекорда
        with open('record.txt', 'w') as f:
            f.write(str(stats.high_score))
        # закрытие окна программы
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # вызов функции открытия огня по противнику
        fire_bullet(ai_settings, screen, ship, bullets, stats)
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
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
    # очистка групп пришельцев и пуль
    aliens.empty()
    bullets.empty()
    # создание нового флота пришельцев и перемещение корабля игрока в начальное положение
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


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
                  sb, hint_for_play_button, hint_for_about_it_button, back_button, exit_button, explosions):
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

    # отрисовка корабля игрока и группы пришельцев
    ship.blitme()
    aliens.draw(screen)

    explosions.draw(screen)
    # отображение рекорда
    sb.show_high_score()

    # действия во время неактивной игры
    if not stats.game_active:
        # задание расположения корабля по центру
        ship.center_ship()
        # очистка групп пришельцев, пуль, взрывов
        aliens.empty()
        bullets.empty()
        explosions.empty()
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


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions):
    """Обновляет количество и позиции пуль, обрабатывает коллизии пуль с пришельцами"""
    # обновление позиции пуль
    bullets.update()
    # отслеживание позиции для каждой пули из группы
    for bullet in bullets.copy():
        # удаление пули при достижении её нижнего края координаты верха экрана
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # функция обработки столкновения пуль с флотом пришельцев
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions)


def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, explosions):
    """Обработка столкновений пуль с пришельцами"""
    # удаление пуль и/или пришельцев во время столкновения с получением флага столкновения
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # при попадании пули по пришельцу увеличивается счёт игры, обновляется изображение с текстом счета,
    # появляется взрыв на месте пришельца
    if collisions:
        # для кораблей пришельцев, по которым попала пуля
        for aliens in collisions.values():
            # для каждого корабля из списка кораблей, по которым попала пуля
            for alien in aliens:
                # вызов функции для создания эффекта взрыва конкретного корабля
                create_explosion(explosions, ai_settings, screen, alien)
            # вызов функции для обновления счета игры и проверки рекорда
            update_score(ai_settings, stats, aliens, sb)

    # для случая отсутствия флота пришельцев после его уничтожения
    if len(aliens) == 0:
        # функция перехода на новый уровень игры
        start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship)


def start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship):
    """Функция перехода игры на новый уровень"""
    # сброс флагов движения корабля в состояние False
    reset_moving_flags_ship(ship)
    # задание временной паузы
    sleep(2.5)
    # очистка списка оставшихся пуль
    bullets.empty()
    # вызов функции увеличения скорости игровых объектов
    ai_settings.increase_speed()
    # увеличение уровня игры
    stats.level += 1
    # обновление изображения с уровнем игры
    sb.prep_level()
    # создание нового флота пришельцев
    create_fleet(ai_settings, screen, ship, aliens)


def create_explosion(explosions, ai_settings, screen, game_ship, alien=True):
    """Функция создания эффекта взрыва для корабля игрока/пришельца"""
    # создание экземпляра взрыва по координатам пришельца
    if alien:
        explosion = Explosion(ai_settings, screen, game_ship.x, game_ship.y)
    # создание экземпляра взрыва по координатам корабля игрока
    else:
        explosion = Explosion(ai_settings, screen, game_ship.centerx-25, game_ship.centery-25)
    # добавление экземпляра в группу
    explosions.add(explosion)


def update_score(ai_settings, stats, aliens, sb):
    """Функция для обновления счета игры и проверки рекорда"""
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


def fire_bullet(ai_settings, screen, ship, bullets, stats):
    """Позволяет совершить выстрел если максимум пуль еще не достигнут"""
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
        # создание новой пули и включение её в группу bullets
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


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


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создание пришельца в ряду"""
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


def create_fleet(ai_settings, screen, ship, aliens):
    """Создание флота пришельцев"""
    # создание экземпляра пришельца для вычисления его ширины и высоты
    alien = Alien(ai_settings, screen)
    # вычисление количества пришельцев в ряду
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # вычисление количества рядов пришельцев
    number_rows_aliens = get_number_rows_aliens(ai_settings, ship.rect.height, alien.rect.height)
    # перебор рядов пришельцев для создания флота
    for row_number in range(number_rows_aliens):
        # создание ряда пришельцев
        for alien_number in range(number_aliens_x):
            # создание пришельца в ряду
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


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, collision=True):
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
            create_fleet(ai_settings, screen, ship, aliens)

        # очистка группы пуль
        bullets.empty()
        #print(ship.x)
        # задание паузы
        #sleep(1.5)

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
        # задание паузы
        #sleep(1.5)
    # задание расположения объекта корабля снизу в центре экрана
    ship.center_ship()


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
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
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, collisions)
            return True


def check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, explosions):
    """Проверка и реакция на столкновение корабля с флотом пришельцев"""
    # выявление столкнувшегося с кораблём игрока пришельца из группы
    collide_alien = pygame.sprite.spritecollideany(ship, aliens)
    # если существует пришелец из группы, столкнувшийся с кораблём игрока
    if collide_alien:
        # сброс флагов движения корабля игрока в значение False
        reset_moving_flags_ship(ship)
        # уничтожение пришельца из группы
        collide_alien.kill()
        # отображение эффекта взрыва корабля и пришельца при столкновении
        show_ship_alien_explosion(explosions, ai_settings, screen, collide_alien, ship)
        # задание паузы игры
        sleep(1.5)
        # вызов функции обработки уничтожения корабля
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
        return True


def show_ship_alien_explosion(explosions, ai_settings, screen, collide_alien, ship):
    """Функция для отображения эффекта взрыва корабля и пришельца при столкновении"""
    # создание эффекта взрыва на месте пришельца и корабля игрока
    create_explosion(explosions, ai_settings, screen, collide_alien)
    create_explosion(explosions, ai_settings, screen, ship, alien=False)
    # сохранение двух последних эффектов в переменной
    last_two_explosions = explosions.sprites()[-2:]
    # отображение двух последних эффектов взрыва
    for explosion in last_two_explosions:
        explosion.blitme()
    # обновление экрана
    pygame.display.flip()


def update_ships(ai_settings, stats, screen, number_ship, ships, ship, aliens, bullets, sb, explosions):
    """Обновление корабля на экране при столкновении с флотом пришельцев / достижения флотом нижнего края"""
    # проверка столкновения корабля игрока и пришельца
    collision = check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb, explosions)

    # проверка достижения флотом пришельцев нижнего края экрана
    getting_bottom = check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # если столкновение случилось или пришельцы достигли низа экрана и индекс корабля не последний
    if (collision or getting_bottom) and number_ship != ai_settings.ship_limit-1:
        # увеличение индекса корабля в группе
        number_ship += 1

    # если столкновение или достижение края экрана случилось и индекс корабля последний
    # или игра находится в неактивном состоянии
    elif ((collision or getting_bottom) and number_ship == ai_settings.ship_limit-1) or not stats.game_active:
        # индекс списка кораблей игрока сбрасывается до нуля
        number_ship = 0
    # выбор корабля с нужным индексом из списка доступных
    ship = ships.sprites()[number_ship]
    ship.update()
    #print(ship.centerx)
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
