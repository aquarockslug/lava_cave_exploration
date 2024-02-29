import sys
from dataclasses import dataclass
import pygame

@dataclass
class ColorsData:
    menu = (154, 166, 177)
    victory = (255, 0, 0)
    player = (249, 26, 142)
    path = (98, 21, 36)
    path_cool = (86, 93, 94)


@dataclass
class GameData:
    fps: int = 30 
    clock: pygame.time.Clock = pygame.time.Clock()
    colors = ColorsData()
    size: tuple = (1079, 1080)
    middle: tuple = (size[-1] / 2, size[1] / 2)
    screen: pygame.Surface = pygame.display.set_mode([size[-1], size[1]])
    font = "monospace"

if __name__ == "__main__":
    pygame.init()
    from lavagame import LavaGame
    LavaGame(GameData()).play()
    pygame.quit()
    sys.exit()
