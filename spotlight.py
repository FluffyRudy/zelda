import pygame


class Spotlight:
    def __init__(self, screen):
        self.screen = screen
        self.viewport = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.max_fade_radius = screen.get_height()
        self.fade_radius = 0
        self.contrast = pygame.Color(0, 0, 0, 0)
        self.fade_increment = 1
        self.fade_increment_factor = 0.5

    def update_alpha(self):
        if self.contrast.a < 255:
            contrast_alpha = (
                255 * (self.fade_radius / self.max_fade_radius) + self.fade_increment
            )
            self.contrast.a = min(int(contrast_alpha), 255)
            self.fade_increment += self.fade_increment_factor

    def apply(self):
        pygame.draw.circle(
            self.viewport,
            (0, 0, 0, self.contrast.a),
            (self.screen.get_width() // 2, self.screen.get_height() // 2),
            self.fade_radius,
            5,
        )

    def update(self):
        self.fade_radius = min(self.fade_radius + 3, self.max_fade_radius)
        if self.fade_radius < self.max_fade_radius:
            self.apply()
            self.update_alpha()
        self.screen.blit(self.viewport, (0, 0))
