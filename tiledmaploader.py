import pygame
import pytmx
from settings import TILESIZE

class TiledMapLoader:
    def __init__(self, path: str):
        map_data: pytmx.TiledMap = pytmx.load_pygame(path)
        self.tilewidth = map_data.tilewidth
        self.tileheight = map_data.tileheight
        self.width = self.tilewidth * map_data.width
        self.height = self.tileheight * map_data.height
        self.w = map_data.width
        self.h = map_data.height

        #data
        self.ground = None
        self.boundries = []
        self.obstacles = []
        self.player_pos = (0, 0)

        self.load_map(map_data)

    def load_map(self, map_data):
        ground: pytmx.TiledImageLayer = self.__get_layer_by_name('ground', map_data)
        self.ground = ground.image

        player = self.__get_layer_by_name('player', map_data)[0]
        self.player_pos = ( player.x, player.y )

        boundries = self.__get_layer_by_name('boundry', map_data)

        for boundry in boundries:
            x, y, gid = boundry
            image = self.__get_image_by_gid(gid, map_data)
            if image:
                self.boundries.append((x * TILESIZE, y * TILESIZE))

    def __get_layer_by_name(self, name: str, map_data: pytmx.TiledMap):
        return map_data.layernames[name]

    def __get_image_by_gid(self, gid, map_data):
        return map_data.get_tile_image_by_gid(gid)

    def __get_props_by_gid(self, map_data):
        pass