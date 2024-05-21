from typing import Optional
import sys
from settings import WIDTH, HEIGHT,TILESIZE, FPS
import pygame



class Game:
    BLACK = pygame.Color(0, 0, 0, 255)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
    
    def handle_event(self) -> Optional[None]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def run(self) -> None:
        while True:
            self.handle_event()
            self.screen.fill(self.BLACK)
            pygame.display.update()
            self.clock.tick(FPS)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()