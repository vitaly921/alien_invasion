import pygame


class GameTitle:
    """"""
    def __init__(self, screen):
        """"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        #
        self.image = pygame.image.load('images/name_game.png')
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        #
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery / 1.5

    def blitme(self):
        """"""
        self.screen.blit(self.image, self.rect)
