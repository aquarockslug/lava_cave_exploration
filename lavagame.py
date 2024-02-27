import random
import sys
from math import sqrt
import pygame

from paths import Path, Island
from player import Player


class Sprite(pygame.sprite.Sprite):
    rect = pygame.Rect
    image = pygame.Surface
    size = []

    def __init__(self, pos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.size = size


class LavaGame:
    player_group, enemy_group, path_group, world_group = (
        pygame.sprite.Group(),
        pygame.sprite.Group(),
        pygame.sprite.Group(),
        pygame.sprite.Group(),
    )
    paths = []
    world = pygame.sprite.Sprite

    def __init__(self, gamedata):
        self.data = gamedata 
        self.data.font = pygame.font.SysFont("monospace", 42)
        self.health_display = self.data.font.render("200", 1, (255, 255, 255))
        
        self.player: Player = Player(self.data, self.data.middle, [50, 50])
        self.player_group.add(self.player)
        
        self.world_size = [7500, 7500]
        self.world_pos = [self.world_size[0] / 2, self.world_size[1] / 2]
        self.world = Sprite(self.world_pos, self.world_size, self.data.colors.victory)
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
        self.data.screen.fill((0, 0, 0))
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
        world = self.world.rect
        
        if world.x < -self.world_size[0] + 325 or world.y < -self.world_size[1] + 325:
            player.burning = False
            print("victory")
            return

        if pygame.sprite.spritecollide(player, self.path_group, False):
            player.burning = False
        else:
            player.burning = True

    def create_world_border(self):
        bottom_border_pos = [self.world_pos[0], (self.world_pos[1] * 2) + 500]
        bottom_border = Sprite(bottom_border_pos, [self.world_size[0], 1000], self.data.colors.victory)  
        self.world_group.add(bottom_border)
        top_border_pos = [(self.world_pos[0] * 2) + 500, self.world_pos[1]]
        top_border = Sprite(top_border_pos, [self.world_size[0], 1000], self.data.colors.victory)  
        self.world_group.add(top_border)


    def update_display(self):
        self.health_display = self.data.font.render(
            str(self.player.health), 1, (0, 0, 0)
        )
        self.data.screen.blit(self.health_display, (50, 50))

    def generate_world(self, path_limit):
        self.tile_surface(self.world.image, pygame.image.load("assets/fire.png"), 64)

        def generate_path():
            self.create_path(path.destination, 250)
            self.create_island(path.destination, 250)
            if not random.randrange(0, 4):
                self.create_path(path.destination, 100)
                self.create_island(path.destination, 400)
            if len(self.paths) < path_limit/3 and not random.randrange(0, 4):
                self.create_path(path.destination, 100)
                self.create_island(path.destination, 400)

        # add paths until size limit is reached
        self.create_island(self.data.middle, 400)
        self.create_path(self.data.middle, 200)
        for path in self.paths:
            generate_path()
            if len(self.paths) >= path_limit:
                break

        for path in self.paths:
            path.draw_path(self.data, self.world)
        
        self.create_world_border()

    def create_path(self, pos, thickness):
        new_path_angle = random.choice([[0, 1], [1, 1], [1, 0]])
        new_thickness = (
            int(thickness * sqrt(2)) if new_path_angle == [1, 1] else thickness
        )
        new_length = random.choice([30, 60])
        if 0 in new_path_angle:
            new_length *= 2

        new_path = Path(self.data, pos, new_thickness, new_length, new_path_angle)
        for section in new_path.sections:
            self.path_group.add(section)
        self.paths.append(new_path)

    def create_island(self, pos, size):
        new_island = Island(self.data, pos, size)
        self.path_group.add(new_island)
        self.world.image.blit(new_island.image, [pos[0] - size / 2, pos[1] - size / 2])


if __name__ == "__main__":
    pygame.init()
    LavaGame().play()
