import pygame


class Upgrade:
    def __init__(self, player, viewwindow: pygame.Surface):
        self.viewwindow = viewwindow
        self.player = player

    def display(self):
        self.viewwindow.fill((0, 0, 0, 150))
