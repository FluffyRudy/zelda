from settings import TILESIZE, magic_data
import pygame
from pygame import Surface
from pygame.sprite import Group, GroupSingle, Sprite
from tile import Tile, Grass
from player import Player
from weapon import Weapon
from magic import Flame, Heal
from enemy import Enemy
from particle import Particle, grass_destruction_particle
from ui import UI
from tiledmaploader import TiledMapLoader
from debug import Debug


class Level:
    def __init__(self):
        self.display_surface: Surface = pygame.display.get_surface()

        self.map_data = TiledMapLoader("maps/tmx/map.tmx")

        self.visible_sprites: YSortCameraGroup = YSortCameraGroup(self.map_data)
        self.obstacle_sprites: Group = Group()
        self.attackable_sprites: Group = Group()
        self.particles_list = ParticleGroup()

        self.setup_level()
        Grass.set_particle_groups(
            {
                "visible_group": self.visible_sprites,
                "particle_group": self.particles_list,
            }
        )

        self.current_weapon = None
        self.current_magic = None

        self.ui = UI(self.player)

        self.debug = Debug()

    def create_magic_attack(self, magic_entity: dict):
        magic_type = magic_entity["type"]
        match magic_type:
            case "flame":
                self.current_magic = Flame(
                    magic_entity, self.player, [self.visible_sprites]
                )

            case "heal":
                self.current_magic = Heal(
                    magic_entity, self.player, [self.visible_sprites]
                )
        Particle(
            self.player.rect.midbottom,
            "aura",
            [self.visible_sprites, self.particles_list],
            is_dynamic=True,
        )

    def destroy_magic_attack(self):
        if self.current_magic is not None:
            centerx, centery = self.current_magic.rect.center
            match self.current_magic.type:
                case "flame":
                    for i in range(3):
                        pos_x = centerx + i * self.current_magic.image.get_width()
                        pos_y = centery
                        Particle(
                            (pos_x, pos_y),
                            "flame/frames",
                            [self.visible_sprites, self.particles_list],
                            is_dynamic=False,
                            kill_time=1500,
                        )
            self.current_magic.kill()
        self.current_magic = None

    def handle_magic_obstacle_collision(self):
        if self.current_magic is None or self.current_magic.type == "heal":
            return

        for obstacle in self.obstacle_sprites:
            if self.current_magic.rect.colliderect(obstacle.hitbox):
                if pygame.sprite.collide_mask(self.current_magic, obstacle):
                    self.destroy_magic_attack()
                    break

    def show_weapon(self):
        self.current_weapon = Weapon(self.player, [self.visible_sprites])

    def hide_weapon(self):
        if self.current_weapon is not None:
            self.current_weapon.kill()
        self.current_weapon = None

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.draw(relative_sprite=self.player)
        self.particles_list.update()
        self.particles_list.update_position(self.player.rect)
        self.particles_list.draw(self.display_surface)
        self.handle_enemy_getting_attacked()
        self.handle_particle_effect_collision()
        self.ui.display()

    def setup_level(self):
        self.player = Player(
            self.map_data.player_pos,
            [self.visible_sprites],
            self.obstacle_sprites,
            self.show_weapon,
            self.hide_weapon,
            self.create_magic_attack,
            self.destroy_magic_attack,
            self.handle_magic_obstacle_collision,
        )
        self._create_map_objects()

    def _create_map_objects(self):
        for pos_x, pos_y, _ in self.map_data.boundries:
            Tile((pos_x, pos_y), [self.obstacle_sprites])
        for pos_x, pos_y, image in self.map_data.grasses:
            Grass(
                (pos_x, pos_y),
                [self.obstacle_sprites, self.visible_sprites, self.attackable_sprites],
                image,
            )
        for pos_x, pos_y, image in self.map_data.trees:
            Tile((pos_x, pos_y), [self.obstacle_sprites, self.visible_sprites], image)
        for pos_x, pos_y, image in self.map_data.blocks:
            Tile((pos_x, pos_y), [self.obstacle_sprites, self.visible_sprites], image)
        for monster_type, pos_x, pos_y, image in self.map_data.enemies:
            Enemy(
                monster_type,
                (pos_x, pos_y),
                image,
                [self.visible_sprites, self.attackable_sprites],
                self.obstacle_sprites,
                self.player,
                self.handle_player_getting_attacked,
            )

    def handle_enemy_getting_attacked(self):
        for attack_type in [self.current_weapon, self.current_magic]:
            if attack_type is not None:
                for sprite in self.attackable_sprites:
                    if attack_type.rect.colliderect(sprite.hitbox):
                        if pygame.sprite.collide_mask(attack_type, sprite):
                            if isinstance(sprite, Grass):
                                self.player.update_exp(10)
                                center = sprite.hitbox.center
                                sprite.kill()
                                grass_destruction_particle(
                                    center,
                                    [self.visible_sprites, self.particles_list],
                                )
                            if attack_type == self.current_weapon:
                                self.hide_weapon()
                                sprite.get_damage(attack_type.damage)
                            else:
                                self.destroy_magic_attack()
                                sprite.get_damage(attack_type.strength)
                            break

    def handle_player_getting_attacked(self, damage: int, attack_type: str):
        if self.player.vulnerable:
            self.particles_list.add(
                Particle(
                    self.player.rect.center,
                    attack_type,
                    self.visible_sprites,
                    is_dynamic=True,
                )
            )
            self.player.health = max(self.player.health - damage, 0)
            self.player.vulnerable = False
            self.player.invincibility_timer = pygame.time.get_ticks()

    def handle_particle_effect_collision(self):
        collided_sprites = pygame.sprite.groupcollide(
            self.particles_list, self.attackable_sprites, False, False
        )
        for particle, enemy_list in collided_sprites.items():
            for enemy in enemy_list:
                if particle.rect.colliderect(enemy.hitbox):
                    if pygame.sprite.collide_mask(particle, enemy):
                        match particle._type:
                            case "flame":
                                enemy.get_damage(magic_data["flame"]["burn_strength"])


class YSortCameraGroup(Group):
    def __init__(self, map_data):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.screen_center_x = self.display_surface.get_width() // 2
        self.screen_center_y = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2(0, 0)

        self.floor = map_data.ground
        self.floor_rect = self.floor.get_rect(topleft=(0, 0))

        # Set the visibility bound to 100 to ensure sprites become visible when they are within 100 pixels off-screen.
        self.visibility_bound = 100

    def draw(self, relative_sprite: Sprite):
        self.offset.x = relative_sprite.rect.left - self.screen_center_x
        self.offset.y = relative_sprite.rect.top - self.screen_center_y

        self._draw_floor(self.offset)

        sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.y)
        for sprite in sorted_sprites:
            offset_rect = sprite.rect.topleft - self.offset
            if self._is_sprite_visible(offset_rect, sprite):
                self.display_surface.blit(sprite.image, offset_rect)
                if isinstance(sprite, Enemy):
                    pygame.draw.rect(
                        self.display_surface,
                        "red",
                        (*offset_rect, *sprite.hitbox.size),
                        5,
                    )

    def _draw_floor(self, offset: tuple):
        offset_rect = self.floor_rect.topleft - offset
        self.display_surface.blit(self.floor, offset_rect)

    def _is_sprite_visible(self, offset_rect, sprite):
        return (
            -self.visibility_bound <= offset_rect.x <= self.display_surface.get_width()
            and -self.visibility_bound
            <= offset_rect.y
            <= self.display_surface.get_height()
        )


class ParticleGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update_position(self, new_rect: pygame.Rect):
        for sprite in self.sprites():
            sprite.update_position(new_rect)
