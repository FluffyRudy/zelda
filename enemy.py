import pygame
from settings import monster_data
from character import Character
from frameloader import load_frames
from os.path import join
from math import hypot, sin


class Enemy(Character):
    def __init__(
        self,
        monster_type: str,
        pos: tuple[int, int],
        image: pygame.Surface,
        groups: list[pygame.sprite.Group],
        obstacle_sprites: pygame.sprite.Group,
        relative_sprite: pygame.sprite.Sprite,
    ):
        super().__init__(groups)

        # Get monster_info from monster_data using monster_type
        monster_info: dict = monster_data[monster_type]

        self.monster_type = monster_type
        self.health = monster_info.get("health")
        self.exp = monster_info.get("exp")
        self.damage = monster_info.get("damage")
        self.attack_type = monster_info.get("attack_type")
        self.attack_sound = monster_info.get("attack_sound")
        self.speed = monster_info.get("speed")
        self.resistance = monster_info.get("resistance")
        self.attack_radius = monster_info.get("attack_radius")
        self.notice_radius = monster_info.get("notice_radius")

        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        self.obstacle_sprites = obstacle_sprites
        self.relative_sprite = relative_sprite

        self.can_attack = True
        self.attack_cooldown = 500
        self.attack_time = 0

        self.animation_handler = AnimationHandler(self, self.relative_sprite)

    def update(self):
        self.animation_handler.animate()
        self.animation_handler.get_status()
        self.animation_handler.attack_cooldown()
        self.move()
        self.actions()

    def actions(self):
        if self.animation_handler.status == "attack" and self.can_attack:
            self.attack_time = pygame.time.get_ticks()
        elif self.animation_handler.status == "move":
            direction = self.get_vector_from_relative_sprite()[1]
            if self.can_attack:
                self.direction.x = direction[0]
                self.direction.y = direction[1]
            else:
                self.direction.x = 0
                self.direction.y = 0
        else:
            self.direction.x = 0
            self.direction.y = 0

    def get_vector_from_relative_sprite(self):
        relative_rect: pygame.Rect = self.relative_sprite.rect
        x_dist = relative_rect.centerx - self.hitbox.centerx
        y_dist = relative_rect.centery - self.hitbox.centery
        magnitude = hypot(x_dist, y_dist)
        if magnitude > 0:
            directon = x_dist / magnitude, y_dist / magnitude
        else:
            directon = (0, 0)
        return (magnitude, directon)

    def get_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def normalized_sine(self):
        return int(127.5 * (sin(pygame.time.get_ticks()) + 1))


class AnimationHandler:
    def __init__(self, enemy_character: Enemy, relative_sprite: pygame.sprite.Sprite):
        self.status = "idle"
        self.enemy = enemy_character
        self.relative_sprite = relative_sprite

        self.frame_index = 0
        self.animation_speed = 0.08

        base_path = "graphics/monsters"
        monster_path = join(base_path, self.enemy.monster_type)

        self.animations = {
            "idle": load_frames(join(monster_path, "idle")),
            "attack": load_frames(join(monster_path, "attack")),
            "move": load_frames(join(monster_path, "move")),
        }

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.enemy.can_attack = False
            self.frame_index = 0

        self.enemy.image = animation[int(self.frame_index)]
        self.enemy.rect = self.enemy.image.get_rect(center=self.enemy.rect.center)

    def get_status(self):
        distance, direction = self.enemy.get_vector_from_relative_sprite()

        if distance <= self.enemy.attack_radius and self.enemy.can_attack:
            self.status = "attack"
        elif distance <= self.enemy.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def attack_cooldown(self):
        if not self.enemy.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.enemy.attack_time >= self.enemy.attack_cooldown:
                self.enemy.can_attack = True
