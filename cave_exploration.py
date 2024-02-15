import pygame
import sys
from sprites import *
from dataclasses import dataclass

@dataclass
class GameData():
    fps: int = 50
    menu_color: tuple = (155, 166, 177)
    bg_color: tuple = (255, 127, 0)
    player_color: tuple = (250, 26, 142)
    floor_color: tuple = (87, 93, 94)
    clock: object = pygame.time.Clock()
    size: dict = (1080, 1080) 
    middle: dict = (size[0]/2, size[1]/2) 
    screen: object = pygame.display.set_mode([size[0], size[1]])

def init():
    pygame.init()
    global playing
    playing = True

    global game
    game = load_game_data(GameData())

    global player
    player = Player([game.middle[0], game.middle[1]], [20, 20])
    player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]

    global floor_group
    floor_group = pygame.sprite.Group()

    global player_group
    player_group = pygame.sprite.Group()
    player_group.add(player)

    global my_font
    my_font = pygame.font.SysFont("monospace", 42)
    
    global health_display
    health_display = my_font.render("100", 1, (255, 255, 0))

    create_start_location()

def main():
    game.screen.fill(game.bg_color)
    player.movement_handler(floor_group) 

    if pygame.sprite.spritecollide(player, floor_group, False):
        player.image.fill(game.player_color)
        player.burning = False
    else: 
        if player.image.get_at([0, 0]) == game.player_color:
            player.fall_in_lava()
            player.burning = True
   
    if player.burning: player.take_burn_damage()
        
    health_display = my_font.render(str(player.health), 1, (255, 255, 0))
    game.screen.blit(health_display, (50, 50))

    floor_group.draw(game.screen)
    player_group.draw(game.screen)

    pygame.display.update()
    game.clock.tick(game.fps)

def create_start_location():
    create_island([game.middle[0], game.middle[1]])
    create_paths([game.middle[0], game.middle[1]])
    
def create_paths(pos):
    # TODO: random angle 
    floor_group.add(Path(pos, [160, 1000], 0))
    # floor_group.add(Path(pos, [160, 1000], 270))

def create_island(pos):
    new_island = Island(pos)
    floor_group.add(new_island)
   
if __name__ == '__main__':
    init()
    while playing:
        main()
        if player.health <= 0: 
            playing = False 

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                playing = False 
    sys.exit()
