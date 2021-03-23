import pygame
from pygame.locals import *
import sys
from core.racetrack import Track
from core.constants import BACKGROUND_COLOR, SIZE

pygame.init()

class Driver():
    def __init__(self, debug: bool = False):
        self.screen_res = SIZE[0], SIZE[1]
        self.screen = pygame.display.set_mode(self.screen_res, pygame.RESIZABLE)
        self.background = BACKGROUND_COLOR
        self.debug = debug
        self.Track = Track()
        self.img = pygame.image.load('grass.png')

    def run(self):
        while True:
            self.Loop()

    def Loop(self):
        self.EventLoop()
        self.Draw()
        self.Track.Draw(self.screen, self.debug)
        pygame.display.update()

    def EventLoop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def Draw(self):
        #self.screen.fill(self.background)
        for y in range(0, 800, 384):
            for x in range(0, 800, 384):
                self.screen.blit(self.img, (x, y))
