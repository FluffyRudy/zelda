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
)
from pygame.math import Vector2
import pygame


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()

        self.offset_x = 10
        self.offset_y = 10

        self.get_current_magic = player.magic_handler.get_current_magic

        self.get_player_health = player.get_current_health
        self.get_player_energy = player.get_current_energy
        self.get_player_exp = player.get_current_exp

        self.weapon_image = player.weapon_handler.weapon.copy()
        self.weapon_pos = (
            ITEM_BOX_SIZE // 2 - self.weapon_image.get_width() // 2,
            ITEM_BOX_SIZE // 2 - self.weapon_image.get_height() // 2,
        )

        self.magic_pos = (
            self.offset_x + ITEM_BOX_SIZE,
            ITEM_BOX_SIZE // 2 - self.get_current_magic().get_height() // 2,
        )

        self.font = pygame.font.Font("graphics/font/joystix.ttf", FONT_SIZE)

        self.health_bar_rect = pygame.Rect(
            self.offset_x, self.offset_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT
        )
        self.energy_bar_rect = pygame.Rect(
            self.offset_x, self.offset_y * 3, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT
        )

        self.lower_health_layer_rect = self.health_bar_rect.copy()
        self.lower_energy_layer_rect = self.energy_bar_rect.copy()
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
        pygame.draw.rect(
            self.display_surface, LOWER_LAYER_COLOR, self.lower_health_layer_rect, 0, 3
        )
        pygame.draw.rect(
            self.display_surface, LOWER_LAYER_COLOR, self.lower_energy_layer_rect, 0, 3
        )
        exp_label = self.font.render(
            f" {self.get_player_exp()} ", True, "white", "black"
        )
        self.display_surface.blit(
            exp_label,
            self.exp_label_pos - (exp_label.get_width(), exp_label.get_height()),
        )
        pygame.draw.rect(self.display_surface, HEALTH_COLOR, self.health_bar_rect, 0, 3)
        pygame.draw.rect(self.display_surface, ENERGY_COLOR, self.energy_bar_rect, 0, 3)
        self.health_bar_rect.width = self.get_player_health()
        self.energy_bar_rect.width = self.get_player_energy()
        self.display_surface.blit(self.item_box_surf, self.item_box_pos)
        self.weapon_overlay()
        self.magic_overlay()
        self.display_surface.blit(self.item_box_surf, self.item_box_pos)
