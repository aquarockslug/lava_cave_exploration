import pygame
import sys
import random
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
    health_display = my_font.render("100", 1, (255, 255, 255))

    global paths
    paths = []

    create_map(50)

def main():
    game.screen.fill(game.bg_color)
    player.movement_handler(floor_group) 
    update_display()
    update_collision()
    if player.burning: player.take_burn_damage()
    floor_group.draw(game.screen)
    player_group.draw(game.screen)
    pygame.display.update()
    game.clock.tick(game.fps)

def update_collision():
    if pygame.sprite.spritecollide(player, floor_group, False):
        player.image.fill(game.player_color)
        player.burning = False
    else: 
        if player.image.get_at([0, 0]) == game.player_color:
            player.fall_in_lava()
            player.burning = True
   
def update_display():
    health_display = my_font.render(str(player.health), 1, (255, 255, 0))
    game.screen.blit(health_display, (50, 50))

def create_map(size):
    create_island([game.middle[0], game.middle[1]])
    create_path([game.middle[0], game.middle[1]])
    for p in paths:
        if len(paths) >= size: break
        for i in range(0, random.randint(1,2)):
            create_path(p.destination)

def create_path(pos):
    new_path_angle = random.choice([[0, 1], [3, 1], [-3, 1]])
    if new_path_angle == [0, 1]: new_length = random.randint(40, 80)
    else: new_length = random.randint(80, 160)

    new_path = Path(pos, [240, 240], new_length, new_path_angle)
    for section in new_path.sections: floor_group.add(section)
    paths.append(new_path)

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
