from typing import Optional
import sys
from random import choice
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
        self.max_fade_radius = self.screen.get_height()
        self.fade_radius = 0
        self.contrast = pygame.Color(0, 0, 0, 0)
        self.clock = pygame.time.Clock()
        self.level = Level()

    def handle_event(self) -> Optional[None]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.fade_radius = min(self.fade_radius + 2, self.max_fade_radius)
                self.update_viewport_alpha()

    def update_viewport_alpha(self):
        if self.contrast.a < 255:
            self.contrast_alpha = 255 * (self.fade_radius / self.max_fade_radius)
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
        if self.level.player.get_current_health() <= 0:
            self.fade_radius = min(self.fade_radius + 3, self.max_fade_radius)
            self.update_viewport_alpha()
        else:
            self.level.run()

    def render(self):
        self.viewport.fill((0, 0, 0, 0))
        if self.level.player.get_current_health() <= 0:
            self.apply_circular_fade()
        self.screen.blit(self.viewport, (0, 0))
        pygame.display.update()

    def run(self) -> None:
        self.initialize()
        while True:
            self.update()
            self.render()
            self.clock.tick(FPS)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
