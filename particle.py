import pygame
from os.path import join
from os import listdir
from random import shuffle
from frameloader import load_frames
from typing import Iterable, Callable


class Particle(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        particle_type: str,
        groups: Iterable[pygame.sprite.Group],
        flip_x=False,
        is_dynamic=False,
    ):
        super().__init__(groups)

        base_path = "graphics/particles/"

        self.frame_index = 0
        self.animation_speed = 0.15

        self.frames = load_frames(join(base_path, particle_type), flip_x)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.is_dynamic = is_dynamic

    def update(self):
        self.animate()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update_position(self, new_pos: pygame.Rect):
        if self.is_dynamic:
            self.rect.center = new_pos.center


def grass_destruction_particle(pos: tuple[int, int], groups: list[pygame.sprite.Group]):
    leaf_types = [f"leaf{i}" for i in range(1, 6 + 1)]
    shuffle(leaf_types)

    for idx, leaf_type in enumerate(leaf_types):
        grass_type = leaf_type
        flip = idx % 2 == 0
        Particle(pos, grass_type, groups, flip)
