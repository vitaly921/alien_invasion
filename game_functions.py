import sys
import pygame
from time import sleep
from random import randint
from bullet import Bullet
from alien import Alien
from star import Star
from ship import Ship


def check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb, pause, pause_button,
                         hint_for_pause_button, ships, number_ship):
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
    elif event.key == pygame.K_RETURN and not stats.game_active:
        # вызов функции для начала игры
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)
    # обработка события нажатия клавиши "p" во время активной игры
    elif event.key == pygame.K_p and stats.game_active:
        # вызов функции для задания паузы игры
        return_menu = False
        return_menu = pause_game(ship, stats, pause, pause_button, hint_for_pause_button, ships)
        if return_menu:
            update_ships(ai_settings, stats, screen, number_ship, ships, ship, aliens, bullets, sb, True)


def reset_moving_flags_ship(ship):
    """Сброс флагов движения корабля"""
    ship.moving_left = False
    ship.moving_right = False
    ship.moving_up = False
    ship.moving_down = False


def pause_game(ship, stats, pause, pause_button, hint_for_pause_button, ships):
    """Обработка паузы в игре"""
    # флаг паузы переходит в значение True
    pause = not pause
    # сброс флагов движения корабля
    reset_moving_flags_ship(ship)
    # отображение курсора мыши
    pygame.mouse.set_visible(True)
    hint_for_pause_button.blitme()
    # основной цикл паузы
    while pause:
        # переход игры в неактивное состояние
        stats.game_active = False
        # отрисовка кнопки паузы
        pause_button.draw_button()
        #hint_for_pause_button.blitme()
        # отслеживание определённых событий во время паузы
        for event in pygame.event.get():
            # обработка события выхода из игры
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # обработка события нажатия клавиш
            if event.type == pygame.KEYDOWN:
                # случай нажатия клавиш "p" или "space"
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # флаг паузы переходит в состояние false, что приводит к выходу из цикла и окончанию паузы
                    pause = False
                    # скрытие курсора мыши
                    pygame.mouse.set_visible(False)
                    # переход игры в активное состояние
                    stats.game_active = True
                # случай нажатия клавиши "Esc"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_BACKSPACE:
                    pause = False
                    stats.game_active = True
                    ship.center_ship()
                    ship.update()
                    stats.reset_stats()
                    return True

            # обработка события нажатия любой кнопки мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                    # обработка события движения курсора мыши
            # обработка события движения мыши
            elif event.type == pygame.MOUSEMOTION:
                # случай нахождения курсора мыши в пределах области кнопки
                if pause_button.rect.collidepoint(event.pos):
                    # изменение цвета фона кнопки
                    pause_button.button_color = (210, 55, 75)
                    pause_button.prep_msg(pause_button.msg)
                else:
                    pause_button.button_color = (30, 120, 20)
                    pause_button.prep_msg(pause_button.msg)

        # обновление экрана для отрисовки кнопки паузы
        pygame.display.flip()

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


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, pause_button, about_it_button,
                 sb, pause, hint_for_pause_button, hint_for_about_it_button, back_button, exit_button, ships, number_ship):
    """Обработка событий в игре"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # запись в файл обновленного значения рекорда
            with open('record.txt', 'w') as f:
                f.write(str(stats.high_score))
            sys.exit()
        # обработка события нажатия клавиши
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb, pause, pause_button,
                                 hint_for_pause_button, ships, number_ship)
        # обработка события отпускания клавиши
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        # обработка события нажатия любой клавиши мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # получение координат точки нажатия клавиши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # проверка нажатия клавиши в пределах кнопки и запуск игры заново в активном состоянии
            check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, sb)
            check_about_it_button(ai_settings, screen, mouse_x, mouse_y, about_it_button, hint_for_about_it_button, aliens, stats, back_button)
            check_back_button(ai_settings, screen, mouse_x, mouse_y, about_it_button, hint_for_about_it_button, aliens, stats, back_button)
            check_exit_button(ai_settings, screen, mouse_x, mouse_y, about_it_button, hint_for_about_it_button, aliens, stats, exit_button)
        # обработка события движения курсора мыши
        elif event.type == pygame.MOUSEMOTION:
            # случай нахождения курсора мыши в пределах области кнопки Play
            if play_button.rect.collidepoint(event.pos):
                # изменение цвета фона кнопок
                play_button.button_color = (210, 55, 75)
                play_button.prep_msg(play_button.msg)
            # случай нахождения курсора мыши в пределах области кнопки About It
            elif about_it_button.rect.collidepoint(event.pos):
                about_it_button.button_color = (210, 55, 75)
                about_it_button.prep_msg(about_it_button.msg)
            # для случая отсутствия курсора мыши в пределах областей кнопок
            else:
                play_button.button_color = (30, 120, 20)
                play_button.prep_msg(play_button.msg)
                about_it_button.button_color = (30, 120, 20)
                about_it_button.prep_msg(about_it_button.msg)

def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):
    """Функция настройки игровых элементов при старте игры"""
    # сброс скоростей игровых элементов
    ai_settings.initialize_dynamic_settings()
    reset_moving_flags_ship(ship)
    # скрытие курсора мыши
    pygame.mouse.set_visible(False)
    # вызов функции для отрисовки статистических данных (счет, рекорд, уровень, оставшиеся корабли) в виде изображений
    sb.prep_images()
    # переход игры в активный режим
    stats.game_active = True
    # очистка группы пришельцев и пуль
    aliens.empty()
    bullets.empty()
    # создание нового флота пришельцев и перемещение корабля игрока в начальное положение
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, sb):
    """Проверка нажатия мышью кнопки и новый запуск игры в активном состоянии"""
    # флаг нажатия кнопки мыши в пределах кнопки Play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # запуск новой игры в активном состоянии при нажатии мыши на кнопку Play и текущем неактивном состоянии игры
    if button_clicked and not stats.game_active and not stats.press_about_it_button:
        # вызов функции настройки игровых элементов при старте
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def check_about_it_button(ai_settings, screen, mouse_x, mouse_y, about_it_button, hint_for_about_it_button, aliens, stats, back_button):
    """"""
    button_clicked = about_it_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        stats.press_about_it_button = True


def check_back_button(ai_settings, screen, mouse_x, mouse_y, about_it_button, hint_for_about_it_button, aliens, stats, back_button):
    """"""
    button_clicked = back_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        stats.press_about_it_button = False


def check_exit_button(ai_settings, screen, mouse_x, mouse_y, about_it_button, hint_for_about_it_button, aliens, stats, exit_button):
    """"""
    button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        pygame.quit()
        quit()


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
                  sb, hint_for_play_button, hint_for_about_it_button, back_button, exit_button):
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

    # отображение рекорда
    sb.show_high_score()

    # отрисовка кнопки Play, надписи названия игры. Очистка экрана от пришельцев и пуль
    if not stats.game_active:
        ship.center_ship()
        aliens.empty()
        bullets.empty()
        if stats.press_about_it_button:
            hint_for_about_it_button.blitme()
            back_button.draw_button()
        else:
            game_title.blitme()
            play_button.draw_button()
            exit_button.draw_button()
            about_it_button.draw_button()
            hint_for_play_button.blitme()
    else:
        # отображение текущего счёта, уровня и доступных кораблей для игры
        sb.show_score()


    # обновление окна
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Обновляет количество и позиции пуль, обрабатывает коллизии пуль с пришельцами"""
    bullets.update()
    for bullet in bullets.copy():
        # удаление пули при достижении её нижнего края координаты верха экрана
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # функция обработки взаимодействия пуль с флотом пришельцев
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb)


def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Обработка столкновений пуль с пришельцами"""
    # удаление пуль и пришельцев во время столкновения
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    # при попадании пули по пришельцу увеличивается счёт игры и обновляется изображение с текстом счета
    if collisions:
        # для кораблей пришельцев, по которым попала пуля
        for aliens in collisions.values():
            # увеличение значения счёта, который учитывает все попадания одного снаряда
            stats.score += ai_settings.alien_points * len(aliens)
            # обновление словаря со значением счёта игры на текущем уровне
            stats.score_dict[stats.level] = stats.score
            #print(stats.score_dict)
            #score_in_level = stats.score - stats.score_dict[stats.level - 1]
            #print('Получено очков на уровне: ' + str(score_in_level))
            #print('Level: ' +str(stats.level))
        # формирование изображения с текстом обновленного счёта
        sb.prep_score()
        # проверка достижения рекордного счёта
        check_high_score(stats, sb)

    # функция перехода на новый уровень при отсутствии пришельцев
    start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship)


def start_new_level(aliens, bullets, ai_settings, stats, sb, screen, ship):
    """Функция проверки и перехода игры на новый уровень"""
    # для случая отсутствия флота пришельцев после его уничтожения
    if len(aliens) == 0:
        # сброс флагов движения корабля в состояние False
        reset_moving_flags_ship(ship)
        # уничтожение оставшихся пуль, увеличение скорости и уровня игры, создание нового флота пришельцев
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
        # уменьшение значения оставшихся кораблей
        stats.ship_left -= 1
        print('осталось кораблей ' + str(stats.ship_left))
        # обновление изображения с доступным кол-вом кораблей
        sb.prep_ships()

        # для случая если столкновения корабля и пришельцев не происходит
        if not collision:
            # счёт игры сбрасывается до крайнего значения предыдущего уровня
            stats.score = stats.score_dict[stats.level - 1]
            # обновление счёта игры
            sb.prep_score()
            # очистка на экране группы пришельцев
            aliens.empty()
            # создание нового флота в начальной позиции
            create_fleet(ai_settings, screen, ship, aliens)

        # очистка группы пуль
        bullets.empty()
        # задание паузы
        sleep(1.5)

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
        sleep(1.5)

    # задание расположения объекта корабля снизу в центре экрана
    ship.center_ship()


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Проверка достижения флотом нижнего края экрана"""
    screen_rect = screen.get_rect()
    # при достижении кораблем флота нижнего края экрана вызывается функция обработки этого события
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # задается флаг столкновения корабля с пришельцами в состоянии False
            collisions = False
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb, collisions)
            return True


def check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Проверка и реакция на столкновение корабля с флотом пришельцев"""
    if pygame.sprite.spritecollideany(ship, aliens):
        # сброс флагов движения корабля в значение False
        reset_moving_flags_ship(ship)
        # переход игры в начальное состояние
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
        return True


def update_ships(ai_settings, stats, screen, number_ship, ships, ship, aliens, bullets, sb, return_menu = False):
    """Обновление корабля на экране при столкновении с флотом пришельцев"""
    # проверка столкновения корабля игрока и пришельца
    collision = check_ship_aliens_collision(ai_settings, stats, screen, ship, aliens, bullets, sb)
    print(return_menu)
    # проверка достижения флотом пришельцев нижнего края экрана
    getting_bottom = check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # если столкновение случилось или пришельцы достигли низа экрана и индекс корабля не последний
    if (collision or getting_bottom) and number_ship != ai_settings.ship_limit-1:
        print('stats.ship_left: ' + str(stats.ship_left))
        # увеличение индекса корабля в группе
        number_ship += 1
    # если столкновение случилось и индекс корабля последний
    elif (collision or getting_bottom) and number_ship == ai_settings.ship_limit-1:
        # индекс сбрасывается до нуля
        number_ship = 0
    if return_menu:
        number_ship = 0
        stats.game_active = False
    # выбор корабля с нужным индексом
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
