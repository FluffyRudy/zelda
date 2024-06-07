from typing import Optional
import sys
from random import choice
from settings import WIDTH, HEIGHT, TILESIZE, FPS
import pygame
from level import Level


class Game:
    BLACK = pygame.Color(0, 0, 0, 255)

    def __init__(self):
        self.initialize()
        pygame.display.set_caption("ZELDA")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

    def handle_event(self) -> Optional[None]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.level.toggle_upgrade_menu()

    def initialize(self):
        pygame.init()
        pygame.display.set_caption("ZELDA")

    def run(self) -> None:
        while True:
            self.handle_event()
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
