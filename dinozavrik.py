import pygame
from settings import Settings

class DinoObject():
    def __init__(self, ui_game):
        self.screen = ui_game.screen
        self.settings = Settings()
        self.screen_rect = ui_game.screen.get_rect()
        self.images = [pygame.image.load("dinozavr2.png"), pygame.image.load("dinozavr3.png")]
        self.rect = self.images[0].get_rect()
        self.rect.x = 100
        self.rect.y = self.settings.screen_height//2+90
        self.settings = Settings()
        self.y = float(self.rect.y)
        self.count = 0

    def blitme(self):
        if self.count == 12:
                self.count = 0
        s = self.count//8
        self.images[s] = pygame.transform.scale(self.images[s], (90, 80))
        self.screen.blit(self.images[s], self.rect)
        self.count += 1
        