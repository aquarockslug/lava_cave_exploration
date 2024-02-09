import pygame
def load_game_data(game_data):
    global game
    game = game_data
    return game

class Sprite(pygame.sprite.Sprite):
    rect = None
    circle = None
    image = None
    def __init__(self, pos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
                
class Player(Sprite):
    speed = 7 
    health = 100
    burning = False

    def __init__(self, pos, size):
        super().__init__(pos, size, game.player_color)

    def movement_handler(self, floor_group):
        key = pygame.key.get_pressed()
        for i in range(2):
            if key[self.move[i]]:
                for sprite in floor_group:
                    sprite.rect.x += self.speed * [1, -1][i]

        for i in range(2):
            if key[self.move[2:4][i]]:
                for sprite in floor_group:
                    sprite.rect.y += self.speed * [1, -1][i]

    def fall_in_lava(self):
        print("lava entered")
        # play sound and animation

    def take_burn_damage(self):
        self.image.fill((255, 0, 0))
        self.health -= 1

class Path(Sprite):
    destination = None
    def __init__(self, pos, size, angle):
        super().__init__(pos, size, game.floor_color)
        # TODO rotate around pos
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect.midbottom = pos
        self.destination = self.rect.midtop

    def update(self):
        game.screen.blit(self.image, self.rect.center)

class Island(Sprite):
    def __init__(self, pos):
        super().__init__(pos, [512, 512], game.floor_color)
        self.rect.center = pos

class HealthBar():
    pass

# class volcano(Sprite):
