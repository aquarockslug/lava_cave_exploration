import pygame
import sys
from dataclasses import dataclass

@dataclass
class GameData():
    fps: int = 50
    menu_color: tuple = (155, 166, 177)
    bg_color: tuple = (255, 127, 0)
    player_color: tuple = (250, 26, 142)
    path_color: tuple = (87, 93, 94)
    clock: object = pygame.time.Clock()
    size: dict = (1080, 1080) 
    middle: dict = (size[0]/2, size[1]/2) 
    screen: object = pygame.display.set_mode([size[0], size[1]])

def main():
    global game
    pygame.init()
    game = GameData()

    # TODO: Create player object
    player = Player([game.middle[0], game.middle[1]], [20, 20])
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
        player.movement_handler() 

        if pygame.sprite.spritecollide(player, path_group, False):
            player.image.fill(game.player_color)
        else:
            if player.image.get_at([0, 0]) == game.player_color:
                player.fall_in_lava()    
            player.burn()

        path_group.draw(game.screen)
        player_group.draw(game.screen)

        pygame.display.update()
        game.clock.tick(game.fps)

    sys.exit()

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
                
class Player(Sprite):
    speed = 5

    def __init__(self, pos, size):
        super().__init__(pos, size, game.player_color)

    def movement_handler(self):
        key = pygame.key.get_pressed()
        for i in range(2):
            if key[self.move[i]]:
                for sprite in path_group:
                    sprite.rect.x += self.speed * [1, -1][i]

        for i in range(2):
            if key[self.move[2:4][i]]:
                for sprite in path_group:
                    sprite.rect.y += self.speed * [1, -1][i]

    def fall_in_lava(self):
        print("lava entered")
        # play sound and animation
        pass

    def burn(self):
        self.image.fill((255, 0, 0))
        # self.health -= 1
        pass

class Path(Sprite):
    length = 100
    def __init__(self, pos, size):
        super().__init__(pos, size, game.path_color)
        self.length = size[1] 

# class volcano(Sprite):
   
if __name__ == '__main__':
    main()
