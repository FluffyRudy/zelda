from typing import Optional
import sys
from random import choice
from settings import WIDTH, HEIGHT, TILESIZE, FPS
import pygame
from spotlight import Spotlight
from level import Level
from upgrade import Upgrade


class Game:
    BLACK = pygame.Color(0, 0, 0, 255)

    def __init__(self):
        self.initialize()
        pygame.display.set_caption("ZELDA")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fade_effect = Spotlight(self.screen)
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.upgrade_menu = Upgrade(self.level.get_player())
        self.paused = False

    def handle_event(self) -> Optional[None]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

    def initialize(self):
        pygame.init()
        pygame.display.set_caption("ZELDA")

    def run(self) -> None:
        while True:
            self.handle_event()
            if not self.paused:
                self.level.run()
                self.fade_effect.update()
                self.level.ui.display()
            else:
                self.upgrade_menu.display()
            pygame.display.update()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
