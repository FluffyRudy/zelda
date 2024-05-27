from settings import TILESIZE
import pygame
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle, Sprite
from tile import Tile
from player import Player
from tiledmaploader import TiledMapLoader
from debug import Debug


class Level:
    def __init__(self):
        self.display_surface: Surface = pygame.display.get_surface()

        self.map_data = TiledMapLoader('maps/tmx/map.tmx')

        self.visible_sprites: YSortCameraGroup = YSortCameraGroup(self.map_data)
        self.obstacle_sprites: Group = Group()

        self.setup_level()

    def update(self):
        pass

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.draw(relative_sprite=self.player)

    def setup_level(self):
        self.player = Player(self.map_data.player_pos, self.visible_sprites, self.obstacle_sprites)
        for pos_x, pos_y in self.map_data.boundries:
            Tile((pos_x, pos_y), self.visible_sprites)

class YSortCameraGroup(Group):
    def __init__(self, map_data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen_center_x = self.display_surface.get_width() // 2
        self.screen_center_y = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        self.floor = map_data.ground
        self.floor_rect = self.floor.get_rect(center=(0, 0))

    def draw(self, relative_sprite: Sprite):
        self.offset.x = relative_sprite.rect.centerx - self.screen_center_x
        self.offset.y = relative_sprite.rect.centery - self.screen_center_y

        self.draw_floor(self.offset)

        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.y)
        for sprite in sorted_sprites:
            offset_rect = sprite.rect.center - self.offset
            self.display_surface.blit(sprite.image, offset_rect)
    
    def draw_floor(self, offset: tuple):
        offset_rect = self.floor_rect.center - offset
        self.display_surface.blit(self.floor, offset_rect)

    def draw_obstacle(self, offset: tuple):
        offset_rect 