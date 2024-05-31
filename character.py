import pygame
from pygame.sprite import Sprite


class Character(Sprite):
    def __init__(self, groups):
        super().__init__(groups)

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.hitbox.x += self.direction.x * self.speed
            self.handle_obstacle_collision("h")
            self.hitbox.y += self.direction.y * self.speed
            self.handle_obstacle_collision("v")
            self.rect.center = self.hitbox.center

    def handle_obstacle_collision(self, direction: str):
        for obstacle in self.obstacle_sprites.sprites():
            if direction == "v":
                self.obstacle_collision_v(obstacle)
            if direction == "h":
                self.obstacle_collision_h(obstacle)

    def obstacle_collision_v(self, obstacle: Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.y > 0:
                self.hitbox.bottom = obstacle.hitbox.top
            elif self.direction.y < 0:
                self.hitbox.top = obstacle.hitbox.bottom

    def obstacle_collision_h(self, obstacle: Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.x > 0:
                self.hitbox.right = obstacle.hitbox.left
            elif self.direction.x < 0:
                self.hitbox.left = obstacle.hitbox.right
