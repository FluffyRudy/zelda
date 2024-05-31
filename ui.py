from settings import (
    FONT_SIZE,
    HEALTH_BAR_WIDTH,
    HEALTH_BAR_HEIGHT,
    ENERGY_BAR_WIDTH,
    ENERGY_BAR_HEIGHT,
    ITEM_BOX_SIZE,
    HEALTH_COLOR,
    ENERGY_COLOR,
    LOWER_LAYER_COLOR
)
import pygame

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()

        self.offset_x = 10
        self.offset_y = 10

        self.set_current_health = player.get_current_health
        self.set_current_energy = player.get_current_energy
        self.weapon_image = player.weapon
        self.weapon_pos = (
            ITEM_BOX_SIZE//2 - self.weapon_image.get_width()//2, 
            ITEM_BOX_SIZE//2 - self.weapon_image.get_height()//2
        )
        self.font = pygame.font.Font('graphics/font/joystix.ttf', FONT_SIZE)

        self.health_bar_rect = pygame.Rect(self.offset_x, self.offset_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(self.offset_x, self.offset_y * 3, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT)
        
        self.lower_health_layer_rect = self.health_bar_rect.copy()
        self.lower_energy_layer_rect = self.energy_bar_rect.copy()
        
        self.item_box_surface = pygame.Surface((ITEM_BOX_SIZE, ITEM_BOX_SIZE), pygame.SRCALPHA)
        self.item_box_surface.fill((50, 91, 103, 150))
        self.item_box_pos_y = self.display_surface.get_height() - ITEM_BOX_SIZE

    def selection_box(self, left, top):
        self.display_surface.blit(self.item_box_surface, (left, top))
    
    def weapon_overlay(self):
        self.selection_box(0, self.item_box_pos_y)
        self.item_box_surface.blit(self.weapon_image, self.weapon_pos)
        

    def display(self):
        pygame.draw.rect(self.display_surface, LOWER_LAYER_COLOR, self.lower_health_layer_rect, 0, 3)
        pygame.draw.rect(self.display_surface, LOWER_LAYER_COLOR, self.lower_energy_layer_rect, 0, 3)
        pygame.draw.rect(self.display_surface, HEALTH_COLOR, self.health_bar_rect, 0, 3)
        pygame.draw.rect(self.display_surface, ENERGY_COLOR, self.energy_bar_rect, 0, 3)
        self.health_bar_rect.width = self.set_current_health()
        self.energy_bar_rect.width = self.set_current_energy()
        self.weapon_overlay()