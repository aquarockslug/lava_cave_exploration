import pygame
import sys
from dataclasses import dataclass

@dataclass
class GameData():
    fps: int = 50
    menu_color: tuple = (155, 166, 177)
    bg_color: tuple = (255, 127, 0)
    player_color: tuple = (250, 26, 142)
    clock: object = pygame.time.Clock()
    size: dict = (1080, 1080) 
    middle: dict = (size[0]/2, size[1]/2) 
    screen: object = pygame.display.set_mode([size[0], size[1]])

def main():
    pygame.init()
    game = GameData()

    # TODO: Create player object
    player = Sprite([game.middle[0], game.middle[1]], [20, 20], game.player_color)
    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

    global path_group
    path_group = pygame.sprite.Group()
    create_path([game.middle[0], game.middle[1] - game.size[1]/2])

    player_group = pygame.sprite.Group()
    player_group.add(player)

    loop = True
    while loop:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                loop = False

        game.screen.fill(game.bg_color)
        move(player)

        if pygame.sprite.spritecollide(player, path_group, False):
            player.image.fill(game.player_color)
        else:
            if player.image.get_at([0, 0]) == game.player_color:
                print("lava entered")
                # player.lava_entered()    
            # player.burn()
            player.image.fill((255, 0, 0))

        path_group.draw(game.screen)
        player_group.draw(game.screen)

        pygame.display.update()
        game.clock.tick(game.fps)

    sys.exit()

def move(player):
    key = pygame.key.get_pressed()
    for i in range(2):
        if key[player.move[i]]:
            for sprite in path_group:
                sprite.rect.x += 5 * [1, -1][i]

    for i in range(2):
        if key[player.move[2:4][i]]:
            for sprite in path_group:
                sprite.rect.y += 5 * [1, -1][i]

# factory
def create_path(pos):
    # TODO: random generation
    new_path = Path(pos, [160, 1000])
    return path_group.add(new_path)

# Game objects

class Sprite(pygame.sprite.Sprite):
    rect = None
    image = None
    def __init__(self, pos, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
                
class Path(Sprite):
    length = 100
    def __init__(self, pos, size):
        super().__init__(pos, size, (87, 93, 94))
        self.length = size[1] 
   
if __name__ == '__main__':
    main()
