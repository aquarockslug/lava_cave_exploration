import random
import sys
from dataclasses import dataclass

import pygame

from sprites import * 

@dataclass
class ColorsData:
    menu = (155, 166, 177)
    bg = (255, 127, 0)
    player = (250, 26, 142)
    path = (87, 93, 94)


@dataclass
class GameData:
    fps: int = 30 
    clock: pygame.time.Clock = pygame.time.Clock()
    colors = ColorsData()
    size: tuple = (1080, 1080)
    middle: tuple = (size[0] / 2, size[1] / 2)
    screen: pygame.Surface = pygame.display.set_mode([size[0], size[1]])
    font = None


class LavaGame:
    player_group, enemy_group, path_group = (
        pygame.sprite.Group(),
        pygame.sprite.Group(),
        pygame.sprite.Group(),
    )
    paths = []

    def __init__(self):
        self.data = load_game_data(GameData())
        self.data.font = pygame.font.SysFont("monospace", 42)
        self.player: Player = Player(
            [self.data.middle[0], self.data.middle[1]], [20, 20]
        )

        self.player_group.add(self.player)
        self.health_display = self.data.font.render("100", 1, (255, 255, 255))

        self.create_map(10)

    def play(self):
        playing = True
        while playing:
            self.render()
            if self.player.health <= 0:
                playing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
        sys.exit()

    def render(self):
        self.data.screen.fill(self.data.colors.bg)
        self.player.movement_handler(self.path_group, self.paths)
        self.update_collision()
        if self.player.burning:
            self.player.take_burn_damage()

        for path in self.paths:
            path.draw_borders()

        self.path_group.draw(self.data.screen)
        self.player_group.draw(self.data.screen)
        
        self.update_display()
        pygame.display.update()
        self.data.clock.tick(self.data.fps)

    def update_collision(self):
        player = self.player

        if pygame.sprite.spritecollide(player, self.path_group, False):
            player.image.fill(self.data.colors.player)
            player.burning = False
        else:
            player.burning = True

    def update_display(self):
        self.health_display = self.data.font.render(
            str(self.player.health), 1, (255, 255, 0)
        )
        self.data.screen.blit(self.health_display, (50, 50))

    def create_map(self, size):
        middle = self.data.middle
        self.create_island(middle)
        self.create_path(middle)
        for path in self.paths:
            if len(self.paths) >= size:
                break
            for _ in range(0, random.randint(1, 2)):
                self.create_path(path.destination)

    def create_path(self, pos):
        new_path_angle = random.choice([[0, 1], [3, 1], [-3, 1]])
        if new_path_angle == [0, 1]:
            new_length = 40
        else:
            new_length = random.choice([20, 40])

        new_path = Path(pos, [512, 512], new_length, new_path_angle)
        for section in new_path.sections:
            self.path_group.add(section)
        self.paths.append(new_path)

    def create_island(self, pos):
        # self.path_group.add(new_island)
        pass

if __name__ == "__main__":
    pygame.init()
    LavaGame().play()
