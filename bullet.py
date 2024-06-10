import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Базовый класс для управления пулями корабля игрока и пришельца"""
    def __init__(self, ai_settings, screen, game_ship):
        """"""
        super().__init__()
        self.screen = screen
        self.game_ship = game_ship
        self.speed_factor = ai_settings.bullet_speed_factor
        self.color = None
        self.rect = None

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class ShipBullet(Bullet):
    """"""
    def __init__(self, ai_settings, screen, ship):
        super().__init__(ai_settings, screen, ship)
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width_for_ship, ai_settings.bullet_height_for_ship)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.color = ai_settings.bullet_color_for_ship
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y


class AlienBullet(Bullet):
    """"""
    def __init__(self, ai_settings, screen, alien):
        super().__init__(ai_settings, screen, alien)
        self.image = pygame.image.load('images/alien_bullet.png')
        self.image = pygame.transform.scale(self.image, (22, 45))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.bottom = alien.rect.bottom
        self.y = float(self.rect.y)

    def update(self):
        """"""
        self.y += self.speed_factor / 2
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)


