from typing import Union
from settings import *
import pygame
from pygame.image import load
from pygame import Surface
from pygame import Rect
from pygame.sprite import Group, GroupSingle, Sprite
from pygame.math import Vector2
from frameloader import load_frames
from debug import Debug

class Player(Sprite):
    STATS = {'health': HEALTH_BAR_WIDTH, 'energy': ENERGY_BAR_WIDTH, 'attack': SPEED, 'magic': '4', 'speed': SPEED}

    def __init__(self, 
                 pos: tuple[int, int], 
                 group: Union[Group, GroupSingle], 
                 obstacle: Group, 
                 weapon_creator, 
                 weapon_hider,
                 magic_creator,
                 magic_destroyer,
                 magic_obstacle_handler):
        #attributes
        super().__init__(group)
        self.image: Surface = pygame.transform.scale(
            load('graphics/test/player.png').convert_alpha(),
            (TILESIZE, TILESIZE)
        )
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        self.direction: Vector2 = Vector2(0, 0)

        self.speed  = Player.STATS['speed']
        self.health = Player.STATS['health'] * 0.5
        self.energy = Player.STATS['energy']

        self.attack_delay = ATTACK_DELAY
        self.attack_time = 0
        self.attacking = False
        self.create_attack = weapon_creator
        self.hide_weapon = weapon_hider
        self.weapon = pygame.image.load('graphics/weapons/sword/up.png')

        #magic and magic
        self.change_to_idle = False
        self.magic_exist_delay = 800 
        self.magic_attacking = False
        self.magic_attack_time = 0
        self.destroy_magic = magic_destroyer
        self.create_magic = magic_creator
        self.handle_magic_obstacle_collision = magic_obstacle_handler
        self.magic_index = 0
        self.magic_list = list(magic_data.keys()) 
        self.magic = self.magic_list[self.magic_index]
        self.magic_image = pygame.image.load(magic_data[self.magic]['image'])
        self.can_switch_magic = True

        #player animation
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
                self.attack_time = pygame.time.get_ticks()
                self.attacking = True
                self.create_attack()
            
            if keys[pygame.K_RETURN] and not self.magic_attacking:
                magic_cost = magic_data[self.magic]['cost']
                self.magic_attack_time = pygame.time.get_ticks()
                self.magic_attacking = True
                self.create_magic(magic_data[self.magic])
                self.update_energy(-magic_cost)

        if keys[pygame.K_LCTRL] and self.can_switch_magic:
            self.magic_index += 1
            self.magic = self.magic_list[self.magic_index % len(self.magic_list)]
            self.magic_image = pygame.image.load(magic_data[self.magic]['image'])
            self.can_switch_magic = False
        
        if not keys[pygame.K_LCTRL] and not self.can_switch_magic:
            self.can_switch_magic = True

    def update_energy(self, amount: int):
        self.energy += amount
        if self.energy > ENERGY_BAR_WIDTH:
            self.energy = ENERGY_BAR_WIDTH
        elif self.energy < 0:
            self.energy = 0
    
    def update_health(self, amount: int):
        self.health += amount
        if self.health > HEALTH_BAR_WIDTH:
            self.health = HEALTH_BAR_WIDTH
        elif self.health < 0:
            self.health = 0

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction = self.direction * 0
            if 'attack' not in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        elif 'attack' in self.status:
            self.status = self.status.replace('_attack', '_idle')
        
        if self.magic_attacking and not self.change_to_idle:
            if 'attack' not in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        elif self.change_to_idle:
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

    def get_current_health(self):
        return (self.health / self.STATS['health']) * 100

    def get_current_energy(self):
        return (self.energy / self.STATS['energy']) * 100

    def get_current_magic(self):
        return self.magic_image
    
    def get_current_weapon(self):
        return self.weapon

    def update(self):
        self.get_input()
        self.move()
        self.cooldown()
        self.get_status()
        self.animate()
        self.handle_magic_obstacle_collision()

    def obstacle_collision(self, direction: str):
        for obstacle in self.obstacle_sprites.sprites():
            if direction == 'v':
                self.obstacle_collision_vrt(obstacle)
            if direction == 'h':
                self.obstacle_collision_hrz(obstacle)
    
    def obstacle_collision_vrt(self, obstacle: Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.y > 0:
                self.hitbox.bottom = obstacle.hitbox.top
            elif self.direction.y < 0:
                self.hitbox.top = obstacle.hitbox.bottom

    def obstacle_collision_hrz(self, obstacle: Sprite):
        if self.hitbox.colliderect(obstacle.hitbox):
            if self.direction.x > 0:
                self.hitbox.right = obstacle.hitbox.left
            elif self.direction.x < 0:
                self.hitbox.left = obstacle.hitbox.right
    
    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.attack_time) >= self.attack_delay:
                self.attacking = False
                self.hide_weapon()

        magic_time_diff = (current_time - self.magic_attack_time)
        if magic_time_diff >= self.magic_exist_delay:
            self.magic_attacking = False
            self.change_to_idle = False
            self.destroy_magic()
        elif magic_time_diff >= self.magic_exist_delay // 4:
            self.change_to_idle = True