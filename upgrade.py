import pygame
from typing import Optional, Callable
from settings import UPGRADE_BOX_SIZE, GEAR_SIZE


class Upgrade:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.num_boxes = 4
        self.spacing = 10

        self.positions = self.calculate_positions()
        self.selection_index = 0

        # Initialize upgrade boxes
        self.health_box = UpgradeBox(self.positions[0], "HEALTH")
        self.energy_box = UpgradeBox(self.positions[1], "ENERGY")
        self.weapon_box = UpgradeBox(self.positions[2], "WEAPON")
        self.magic_box = UpgradeBox(self.positions[3], "MAGIC")

    def calculate_positions(self):
        total_width = (
            self.num_boxes * UPGRADE_BOX_SIZE[0] + (self.num_boxes - 1) * self.spacing
        )
        offset_x = (self.display_surface.get_width() - total_width) // 2
        offset_y = (self.display_surface.get_height() - UPGRADE_BOX_SIZE[1]) // 2

        return [
            (offset_x + i * (UPGRADE_BOX_SIZE[0] + self.spacing), offset_y)
            for i in range(self.num_boxes)
        ]

    def display(self):
        self.display_surface.fill((0, 0, 0))
        for box in [self.health_box, self.energy_box, self.weapon_box, self.magic_box]:
            box.display(self.display_surface)


class UpgradeBox:
    LINE_WIDTH = 25
    OFFSET = (10, 10)

    def __init__(
        self,
        pos: tuple[int, int],
        label: str,
        action: Optional[Callable] = None,
    ):
        self.font = self.load_font()
        self.position = pos
        self.surface = self.create_surface(UPGRADE_BOX_SIZE)
        self.rect = self.surface.get_rect(topleft=pos)
        self.label = self.render_label(label)
        self.label_position = self.calculate_label_position()
        self.upgrade_line_size = self.calculate_upgrade_line_size()
        self.upgrade_line_pos = self.calculate_upgrade_line_position()
        self.upgrade_line_rect = pygame.Rect(
            (
                self.rect.left + self.upgrade_line_pos[0],
                self.rect.top + self.upgrade_line_pos[1],
            ),
            self.upgrade_line_size,
        )

        self.gear = Gear(self.rect, self.upgrade_line_rect)

    def load_font(self) -> pygame.font.Font:
        return pygame.font.Font("graphics/font/joystix.ttf", 24)

    def create_surface(self, size: tuple[int, int]) -> pygame.Surface:
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 250, 200, 50))
        return surface

    def render_label(self, label: str) -> pygame.Surface:
        return self.font.render(label, True, "white")

    def calculate_label_position(self) -> tuple[int, int]:
        return (UPGRADE_BOX_SIZE[0] - self.label.get_width()) // 2, 0

    def calculate_upgrade_line_size(self) -> tuple[int, int]:
        return (
            self.LINE_WIDTH,
            self.surface.get_height() - self.label.get_height() - self.OFFSET[1] * 2,
        )

    def calculate_upgrade_line_position(self) -> tuple[int, int]:
        return (
            self.surface.get_width() // 2 - self.upgrade_line_size[0] // 2,
            self.label.get_height() + self.OFFSET[1],
        )

    def display(self, surface: pygame.Surface):
        self.surface.blit(self.label, self.label_position)
        surface.blit(self.surface, self.position)
        pygame.draw.rect(
            self.surface, "white", (*self.upgrade_line_pos, *self.upgrade_line_size)
        )
        self.gear.display(surface)


class Gear:
    def __init__(self, parent_rect: pygame.Rect, upgrade_line_rect: pygame.Rect):
        parent_rect = parent_rect
        self.upgrade_line_rect = upgrade_line_rect
        self.image = pygame.Surface(GEAR_SIZE, pygame.SRCALPHA)
        self.rect = self.image.get_rect(midbottom=parent_rect.midbottom)

    def display(self, display_surface: pygame.Surface):
        self.update()
        pygame.draw.rect(display_surface, "brown", self.rect, 0, 5)

    def update(self):
        mouse_pos, is_pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]
        if self.upgrade_line_rect.collidepoint(mouse_pos) and is_pressed:
            self.rect.center = (self.rect.centerx, mouse_pos[1])
