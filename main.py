from typing import Optional
import sys
from random import choice
from settings import WIDTH, HEIGHT, TILESIZE, FPS
import pygame
from level import Level
from upgrade import Upgrade


class Game:
    BLACK = pygame.Color(0, 0, 0, 255)

    def __init__(self):
        self.initialize()
        pygame.display.set_caption("ZELDA")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.viewport = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.max_fade_radius = self.screen.get_height()
        self.fade_radius = 0
        self.contrast = pygame.Color(0, 0, 0, 0)
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.upgrade_menu = Upgrade(self.level.get_player(), self.viewport)

    def handle_event(self) -> Optional[None]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_viewport_alpha(self):
        if self.contrast.a < 255:
            self.contrast_alpha = 255 * (self.fade_radius / self.max_fade_radius) + 50
            self.contrast.a = min(int(self.contrast_alpha), 255)

    def apply_circular_fade(self):
        pygame.draw.circle(
            self.viewport,
            (0, 0, 0, self.contrast.a),
            (self.screen.get_width() // 2, self.screen.get_height() // 2),
            self.fade_radius,
            5,
        )

    def initialize(self):
        pygame.init()
        pygame.display.set_caption("ZELDA")

    def update(self):
        self.handle_event()
        self.level.run()

    def render(self):
        self.fade_radius = min(self.fade_radius + 3, self.max_fade_radius)
        if self.fade_radius < self.max_fade_radius:
            self.apply_circular_fade()
            self.update_viewport_alpha()
        self.screen.blit(self.viewport, (0, 0))

    def run(self) -> None:
        while True:
            self.update()
            self.render()
            self.level.ui.display()
            pygame.display.update()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
