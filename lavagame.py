import random
import sys
import os
from math import sqrt
import pygame

from path import Path, Island
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
    burned_last_frame = False
    asset_dir = os.path.join(os.path.dirname(__file__), 'assets')
    ambient_sound = pygame.mixer.Sound(asset_dir + "/LavaLoop.wav")

    def __init__(self, gamedata):
        self.data = gamedata
        self.data.font = pygame.font.SysFont("monospace", 42)
        self.health_display = self.data.font.render("200", 1, (255, 255, 255))

        self.world_size = [7000, 7000]
        self.world_pos = [self.world_size[0] / 2, self.world_size[1] / 2]
        self.world = Sprite(self.world_pos, self.world_size, self.data.colors.victory)
        self.world_group.add(self.world)
        self.generate_world(100)

        self.player: Player = Player(self.data.middle, [50, 50])
        self.player_group.add(self.player)

    def play(self):
        """main gameplay loop"""
        self.ambient_sound.play(-1)
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
        """renders a frame of the game"""
        key = pygame.key.get_pressed()
        self.data.screen.fill((0, 0, 0))
        self.world_group.draw(self.data.screen)
        self.player.movement_handler(key, self.path_group, self.world_group)
        self.player.update_direction(key)

        if not self.victory_condition(self.world.rect):
            self.update_collision()
            if self.player.burning and not self.burned_last_frame:
                self.player.fall_in_lava()
            if self.player.burning:
                self.player.take_burn_damage()
                self.burned_last_frame = True
            else:
                if self.burned_last_frame:
                    self.player.left_lava()
                self.burned_last_frame = False

        # self.path_group.draw(self.data.screen)
        self.player_group.draw(self.data.screen)

        self.update_display()
        pygame.display.update()
        self.data.clock.tick(self.data.fps)

    def update_collision(self):
        """updates player burning"""
        if pygame.sprite.spritecollide(self.player, self.path_group, False):
            self.player.burning = False
        else:
            self.player.burning = True

    def tile_surface(self, surface, image, tile_size):
        """cover a surface with tiles"""
        tile = pygame.transform.scale(image, [tile_size, tile_size])
        for row in range(0, int(surface.get_height() / tile_size)):
            for col in range(0, int(surface.get_width() / tile_size)):
                surface.blit(tile, [col * tile_size, row * tile_size])

    def victory_condition(self, rect):
        """check if the player has reached the world border"""
        if rect.x < -self.world_size[0] + 500 or rect.y < -self.world_size[1] + 500:
            self.player.burning = False
            print("victory")
            return True
        return False

    def create_world_border(self):
        """creates a tiled border around the world"""
        bottom_border_pos = [self.world_pos[0], (self.world_pos[1] * 2) + 512]
        bottom_border = Sprite(
            bottom_border_pos, [self.world_size[0], 1024], self.data.colors.victory
        )
        self.tile_surface(
            bottom_border.image, pygame.image.load(self.asset_dir + "/basalt.png"), 512
        )
        self.world_group.add(bottom_border)

        right_border_pos = [(self.world_pos[0] * 2) + 512, self.world_pos[1]]
        right_border = Sprite(
            right_border_pos, [1024, self.world_size[0]], self.data.colors.victory
        )
        self.tile_surface(
            right_border.image, pygame.image.load(self.asset_dir + "/basalt.png"), 512
        )
        self.world_group.add(right_border)

    def update_display(self):
        """update health display"""
        self.health_display = self.data.font.render(
            str(self.player.health), 1, (0, 0, 0)
        )
        self.data.screen.blit(self.health_display, (50, 50))

    def generate_world(self, path_limit):
        """randomly generate a world"""
        self.tile_surface(self.world.image, pygame.image.load(self.asset_dir + "/fire.png"), 64)

        def generate_path():
            """randomly creates one, two, or three paths"""
            self.create_path(path.destination, 250)
            self.create_island(path.destination, 250)
            if not random.randrange(0, 2):
                self.create_path(path.destination, 100)
                self.create_island(path.destination, 400)
            if len(self.paths) < path_limit / 3 and not random.randrange(0, 2):
                self.create_path(path.destination, 100)
                self.create_island(path.destination, 400)

        # starting area
        self.create_island(self.data.middle, 400)
        self.create_path(self.data.middle, 200)

        # add paths until one of the conditions are met
        victory_island_count = 0
        for path in self.paths:
            generate_path()

            # count how many paths are outside the map
            if (
                path.destination[0] > self.world_size[0]
                or path.destination[1] > self.world_size[1]
            ):
                victory_island_count += 1

            # stop generating conditions
            if victory_island_count > 0 and len(self.paths) >= path_limit:
                break
            if victory_island_count >= 5:
                break

        for path in self.paths:
            path.draw_path(self.data, self.world)

        self.create_world_border()

    def create_path(self, pos, thickness):
        new_path_angle = random.choice([[0, 1], [1, 1], [1, 0]])
        new_thickness = (
            int(thickness * sqrt(2)) if new_path_angle == [1, 1] else thickness
        )
        new_length = random.choice([40, 80])
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
