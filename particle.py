import pygame
from os.path import join
from os import listdir
from random import shuffle
from frameloader import load_frames
from typing import Iterable, Optional, TYPE_CHECKING
from settings import PROJECT_DIR


if TYPE_CHECKING:
    from particle import Particle


class Particle(pygame.sprite.Sprite):
    current_instance: Optional["Particle"] = None

    sound_map = {
        "flame": "audio/Fire.wav",
        "heal": "audio/heal.wav",
        "leaf_attack": "audio/attack/slash.wav",
        "slash": "audio/attack/slash.wav",
        "claw": "audio/attack/claw.wav",
        "thunder": "audio/attack/fireball.wav",
    }

    def __init__(
        self,
        pos: tuple[int, int],
        particle_type: str,
        groups: Iterable[pygame.sprite.Group],
        flip_x=False,
        is_dynamic=False,
        kill_time: Optional[float] = None,  # in ms
    ):
        super().__init__(groups)

        base_path = join(PROJECT_DIR, "graphics/particles/")

        self.frames = load_frames(join(base_path, particle_type), flip_x)

        self.image = self.frames[2]
        self.rect = self.image.get_rect(center=pos)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.time_controlled = kill_time is not None
        if self.time_controlled:
            self.kill_timer = pygame.time.get_ticks()
            self.kill_time = kill_time

        self.is_dynamic = is_dynamic
        self._type = particle_type.split("/")[0]
        self.mask = pygame.mask.from_surface(self.image)

        if not self._type in (
            "smoke_orange",
            "aura",
            *tuple(f"leaf{i}" for i in range(1, 6 + 1)),
        ):
            self.sound = pygame.mixer.Sound(
                join(PROJECT_DIR, self.sound_map[self._type])
            )
            self.sound.set_volume(1.0)

        self.set_instance(self)

    @classmethod
    def set_instance(cls, instance: "Particle"):
        cls.current_instance = instance

    @classmethod
    def clear_instance(cls):
        cls.current_instance = None

    @classmethod
    def play_sound(cls):
        if cls.current_instance is not None and hasattr(cls.current_instance, "sound"):
            cls.current_instance.sound.play(fade_ms=1000)

    def update(self):
        if self.time_controlled:
            self.timer_animation()
        else:
            self.animate()
        Particle.play_sound()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def timer_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        current_time = pygame.time.get_ticks()
        if current_time - self.kill_timer >= self.kill_time:
            self.kill()
            self.clear_instance()

    def update_position(self, new_pos: pygame.Rect):
        if self.is_dynamic:
            self.rect.center = new_pos.center


def grass_destruction_particle(pos: tuple[int, int], groups: list[pygame.sprite.Group]):
    leaf_types = [f"leaf{i}" for i in range(1, 6 + 1)]
    shuffle(leaf_types)

    for idx, leaf_type in enumerate(leaf_types):
        grass_type = leaf_type
        flip = idx % 2 == 0
        Particle(pos, grass_type, groups, flip)
