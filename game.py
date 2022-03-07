from tkinter import font
import pygame
from settings import *

# Initialize clock for dt and limiting the framerate
clock = pygame.time.Clock()

class Game:
    def __init__(self, caption, icon, resolution, font):
        pygame.init()
        pygame.display.set_caption(caption)
        self.gameIcon = pygame.image.load(icon)
        self.screen = pygame.display.set_mode(resolution)
        self.SCREEN_WIDTH = pygame.display.get_window_size()[0]
        self.SCREEN_HEIGHT = pygame.display.get_window_size()[1]
        pygame.font.init()
        self.font = pygame.font.SysFont(font, 30)
        self.fireballState = 'ready'
        self.score = 0
        self.playerAlive = True
        self.active = True
        self.waiting = False
    def waitForKey(self, text):
        self.waiting = True
        while self.waiting:
            clock.tick(fpsLimit)
            gameOverText = game.font.render(text, False, (0, 0, 0))
            textRect = gameOverText.get_rect(center=(self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2))
            game.screen.blit(gameOverText,textRect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.waiting = False
                        self.playerAlive = True
            if not self.active:
                break
            pygame.display.update()

# Game initialization
game = Game(title, icon, resolution, font_)