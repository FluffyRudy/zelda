WIDTH    = 1200
HEIGHT   = 720
TILESIZE = 64
FPS      = 60
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

magic_data = {
    'flame': {
        'type': 'flame',
        'strength': 5, 
        'cost': 20, 
        'image': 'graphics/particles/flame/fire.png',
        'frames': 'graphics/particles/flame/frames/'
    },
    'heal': {
        'type': 'heal',
        'strength': 20, 
        'cost': 10, 
        'image': 'graphics/particles/heal/heal.png',
        'frames': 'graphics/particles/heal/frames/'
    }
}