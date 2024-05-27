from settings import TILESIZE
import pygame
from pygame.image import load
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle, Sprite
from pygame.math import Vector2
from debug import Debug

class Player(Sprite):
    def __init__(self, pos: tuple[int, int], group: [Group, GroupSingle], obstacle):
        super().__init__(group)
        self.image: Surface = pygame.transform.scale(
            load('graphics/test/player.png').convert_alpha(),
            (TILESIZE, TILESIZE)
        )
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        self.direction: Vector2 = Vector2(0, 0)
        self.speed: float = 5.0

        self.obstacle_sprites = obstacle

        self.debug = Debug()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y =  1
        else:
            self.direction.y = 0


    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.hitbox.x += (self.direction.x * self.speed)
            self.obstacle_collision('h')
            self.hitbox.y += (self.direction.y * self.speed)
            self.obstacle_collision('v')
            self.rect.center = self.hitbox.center

    def update(self):
        self.get_input()
        self.move()

    def obstacle_collision(self, d):
        for obstacle in self.obstacle_sprites.sprites():
            if d == 'v':
                self.obstacle_collision_vrt(obstacle)

            if d == 'h':
                self.obstacle_collision_hrz(obstacle)
    
    def obstacle_collision_vrt(self, obstacle: Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.y > 0:  # Moving down
                self.hitbox.bottom = obstacle.hitbox.top
            elif self.direction.y < 0:  # Moving up
                self.hitbox.top = obstacle.hitbox.bottom

    def obstacle_collision_hrz(self, obstacle:Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.x > 0:  # Moving right
                self.hitbox.right = obstacle.hitbox.left
            elif self.direction.x < 0:  # Moving left
                self.hitbox.left = obstacle.hitbox.right