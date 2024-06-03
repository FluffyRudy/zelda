from settings import TILESIZE
import pygame
from pygame.image import load
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle
from frameloader import load_frames
from typing import Iterable


class Tile(pygame.sprite.Sprite):
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
