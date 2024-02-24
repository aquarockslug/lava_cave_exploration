import pygame
from random import randrange


def load_game_data(game_data):
    global game
    game = game_data
    return game


class Sprite(pygame.sprite.Sprite):
    rect = pygame.Rect
    image = pygame.Surface

    def __init__(self, pos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Player(Sprite):
    speed = 30 
    health = 100
    burning = False
    move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

    def __init__(self, pos, size):
        super().__init__(pos, size, game.colors.player)

    def movement_handler(self, path_group, world_group):
        key = pygame.key.get_pressed()
        for i in range(2):
            if key[self.move[i]]:
                for section in path_group:
                    section.rect.x += self.speed * [1, -1][i]
                for scenery in world_group:
                    scenery.rect.x += self.speed * [1, -1][i]

        for i in range(2):
            if key[self.move[2:4][i]]:
                for path in path_group:
                    path.rect.y += self.speed * [1, -1][i]
                for scenery in world_group:
                    scenery.rect.y += self.speed * [1, -1][i]

    def fall_in_lava(self):
        """play sound and animation"""

    def take_burn_damage(self):
        self.health -= 1


class Path:
    """line of rects"""

    sections = []
    length = 0
    angle = []
    spread = 30
    danger_level = 1

    def __init__(self, pos, size, length, angle):
        self.length = length
        self.angle = angle
        self.start = [pos[0], pos[1]]
        angle = [angle[0] * self.spread, angle[1] * self.spread]
        for i in range(0, self.length):
            self.sections.append(
                Sprite(
                    [pos[0] + (i * angle[0]), pos[1] + (i * angle[1])],
                    size,
                    game.colors.path,
                )
            )
        self.destination = [
            pos[0] + (self.length * angle[0]),
            pos[1] + (self.length * angle[1]),
        ]

    def draw_border(self, world):
        """draws a line from start to destination on the world Sprite"""
        pygame.draw.line(
            world.image,
            game.colors.path,
            self.start,
            self.destination,
            680,
        )

    def create_hazards(self):
        for section in self.sections:
            if self.danger_check():
                Volcano(section.pos)

    def danger_check(self):
        """More likely to be True if the danger_level is high"""
        return not randrange(100 - self.danger_level)


class Island(Sprite):
    def __init__(self, pos):
        super().__init__(pos, [512, 512], game.colors.path)
        self.rect.center = pos


class Volcano(Sprite):
    def __init__(self, pos):
        super().__init__(pos, 128, game.colors.player)
        self.rect.center = pos
