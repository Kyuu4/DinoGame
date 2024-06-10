import pygame
class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (121, 189, 237)
        self.fon = pygame.image.load("fon.jpg")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))



       