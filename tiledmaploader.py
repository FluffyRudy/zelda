import pygame
import pytmx
from settings import TILESIZE
from typing import Optional, Union


class TiledMapLoader:
    def __init__(self, path: str):
        map_data: pytmx.TiledMap = pytmx.load_pygame(path)
        self.width = TILESIZE * map_data.width
        self.height = TILESIZE * map_data.height
        self.w = map_data.width
        self.h = map_data.height

        # data
        self.ground = None
        self.boundries: list[pygame.Rect, Optional[pygame.Surface]] = []
        self.enemies: list[tuple[int, int, pygame.Surface]] = []
        self.grasses: list[tuple[int, int, pygame.Surface]] = []
        self.trees: list[tuple[int, int, pygame.Surface]] = []
        self.blocks: list[tuple[int, int, pygame.Surface]] = []
        self.player_pos = (0, 0)

        self.load_map(map_data)

    def load_map(self, map_data):
        # main ground
        ground: pytmx.TiledImageLayer = self.__get_layer_by_name("ground", map_data)
        self.ground = ground.image

        # player
        player = self.__get_layer_by_name("player", map_data)[0]
        self.player_pos = (player.x, player.y)

        self.load_layer("boundry", self.boundries, map_data)
        self.load_layer("grass", self.grasses, map_data)
        self.load_layer("tree", self.trees, map_data)
        self.load_layer("enemies", self.enemies, map_data)
        self.load_layer("block", self.blocks, map_data)

    def load_layer(self, layername: str, target: list, map_data):
        layer: Union[pytmx.TiledTileLayer, pytmx.TiledObjectGroup] = (
            self.__get_layer_by_name(layername, map_data)
        )
        if isinstance(layer, pytmx.TiledTileLayer):
            for tree in layer:
                x, y, gid = tree
                image = self.__get_image_by_gid(gid, map_data)
                if image:
                    target.append((x * TILESIZE, y * TILESIZE, image))
        elif isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                monster_type = obj.properties["monster_type"]
                x, y, image = obj.x, obj.y, obj.image
                target.append((monster_type, x, y, image))

    def __get_layer_by_name(self, name: str, map_data: pytmx.TiledMap):
        return map_data.layernames[name]

    def __get_image_by_gid(self, gid, map_data):
        return map_data.get_tile_image_by_gid(gid)

    def __get_props_by_gid(self, map_data):
        pass
