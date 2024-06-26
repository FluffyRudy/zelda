from settings import (
    FONT_SIZE,
    HEALTH_BAR_WIDTH,
    HEALTH_BAR_HEIGHT,
    ENERGY_BAR_WIDTH,
    ENERGY_BAR_HEIGHT,
    ITEM_BOX_SIZE,
    HEALTH_COLOR,
    ENERGY_COLOR,
    LOWER_LAYER_COLOR,
    PROJECT_DIR,
)
from pygame.math import Vector2
import pygame
import os


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()

        self.offset_x = 10
        self.offset_y = 10

        self.player = player

        self.weapon_image = player.weapon_handler.weapon.copy()
        self.get_current_magic = self.player.magic_handler.get_current_magic
        self.weapon_pos = (
            ITEM_BOX_SIZE // 2 - self.weapon_image.get_width() // 2,
            ITEM_BOX_SIZE // 2 - self.weapon_image.get_height() // 2,
        )

        self.magic_pos = (
            self.offset_x + ITEM_BOX_SIZE,
            ITEM_BOX_SIZE // 2 - self.get_current_magic().get_height() // 2,
        )

        self.font = pygame.font.Font(
            os.path.join(PROJECT_DIR, "graphics/font/joystix.ttf"), 24
        )

        self.exp_label_pos = Vector2(
            self.display_surface.get_width(), self.display_surface.get_height()
        )

        self.item_box_surf = pygame.Surface(
            (ITEM_BOX_SIZE * 2 + self.offset_x, ITEM_BOX_SIZE), pygame.SRCALPHA
        ).convert_alpha()
        self.item_box_pos = 0, self.display_surface.get_height() - ITEM_BOX_SIZE
        self.item_box_surf.fill((50, 91, 103, 150))

    def weapon_overlay(self):
        self.item_box_surf.blit(self.weapon_image, self.weapon_pos)

    def magic_overlay(self):
        self.item_box_surf.blit(self.get_current_magic(), self.magic_pos)

    def display(self):
        self.item_box_surf.fill((50, 91, 103, 100))

        exp_label = self.font.render(
            f" {self.player.get_current_exp()} ", True, "white", "black"
        )
        self.display_surface.blit(
            exp_label,
            self.exp_label_pos - (exp_label.get_width(), exp_label.get_height()),
        )

        pygame.draw.rect(
            self.display_surface,
            "brown",
            (
                self.offset_x,
                self.offset_y,
                self.player.STATS["health"]["amount"],
                HEALTH_BAR_HEIGHT,
            ),
            0,
            5,
        )

        pygame.draw.rect(
            self.display_surface,
            "red",
            (
                self.offset_x,
                self.offset_y,
                self.player.get_current_health(),
                HEALTH_BAR_HEIGHT,
            ),
            0,
            5,
        )
        pygame.draw.rect(
            self.display_surface,
            "brown",
            (
                self.offset_x,
                self.offset_y + HEALTH_BAR_HEIGHT + self.offset_y,
                self.player.STATS["energy"]["amount"],
                ENERGY_BAR_HEIGHT,
            ),
            0,
            5,
        )

        pygame.draw.rect(
            self.display_surface,
            "skyblue",
            (
                self.offset_x,
                self.offset_y + ENERGY_BAR_HEIGHT + self.offset_y,
                self.player.get_current_energy(),
                ENERGY_BAR_HEIGHT,
            ),
            0,
            5,
        )
        self.display_surface.blit(self.item_box_surf, self.item_box_pos)
        self.weapon_overlay()
        self.magic_overlay()
        self.display_surface.blit(self.item_box_surf, self.item_box_pos)
