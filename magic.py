import pygame
from pygame.math import Vector2
from frameloader import load_frames
from player import Player

class Magic(pygame.sprite.Sprite):
    MAX_TRAVEL_DISTANCE = 400
    def __init__(self, entity: dict, player: Player, groups: list[pygame.sprite.Group]):
        super().__init__(groups)

        direction = player.status.split('_')[0]
        action_map = {
            'left': (-1, 0.5),
            'right': (1, 0.5),
            'up': (0, -1),
            'down': (0, 1)
        }
        self.speed = 8
        self.direction = Vector2(action_map[direction])
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = pygame.image.load(entity['image']).convert_alpha()
        self.frames = load_frames(entity['frames'])

        dirx, diry = action_map[direction]
        pos_x = player.rect.centerx + dirx * self.image.get_width() // 2
        pos_y = player.rect.centery + diry * self.image.get_height() // 2
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.hitbox = self.rect.inflate(-20, -20)
        self.traveled_distance = 0
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        self.animate()
        self.hitbox.x += int(self.direction.x) * self.speed
        self.hitbox.y += int(self.direction.y) * self.speed
        self.traveled_distance += self.speed

        self.rect.center = self.hitbox.center
    