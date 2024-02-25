import random
import sys
from dataclasses import dataclass
import pygame

from sprites import *

@dataclass
class ColorsData:
    menu = (155, 166, 177)
    bg = (20, 20, 20)
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
    player_group, enemy_group, path_group, world_group = (
        pygame.sprite.Group(),
        pygame.sprite.Group(),
        pygame.sprite.Group(),
        pygame.sprite.Group(),
    )
    paths = []
    world = pygame.sprite.Sprite

    def __init__(self):
        self.data = load_game_data(GameData())
        self.data.font = pygame.font.SysFont("monospace", 42)
        self.player: Player = Player(self.data.middle, [50, 50])

        self.player_group.add(self.player)
        self.health_display = self.data.font.render("100", 1, (255, 255, 255))
        world_size = [10000, 10000]
        world_pos = [world_size[0] / 2, world_size[1] / 2]

        self.world = Sprite(world_pos, world_size, self.data.colors.bg)
        self.world_group.add(self.world)
        self.generate_world(50)

    def tile_surface(self, surface, image, tile_size):
        tile = pygame.transform.scale(image, [tile_size, tile_size])
        for row in range(0, int(surface.get_height() / tile_size)):
            for col in range(0, int(surface.get_width() / tile_size)):
                surface.blit(tile, [col * tile_size, row * tile_size])
            

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
        key = pygame.key.get_pressed()
        self.data.screen.fill(self.data.colors.bg)
        self.world_group.draw(self.data.screen)
        self.player.movement_handler(key, self.path_group, self.world_group)
        self.player.update_direction(key)
        self.update_collision()
        if self.player.burning:
            self.player.take_burn_damage()

        # self.path_group.draw(self.data.screen)
        self.player_group.draw(self.data.screen)

        self.update_display()
        pygame.display.update()
        self.data.clock.tick(self.data.fps)

    def update_collision(self):
        player = self.player

        if pygame.sprite.spritecollide(player, self.path_group, False):
            player.burning = False
        else:
            player.burning = True

    def update_display(self):
        self.health_display = self.data.font.render(
            str(self.player.health), 1, (0, 0, 0)
        )
        self.data.screen.blit(self.health_display, (50, 50))

    def generate_world(self, size):
        self.tile_surface(self.world.image, pygame.image.load("assets/fire.png"), 64)
                
        def generate_path():
            self.create_path(path.destination, 200)
            self.create_island(path.destination, 250)
            if not random.randrange(0, 2):
                self.create_path(path.destination, 100)
                self.create_island(path.destination, 400)

        # add paths until size limit is reached
        self.create_island(self.data.middle, 400)
        self.create_path(self.data.middle, 200)
        for path in self.paths:
            generate_path()
            if len(self.paths) >= size:
                break 

        for path in self.paths:
            path.draw_path(self.world)
        
    def create_path(self, pos, thickness):
        new_path_angle = random.choice([[0, 1], [1, 1], [1, 0]])
        new_thickness = int(thickness*sqrt(2)) if new_path_angle == [1, 1] else thickness
        new_length = random.choice([30, 60])
        if 0 in new_path_angle:
            new_length *= 2

        new_path = Path(pos, new_thickness, new_length, new_path_angle)
        for section in new_path.sections:
            self.path_group.add(section)
        self.paths.append(new_path)

    def create_island(self, pos, size):
        new_island = Island(pos, size)
        self.path_group.add(new_island)
        self.world.image.blit(new_island.image, [pos[0] - size / 2, pos[1] - size / 2])


if __name__ == "__main__":
    pygame.init()
    LavaGame().play()
