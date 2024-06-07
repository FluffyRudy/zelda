from typing import Union
from collections import OrderedDict
from settings import *
import pygame
from pygame.image import load
from pygame import Surface, Rect
from pygame.sprite import Group, GroupSingle, Sprite
from pygame.math import Vector2
from character import Character
from frameloader import load_frames


class Player(Character):
    STATS = OrderedDict(
        {
            "health": {
                "amount": HEALTH_BAR_WIDTH,
                "cost": 100,
                "max_value": 300,
                "increment": 50,
            },
            "energy": {
                "amount": ENERGY_BAR_WIDTH,
                "cost": 100,
                "max_value": 300,
                "increment": 50,
            },
            "flame": {
                "amount": magic_data["flame"]["strength"],
                "cost": 200,
                "max_value": 50,
                "increment": 10,
            },
            "heal": {
                "amount": magic_data["heal"]["strength"],
                "cost": 200,
                "max_value": 50,
                "increment": 10,
            },
            "attack": {"amount": 20, "cost": 150, "max_value": 40, "increment": 10},
            "speed": {"amount": SPEED, "cost": 150, "max_value": 8, "increment": 2},
        }
    )

    def __init__(
        self,
        pos: tuple[int, int],
        group: Union[Group, GroupSingle],
        obstacle: Group,
        weapon_creator,
        weapon_hider,
        magic_creator,
        magic_destroyer,
        magic_obstacle_handler,
    ):
        super().__init__(group)
        self.image: Surface = pygame.transform.scale(
            load(os.path.join(PROJECT_DIR, "graphics/test/player.png")).convert_alpha(),
            (TILESIZE, TILESIZE),
        )
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        # Initializing player attributes
        self.speed = Player.STATS["speed"]["amount"]
        self.health = Player.STATS["health"]["amount"]
        self.energy = Player.STATS["energy"]["amount"]
        self.exp = EXP
        self.obstacle_sprites = obstacle

        self.invincible_duration = 1000

        self.weapon_handler = WeaponHandler(weapon_creator, weapon_hider)
        self.magic_handler = MagicHandler(
            magic_creator, magic_destroyer, magic_obstacle_handler, self
        )
        self.animation_handler = AnimationHandler(self)

    def update(self):
        self.get_input()
        self.move()
        self.weapon_handler.cooldown()
        self.magic_handler.cooldown()
        self.animation_handler.update_status()
        self.animation_handler.animate()
        self.magic_handler.handle_obstacle_collision(self.obstacle_sprites)
        self.handle_vulnerability()

    def update_energy(self, amount: int):
        self.energy += amount
        if self.energy > self.STATS["energy"]["amount"]:
            self.energy = self.STATS["energy"]["amount"]
        elif self.energy < 0:
            self.energy = 0

    def update_health(self, amount: int):
        self.health += amount

        if self.health > self.STATS["health"]["amount"]:
            self.health = self.STATS["health"]["amount"]
        elif self.health < 0:
            self.health = 0

    def update_attribute(self, stat_name: str, update_value: int):
        if stat_name in self.STATS:
            stat = self.STATS[stat_name]
            new_amount = stat["amount"] + update_value
            if new_amount > stat["max_value"]:
                new_amount = stat["max_value"]

            stat["amount"] = new_amount

            if stat_name == "speed":
                self.speed = new_amount

            if stat_name == "health":
                self.update_health(new_amount - self.health)
            elif stat_name == "energy":
                self.update_energy(new_amount - self.energy)
            stat["cost"] += stat["cost"]

    def get_stat_by_index(self, index: int):
        key = list(self.STATS.keys())[index]
        return {"attr": key, "value": self.STATS[key]}

    def get_current_health(self):
        return (self.health / self.STATS["health"]["amount"]) * self.STATS["health"][
            "amount"
        ]

    def get_current_energy(self):
        return (self.energy / self.STATS["energy"]["amount"]) * self.STATS["energy"][
            "amount"
        ]

    def update_exp(self, exp: int):
        self.exp += exp

    def get_current_exp(self):
        return self.exp

    def get_current_status(self):
        return self.animation_handler.status

    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.weapon_handler.attacking:
            self.handle_movement_input(keys)
            self.handle_attack_input(keys)
            self.handle_magic_input(keys)
            self.handle_magic_switching(keys)

    def handle_movement_input(self, keys):
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.animation_handler.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.animation_handler.status = "left"
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.animation_handler.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.animation_handler.status = "down"
        else:
            self.direction.y = 0

    def handle_attack_input(self, keys):
        if keys[pygame.K_SPACE]:
            self.weapon_handler.attack()

    def handle_magic_input(self, keys):
        if keys[pygame.K_RETURN] and not self.magic_handler.magic_attacking:
            self.magic_handler.attack(magic_data[self.magic_handler.magic])

    def handle_magic_switching(self, keys):
        if keys[pygame.K_LCTRL]:
            if self.magic_handler.can_switch_magic:
                self.magic_handler.switch_magic()
                self.magic_handler.can_switch_magic = False
        else:
            self.magic_handler.can_switch_magic = True

    def handle_vulnerability(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable:
            if current_time - self.invincibility_timer >= self.invincible_duration:
                self.vulnerable = True
            self.image.set_alpha(self.normalized_sine())
        elif self.image.get_alpha() != 255:
            self.image.set_alpha(255)


class WeaponHandler:
    def __init__(self, weapon_creator, weapon_hider):
        self.attacking = False
        self.attack_time = 0
        self.attack_delay = ATTACK_DELAY
        self.create_attack = weapon_creator
        self.hide_weapon = weapon_hider
        self.weapon = pygame.image.load(
            os.path.join(PROJECT_DIR, "graphics/weapons/sword/up.png")
        )

    def attack(self):
        self.attack_time = pygame.time.get_ticks()
        self.attacking = True
        self.create_attack()

    def get_current_weapon(self):
        return self.weapon

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.attack_time) >= self.attack_delay:
            self.attacking = False
            self.hide_weapon()


class MagicHandler:
    def __init__(
        self,
        magic_creator,
        magic_destroyer,
        magic_obstacle_handler,
        player,
    ):
        self.player = player
        self.magic_attacking = False
        self.magic_attack_time = 0
        self.magic_exist_delay = 800
        self.create_magic = magic_creator
        self.destroy_magic = magic_destroyer
        self.handle_magic_obstacle_collision = magic_obstacle_handler
        self.magic_index = 0
        self.magic_list = list(magic_data.keys())
        self.magic = self.magic_list[self.magic_index]
        self.magic_image = pygame.image.load(magic_data[self.magic]["image"])
        self.can_switch_magic = True
        self.change_to_idle = False
        self.immidate_kill = False

    def attack(self, magic_entity):
        magic_cost = magic_data[self.magic]["cost"]
        self.magic_attack_time = pygame.time.get_ticks()
        self.magic_attacking = True
        self.create_magic(magic_entity)
        self.player.update_energy(-magic_cost)

    def switch_magic(self):
        self.magic_index += 1
        self.magic = self.magic_list[self.magic_index % len(self.magic_list)]
        self.magic_image = pygame.image.load(magic_data[self.magic]["image"])
        self.can_switch_magic = False

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        magic_time_diff = current_time - self.magic_attack_time
        if magic_time_diff >= self.magic_exist_delay:
            self.magic_attacking = False
            self.change_to_idle = False
            self.destroy_magic()
        elif magic_time_diff >= self.magic_exist_delay // 4:
            self.change_to_idle = True

    def handle_obstacle_collision(self, obstacle_sprites):
        self.handle_magic_obstacle_collision()

    def get_current_magic(self):
        return self.magic_image


class AnimationHandler:
    def __init__(self, player):
        self.player = player
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.2
        self.animations = {
            "right_idle": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/right_idle/")
            ),
            "left_idle": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/left_idle/")
            ),
            "up_idle": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/up_idle/")
            ),
            "down_idle": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/down_idle/")
            ),
            "right_attack": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/right_attack/")
            ),
            "left_attack": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/left_attack/")
            ),
            "up_attack": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/up_attack/")
            ),
            "down_attack": load_frames(
                os.path.join(PROJECT_DIR, "graphics/player/down_attack/")
            ),
            "down": load_frames(os.path.join(PROJECT_DIR, "graphics/player/down/")),
            "up": load_frames(os.path.join(PROJECT_DIR, "graphics/player/up/")),
            "left": load_frames(os.path.join(PROJECT_DIR, "graphics/player/left/")),
            "right": load_frames(os.path.join(PROJECT_DIR, "graphics/player/right/")),
        }

    def update_status(self):
        if self.player.direction.x == 0 and self.player.direction.y == 0:
            if "idle" not in self.status and "attack" not in self.status:
                self.status = self.status + "_idle"
        if self.player.weapon_handler.attacking:
            self.player.direction = self.player.direction * 0
            if "attack" not in self.status:
                if "_idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        elif "attack" in self.status:
            self.status = self.status.replace("_attack", "_idle")

        if (
            self.player.magic_handler.magic_attacking
            and not self.player.magic_handler.change_to_idle
        ):
            if "attack" not in self.status:
                if "_idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status += "_attack"
        elif self.player.magic_handler.change_to_idle:
            self.status = self.status.replace("_attack", "_idle")

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.player.image = animation[int(self.frame_index)]
        self.player.rect = self.player.image.get_rect(center=self.player.hitbox.center)
