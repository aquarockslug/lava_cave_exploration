import pygame


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
    """Sprite that represents the player"""

    speed = 10
    health = 200
    burning = False
    move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    tank_image = pygame.image.load("assets/tank.png")
    lava_enter_sound = pygame.mixer.Sound("assets/LavaSplash.wav")
    engine_sound = pygame.mixer.Sound("assets/engine.wav")
    burning_sound = pygame.mixer.Sound("assets/hiss.wav")

    def __init__(self, pos, size):
        super().__init__(pos, size, (255, 255, 0))
        self.tank_image = pygame.transform.scale(self.tank_image, self.size)
        self.image = pygame.transform.rotate(self.tank_image, 180)
        self.burning_sound.set_volume(0.3)
        self.engine_sound.play(-1)

    def fall_in_lava(self):
        """handler for when the path is exited"""
        self.lava_enter_sound.play()

    def take_burn_damage(self):
        """handler for not touching the path"""
        self.burning_sound.play()
        self.health -= 1

    def left_lava(self):
        """handler for when the lava is exited"""

    def key_count(self, keys):
        """count how many movement keys are being pressed"""
        amount_pressed = 0
        if keys[self.move[0]]:
            amount_pressed += 1
        if keys[self.move[1]]:
            amount_pressed += 1
        if keys[self.move[2]]:
            amount_pressed += 1
        if keys[self.move[3]]:
            amount_pressed += 1
        return amount_pressed

    def movement_handler(self, keys, path_group, world_group):
        """moves all sprites in the path and world group depending on keys"""
        key_count = self.key_count(keys)
        if key_count >= 3:
            return
        speed = self.speed if not self.burning else self.speed / 2
        if key_count >= 2:
            speed = speed - int(speed / 4)

        if key_count in (1, 2):
            self.engine_sound.set_volume(0.7)
        else:
            self.engine_sound.set_volume(0.35)

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
        """uses keys to keep the tank_image pointed in the correct direction"""

        def rotate(degrees):
            return pygame.transform.rotate(self.tank_image, degrees)

        # diagonal if 2 or more keys pressed
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
