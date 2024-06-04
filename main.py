from typing import Optional
import sys
from settings import WIDTH, HEIGHT, TILESIZE, FPS
import pygame
from level import Level


class Game:
    BLACK = pygame.Color(0, 0, 0, 255)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("ZELDA")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.viewport = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.viewport_bg = pygame.Color(0, 0, 0, 0)
        self.clock = pygame.time.Clock()

        self.level = Level()

    def handle_event(self) -> Optional[None]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.viewport_bg.a = min(self.viewport_bg.a + 10, 255)

    def run(self) -> None:
        while True:
            self.handle_event()
            self.level.run()
            self.viewport.fill(self.viewport_bg)
            self.screen.blit(self.viewport, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
