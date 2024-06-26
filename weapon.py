import pygame
from settings import ATTACK_DELAY, PROJECT_DIR
from pygame.math import Vector2
import os


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: pygame.sprite.Sprite, groups: pygame.sprite.Group):
        super().__init__(groups)

        self.damage = player.STATS["attack"]["amount"]

        path = os.path.join(PROJECT_DIR, "graphics/weapons/sword/")
        direction = player.animation_handler.status.split("_")[0]
        action_map = {
            "left": {"image": "left.png", "pos": (-1, 0.5)},
            "right": {"image": "right.png", "pos": (1, 0.5)},
            "up": {"image": "up.png", "pos": (0, -1)},
            "down": {"image": "down.png", "pos": (0, 1)},
        }
        image = action_map[direction]["image"]
        path += image

        self.image = pygame.image.load(path).convert_alpha()
        dirx, diry = action_map[direction]["pos"]
        pos_x = player.rect.centerx + dirx * self.image.get_width()
        pos_y = player.rect.centery + diry * self.image.get_height()
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def hide_weapon(self):
        self.kill()
