from settings import TILESIZE, ATTACK_DELAY
import pygame
from pygame.image import load
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle, Sprite
from pygame.math import Vector2
from frameloader import load_frames
from debug import Debug

class Player(Sprite):
    STATS = {'health': 100, 'energy': 60, 'attack': 10, 'magic': '4', 'speed': 5}
    def __init__(self, pos: tuple[int, int], group: [Group, GroupSingle], obstacle, weapon_creator, weapon_hider):
        super().__init__(group)
        self.image: Surface = pygame.transform.scale(
            load('graphics/test/player.png').convert_alpha(),
            (TILESIZE, TILESIZE)
        )
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        self.direction: Vector2 = Vector2(0, 0)


        self.speed  = Player.STATS['speed']
        self.health = Player.STATS['health']
        self.energy = Player.STATS['energy'] 
        self.magic  = Player.STATS['magic']

        self.attack_delay = ATTACK_DELAY
        self.attack_time = pygame.time.get_ticks()
        self.attacking = False
        self.create_attack = weapon_creator
        self.hide_weapon = weapon_hider

        #animation
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.2
        self.animations  = {
            "right_idle": load_frames('graphics/player/right_idle/'),
            "left_idle": load_frames("graphics/player/left_idle/"),
            "up_idle": load_frames("graphics/player/up_idle/"),
            "down_idle": load_frames("graphics/player/down_idle/"),

            'right_attack': load_frames('graphics/player/right_attack/'),
            'left_attack': load_frames('graphics/player/left_attack/'),
            'up_attack': load_frames('graphics/player/up_attack/'),
            'down_attack': load_frames('graphics/player/down_attack/'),
     
            'down': load_frames('graphics/player/down/'),
            'up': load_frames('graphics/player/up/'),
            'left': load_frames('graphics/player/left/'),
            'right': load_frames('graphics/player/right/')
        }

        self.obstacle_sprites = obstacle

    def get_input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y =  1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.create_attack()
        
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction = self.direction * 0
            if not 'attack' in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        elif 'attack' in self.status:
            self.status = self.status.replace('_attack', '_idle')

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.hitbox.x += (self.direction.x * self.speed)
            self.obstacle_collision('h')
            self.hitbox.y += (self.direction.y * self.speed)
            self.obstacle_collision('v')
            self.rect.center = self.hitbox.center

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.get_input()
        self.move()
        self.cooldown()
        self.get_status()
        self.animate()

    def obstacle_collision(self, d):
        for obstacle in self.obstacle_sprites.sprites():
            if d == 'v':
                self.obstacle_collision_vrt(obstacle)

            if d == 'h':
                self.obstacle_collision_hrz(obstacle)
    
    def obstacle_collision_vrt(self, obstacle: Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.y > 0:
                self.hitbox.bottom = obstacle.hitbox.top
            elif self.direction.y < 0:
                self.hitbox.top = obstacle.hitbox.bottom

    def obstacle_collision_hrz(self, obstacle:Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.x > 0:
                self.hitbox.right = obstacle.hitbox.left
            elif self.direction.x < 0:
                self.hitbox.left = obstacle.hitbox.right
    
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.attack_time) >= self.attack_delay:
                self.attack_time = current_time
                self.attacking = False
                self.hide_weapon()