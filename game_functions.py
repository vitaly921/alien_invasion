import sys
import pygame
from time import sleep
from random import randint
from bullet import Bullet
from alien import Alien
from star import Star


def check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, stats)
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_RETURN or event.key == pygame.K_p:
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


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


def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb):
    """Обработка событий в игре"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # обработка события нажатия клавиши
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, aliens, bullets, stats, sb)
        # обработка события отпускания клавиши
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        # обработка события нажатия любой клавиши мыши
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # получение координат точки нажатия клавиши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # проверка нажатия клавиши в пределах кнопки и запуск игры заново в активном состоянии
            check_play_button(stats, play_button, mouse_x, mouse_y, ship, aliens, bullets, ai_settings, screen, sb)


def start_game(stats, aliens, bullets, ai_settings, screen, ship, sb):
    """Функция настройки игровых элементов при старте игры"""
    # скрытие курсора мыши
    pygame.mouse.set_visible(False)
    # сброс статистики (доступно исходное кол-во попыток для игрока)
    stats.reset_stats()
    sb.prep_score()
    sb.prep_level()
    sb.prep_high_score()
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
    if button_clicked and not stats.game_active:
        # сброс скоростей игровых элементов
        ai_settings.initialize_dynamic_settings()
        # вызов функции настройки игровых элементов при старте
        start_game(stats, aliens, bullets, ai_settings, screen, ship, sb)


def create_gradient(start_color, end_color, width, height):
    """Создание поверхности градиента из двух цветов"""
    gradient_surface = pygame.Surface((width, height))
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
        gradient_surface.fill((r, g, b), (0, y, width, 1))

    return gradient_surface


def update_screen(ai_settings, screen, ship, aliens, bullets, stars, stats, play_button, game_title, sb):
    """Обновляет экран и отрисовывает всё содержимоё на нём"""
    # вариант заполнения экрана сплошным цветом фона
    # screen.fill(ai_settings.bg_color)

    # начальный/конечный цвета градиента фона
    start_color = (7, 16, 40)
    end_color = (9, 114, 167)
    # создание и конвертация поверхности градиента
    gradient_surface = create_gradient(start_color, end_color, ai_settings.screen_width, ai_settings.screen_height)
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

    # вывод счета, рекорда, текущего уровня игры
    sb.show_score()

    # отрисовка кнопки Play, надписи названия игры поверх всех объектов,
    # очистка экаран от пришельцев и пуль, сброс статистики при неактивном состоянии игры
    if not stats.game_active:
        game_title.blitme()
        play_button.draw_button()
        aliens.empty()
        bullets.empty()
        stats.reset_stats()
        sb.prep_score()
        sb.prep_level()

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
    """Обработка столконовений пуль с пришельцами"""
    # удаление пуль и пришельцев во время столкновения
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    # при попадании пули по пришельцу увеличивается счёт игры и создается новое изображение с текстом счета
    if collisions:
        for aliens in collisions.values():
            # значение счёта учитывает все попадания одного снаряда
            stats.score += ai_settings.alien_points * len(aliens)
        # формирование и вывод изображения с текстом счёта
        sb.prep_score()
        # проверка достижения рекордного счёта
        check_high_score(stats, sb)

    # для случая отсутствия флота пришельцев после его уничтожения
    if len(aliens) == 0:
        # уничтожение оставшихся пуль, увеличение скорости и уровня игры, создание нового флота пришельцев
        sleep(2.5)
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets, stats):
    """Позволяет совершить выстрел если максимум пуль еще не достигнут"""
    if len(bullets) < ai_settings.bullets_allowed and stats.game_active:
        # создание новой пули и включение её в группу bullets
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_high_score(stats, sb):
    """Проверка достижения нового рекорда"""
    if stats.score > stats.high_score:
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


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Обработка столкновения корабля с флотом пришельцев / достижения флотом нижнего края экрана
    и переход игры в начальное состояние"""
    if stats.ship_left > 0:
        # уменьшение значения оставшихся кораблей
        stats.ship_left -= 1
        # очистка групп пришельцев и пуль
        aliens.empty()
        bullets.empty()
        # создание нового флота и корабля игрока
        create_fleet(ai_settings, screen, ship, aliens)
        # задание паузы
        sleep(1.5)
    else:
        # переход игры в неактивное состояние и отображение курсора мыши
        stats.game_active = False
        pygame.mouse.set_visible(True)
        sleep(1.5)

    ship.center_ship()


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Проверка достижения флотом нижнего края экрана"""
    screen_rect = screen.get_rect()
    # при достижении кораблем флота нижнего края экрана игра переходит в начальное состояние
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Обновление позиций всех пришельцев во флоте,
     обработка столкновений флота с кораблем игрока
     обработка достижения флотом нижнего края экрана"""
    # проверка достижения флотом края экрана
    check_fleet_edges(ai_settings, aliens)
    # обновление позиции флота
    aliens.update()
    # проверка и реакция на обнаружение коллизии между кораблем и флотом
    if pygame.sprite.spritecollideany(ship, aliens):
        # переход игры в начальное состояние
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # проверка достижения флотом нижнего края экрана
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


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
