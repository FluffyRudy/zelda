import pygame
from pygame.math import Vector2
from frameloader import load_frames
from player import Player
from settings import PROJECT_DIR
from os.path import join


class Magic(pygame.sprite.Sprite):
    def __init__(self, entity: dict, player: Player, groups: list[pygame.sprite.Group]):
        super().__init__(groups)


class StaticFlame(Magic):
    def __init__(self, entity: dict, player: Player, groups: list[pygame.sprite.Group]):
        super().__init__(entity, player, groups)

        self.type = entity["type"]
        self.strength = player.STATS["flame"]["amount"]
        self.image = pygame.image.load(entity["image"]).convert_alpha()
        self.frames = load_frames(entity["frames"])

        direction = player.animation_handler.status.split("_")[0]
        action_map = {
            "left": (-1, 0.5),
            "right": (1, 0.5),
            "up": (0, -1),
            "down": (0, 1),
        }

        dirx, diry = action_map[direction]
        pos_x = player.rect.centerx + dirx * self.image.get_width() // 2
        pos_y = player.rect.centery + diry * self.image.get_height() // 2
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        self.kill()


class Flame(StaticFlame):
    def __init__(self, entity: dict, player: Player, groups: list[pygame.sprite.Group]):
        super().__init__(entity, player, groups)

        direction = player.animation_handler.status.split("_")[0]
        action_map = {
            "left": (-1, 0.5),
            "right": (1, 0.5),
            "up": (0, -1),
            "down": (0, 1),
        }

        self.speed = 8
        self.direction = Vector2(action_map[direction])
        self.frame_index = 0
        self.animation_speed = 0.1
        self.sound = pygame.mixer.Sound(join(PROJECT_DIR, "audio/attack/fireball.wav"))

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.animate()
        self.rect.x += int(self.direction.x) * self.speed
        self.rect.y += int(self.direction.y) * self.speed


class Heal(Magic):
    def __init__(self, entity: dict, player: Player, groups: list[pygame.sprite.Group]):
        super().__init__(entity, player, groups)

        player.update_health(player.STATS["heal"]["amount"])

        self.type = entity["type"]
        self.strength = player.STATS["heal"]["amount"]

        self.follow_rect = player.rect

        self.player = player
        self.diry = player.direction.y
        self.speed = player.speed
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = pygame.image.load(entity["image"]).convert_alpha()
        self.frames = load_frames(entity["frames"])

        pos_x = player.rect.centerx
        pos_y = player.rect.centery
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.sound = pygame.mixer.Sound(join(PROJECT_DIR, "audio/heal.wav"))

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.sound.play()
        self.animate()
        self.rect.center = self.player.rect.center
