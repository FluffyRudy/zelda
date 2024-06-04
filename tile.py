from settings import TILESIZE
import pygame
from pygame.image import load
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle
from frameloader import load_frames
from particle import grass_destruction_particle
from typing import Iterable, Optional, TypedDict


class ParticlesGroupType(TypedDict):
    visibility_group: pygame.sprite.Group
    particle_group: pygame.sprite.Group


class Tile(pygame.sprite.Sprite):
    PARTICLE_GROUP: Optional[ParticlesGroupType] = None

    def __init__(
        self,
        pos: tuple[int, int],
        group: Iterable[pygame.sprite.Group],
        surface=pygame.Surface((TILESIZE, TILESIZE)),
    ):
        super().__init__(group)
        self.image: Surface = surface
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-TILESIZE // 2.5, -TILESIZE // 1.5)
        self.mask = pygame.mask.from_surface(self.image)


class Grass(Tile):
    def __init__(
        self,
        pos: tuple[int, int],
        group: Iterable[pygame.sprite.Group],
        surface=pygame.Surface((TILESIZE, TILESIZE)),
    ):
        super().__init__(pos, group, surface)

    @classmethod
    def set_particle_groups(cls, group_dict: ParticlesGroupType):
        cls.PARTICLE_GROUP = group_dict

    def get_damage(self, damage=0):
        center = self.hitbox.center
        grass_destruction_particle(
            center,
            [
                self.PARTICLE_GROUP["visible_group"],
                self.PARTICLE_GROUP["particle_group"],
            ],
        )
        self.kill()
