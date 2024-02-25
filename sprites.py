import pygame
from random import randrange
from math import sqrt


def load_game_data(game_data):
    global game
    game = game_data
    return game


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


class Player(Sprite):
    speed = 10 
    health = 200
    burning = False
    move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    tank_image = pygame.image.load("assets/tank.png")

    def __init__(self, pos, size):
        super().__init__(pos, size, game.colors.player)
        self.tank_image = pygame.transform.scale(self.tank_image, self.size)
        self.image = pygame.transform.rotate(self.tank_image, 180)

    def fall_in_lava(self):
        """play sound and animation"""

    def take_burn_damage(self):
        self.health -= 1

    def key_count(self, keys):
        amount_pressed = 0
        for key in keys:
            if key:
                amount_pressed += 1
        return amount_pressed

    def movement_handler(self, keys, path_group, world_group):
        """moves all sprites in the groups"""
        if self.key_count(keys) >= 3:
            return
        speed = self.speed if not self.burning else self.speed / 2
        if self.key_count(keys) >= 2:
            speed = speed - int(speed / 4) 

        def move_group(group, i, is_x_axis):
            for element in group:
                if is_x_axis:
                    element.rect.x += speed * [1, -1][i]
                else:
                    element.rect.y += speed * [1, -1][i]

        for i in range(2):
            if keys[self.move[i]]:
                move_group(path_group, i, True)
                move_group(world_group, i, True)

        for i in range(2):
            if keys[self.move[2:4][i]]:
                move_group(path_group, i, False)
                move_group(world_group, i, False)

    def update_direction(self, keys):
        def rotate(degrees):
            return pygame.transform.rotate(self.tank_image, degrees)
        # diagonal if rotation if 2 or more keys pressed
        if self.key_count(keys) >= 2:
            if keys[self.move[1]] and keys[self.move[2]]:
                self.image = rotate(315)
            if keys[self.move[1]] and keys[self.move[3]]:
                self.image = rotate(225)
            if keys[self.move[0]] and keys[self.move[3]]:
                self.image = rotate(135)
            if keys[self.move[0]] and keys[self.move[2]]:
                self.image = rotate(45)
            return

        # perpendicular directions
        if keys[self.move[1]]:
            self.image = rotate(270)
        if keys[self.move[0]]:
            self.image = rotate(90)
        if keys[self.move[2]]:
            self.image = rotate(0)
        if keys[self.move[3]]:
            self.image = rotate(180)


class Path:
    """line of sprites"""

    sections = []
    length = 0
    angle = []
    spread = 15
    danger_level = 1
    thickness = 0

    def __init__(self, pos, thickness, length, angle):
        self.length = length
        self.angle = angle
        self.start = [pos[0], pos[1]]
        self.thickness = thickness

        rect_size = self.thickness
        if 0 not in angle:
            rect_size = self.thickness / sqrt(2)
        if angle == [1, 1]: 
            if not thickness < 200:
                rect_size -= 100
            else:
                rect_size -= 50

        angle = [angle[0] * self.spread, angle[1] * self.spread]
        for i in range(0, self.length):
            self.sections.append(
                Sprite(
                    [pos[0] + (i * angle[0]), pos[1] + (i * angle[1])],
                    [rect_size, rect_size],
                    game.colors.path,
                )
            )
        self.destination = [
            pos[0] + (self.length * angle[0]),
            pos[1] + (self.length * angle[1]),
        ]

    def draw_path(self, world, border_style=False):
        """draws a path from start to destination on the world"""
        if border_style:
            pygame.draw.line(
                world.image,
                (165, 42, 42),
                self.start,
                self.destination,
                self.thickness,
            )
        pygame.draw.line(
            world.image,
            game.colors.path,
            self.start,
            self.destination,
            self.thickness,
        )

    def create_hazards(self):
        for section in self.sections:
            if self.danger_check():
                Volcano(section.pos, 128)

    def danger_check(self):
        """More likely to be True if the danger_level is high"""
        return not randrange(100 - self.danger_level)


class Island(Sprite):
    def __init__(self, pos, size):
        super().__init__(pos, [size, size], game.colors.path)
        self.rect.center = pos


class Volcano(Sprite):
    def __init__(self, pos, size):
        super().__init__(pos, size, game.colors.player)
        self.rect.center = pos
