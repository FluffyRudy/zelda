import pygame
import os


def load_frames(path: str):
    """
    load image frames for animation
    """
    if not os.path.exists(path):
        return []

    valid_extension = ".png"
    images = []

    for file in os.listdir(path):
        if os.path.splitext(file)[1] == valid_extension:
            full_relative_path = os.path.join(path, file)
            image = pygame.image.load(full_relative_path).convert_alpha()
            images.append(image)

    return images
