from settings import TILESIZE
import pygame
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle, Sprite
from tile import Tile
from player import Player
from weapon import Weapon
from ui import UI
from tiledmaploader import TiledMapLoader
from debug import Debug


class Level:
    def __init__(self):
        self.display_surface: Surface = pygame.display.get_surface()

        self.map_data = TiledMapLoader('maps/tmx/map.tmx')

        self.visible_sprites: YSortCameraGroup = YSortCameraGroup(self.map_data)
        self.obstacle_sprites: Group = Group()

        self.setup_level()
        
        self.current_weapon = None
        
        self.ui = UI(self.player)

        self.debug = Debug()

    def show_weapon(self):
        self.current_weapon = Weapon(self.player, [self.visible_sprites])

    def hide_weapon(self):
        if self.current_weapon:
            self.current_weapon.kill()
        self.current_weapon = None

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.draw(relative_sprite=self.player)
        self.debug.debug(self.player.status)
        self.ui.display()

    def setup_level(self):
        self.player = Player(self.map_data.player_pos, [self.visible_sprites], self.obstacle_sprites, self.show_weapon, self.hide_weapon)
        for pos_x, pos_y,_ in self.map_data.boundries:
            Tile((pos_x, pos_y), [self.obstacle_sprites])
        for pos_x, pos_y, image in self.map_data.grasses:
            Tile((pos_x, pos_y), [self.obstacle_sprites, self.visible_sprites], image)
        for pos_x, pos_y, image in self.map_data.trees:
            Tile((pos_x, pos_y), [self.obstacle_sprites, self.visible_sprites], image)
        for pos_x, pos_y, image in self.map_data.blocks:
            Tile((pos_x, pos_y), [self.obstacle_sprites, self.visible_sprites], image)

class YSortCameraGroup(Group):
    def __init__(self, map_data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen_center_x = self.display_surface.get_width() // 2
        self.screen_center_y = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        self.floor = map_data.ground
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

    def draw(self, relative_sprite: Sprite):
        self.offset.x = relative_sprite.rect.left - self.screen_center_x
        self.offset.y = relative_sprite.rect.top - self.screen_center_y

        self.draw_floor(self.offset)

        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.y)
        for sprite in sorted_sprites:
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)
    
    def draw_floor(self, offset: tuple):
        offset_rect = self.floor_rect.topleft - offset
        self.display_surface.blit(self.floor, offset_rect)
