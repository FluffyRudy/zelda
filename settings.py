import os

PROJECT_DIR = os.path.dirname(__file__)

WIDTH = 1100
HEIGHT = 720
TILESIZE = 64
FPS = 60
ATTACK_DELAY = 500
FONT_SIZE = 25
HEALTH_BAR_WIDTH = 100
HEALTH_BAR_HEIGHT = 10
ENERGY_BAR_WIDTH = 100
ENERGY_BAR_HEIGHT = 10
ITEM_BOX_SIZE = 100
SPEED = 5
DAMAGE = 10
LOWER_LAYER_COLOR = (58, 0, 59)
HEALTH_COLOR = (255, 102, 0)
ENERGY_COLOR = (0, 126, 255)
EXP = 0
UPGRADE_BOX_SIZE = 150, HEIGHT - 200
GEAR_SIZE = (50, 25)

magic_data = {
    "flame": {
        "type": "flame",
        "strength": 20,
        "burn_strength": 5,
        "cost": 20,
        "image": os.path.join(PROJECT_DIR, "graphics/particles/flame/fire.png"),
        "frames": os.path.join(PROJECT_DIR, "graphics/particles/flame/frames/"),
    },
    "heal": {
        "type": "heal",
        "strength": 20,
        "cost": 10,
        "image": os.path.join(PROJECT_DIR, "graphics/particles/heal/heal.png"),
        "frames": os.path.join(PROJECT_DIR, "graphics/particles/heal/frames/"),
    },
}

monster_data = {
    "squid": {
        "health": 100,
        "exp": 100,
        "damage": 20,
        "attack_type": "slash",
        "attack_sound": os.path.join(PROJECT_DIR, "graphics/audio/attack/slash.wav"),
        "speed": 3,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "raccoon": {
        "health": 300,
        "exp": 250,
        "damage": 40,
        "attack_type": "claw",
        "attack_sound": os.path.join(PROJECT_DIR, "graphics/audio/attack/claw.wav"),
        "speed": 2,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "spirit": {
        "health": 100,
        "exp": 110,
        "damage": 8,
        "attack_type": "thunder",
        "attack_sound": os.path.join(PROJECT_DIR, "graphics/audio/attack/fireball.wav"),
        "speed": 4,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 350,
    },
    "bamboo": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "leaf_attack",
        "attack_sound": os.path.join(PROJECT_DIR, "graphics/audio/attack/slash.wav"),
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
