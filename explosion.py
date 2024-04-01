import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    """"""
    def __init__(self, ai_settings, screen, pos_x, pos_y):
        """"""
        super().__init__()
        self.ai_settings = ai_settings
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.image = pygame.image.load('images/explotion.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.creation_time = pygame.time.get_ticks()
        self.explosion_duration = 350

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        self.x = float(self.rect.x)
        self.y = self.rect.y

    def update(self):
        """"""
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= self.explosion_duration:
            self.kill()
        else:
            alpha = (pygame.time.get_ticks() - self.creation_time) / self.explosion_duration * 255
            self.image.set_alpha(255 - alpha)

        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        self.y = self.rect.y

    def blitme(self):
        """"""
        self.screen.blit(self.image, self.rect)
