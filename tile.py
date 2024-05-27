from settings import TILESIZE
import pygame
from pygame.image import load
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], group: [Group, GroupSingle]):
        super().__init__(group)
        self.image: Surface = pygame.Surface((TILESIZE, TILESIZE))
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
