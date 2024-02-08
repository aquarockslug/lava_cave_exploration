import pygame
import sys
from dataclasses import dataclass

@dataclass
class GameData():
    fps: int = 50
    menu_color: tuple = (0, 255, 0)
    bg_color: tuple = (255, 255, 255)
    clock: object = pygame.time.Clock()
    screen: object = pygame.display.set_mode([1080, 1080])

class Sprite(pygame.sprite.Sprite):
    rect = None
    image = None
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos
                
class Hallway(Sprite):
    length = 100
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.length = size[0] 

hall_group = pygame.sprite.Group()

def main():
    pygame.init()
    game = GameData()

    player = Sprite([20, 20], [20, 20])
    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    player.vx = 5
    player.vy = 5

    create_paths()

    player_group = pygame.sprite.Group()
    player_group.add(player)

    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        game.screen.fill(game.bg_color)
        update_player(player)

        # TODO: trigger when player isnt touching hall_group
        hit = pygame.sprite.spritecollide(player, hall_group, True)
        if hit: player.image.fill((255, 0, 0))

        player_group.draw(game.screen)
        hall_group.draw(game.screen)

        pygame.display.update()
        game.clock.tick(game.fps)

    sys.exit()

def update_player(player):
    key = pygame.key.get_pressed()
    for i in range(2):
        if key[player.move[i]]:
            player.rect.x += player.vx * [-1, 1][i]

    for i in range(2):
        if key[player.move[2:4][i]]:
            player.rect.y += player.vy * [-1, 1][i]

# factory
def create_paths():
    # TODO: random generation
    new_path = Hallway([200, 200], [20, 200])
    return hall_group.add(new_path)
    
if __name__ == '__main__':
    main()
