import pygame
from os.path import join
from os import listdir
from random import randint
from frameloader import load_frames
from typing import Iterable


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        particle_type: str,
        groups: Iterable[pygame.sprite.Group],
    ):
        super().__init__(groups)

        base_path = "graphics/particles/"

        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = load_frames(join(base_path, particle_type))

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            self.kill()
        self.image = self.frames[int(self.frame_index)]


class EnemyAttackParticle(Particle):
    def __init__(
        self,
        pos: tuple[int, int],
        particle_type: str,
        groups: Iterable[pygame.sprite.Group],
    ):
        super().__init__(pos, particle_type, groups)

    def update_position(self, player_rect: pygame.Rect):
        self.rect.center = player_rect.center
