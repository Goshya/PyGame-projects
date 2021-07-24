import pygame
import random
import sys

# initializing surfaces
window = [640, 960]
screen_size = [1200, 1000]
sc = pygame.display.set_mode(screen_size)
display = pygame.Surface(window)
player_rect = pygame.Rect(307, 600, 26, 50)
TILE = 32
clock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption("Doodle's adventures")
pygame.display.set_icon(pygame.image.load('Images/Doodle.png'))

# player settings/stats
moving_right = False
moving_left = False
in_jump = False
air_timer = 0
double_jump = True
equipment = []
height = 570
score = 0
coins = 0
player_frame = 0
player_action = 'idle'
player_flip = False
total_coins = int(open('Data/Total coins.txt').read())
max_score = int(open('Data/Max score.txt').read())
new_record = ''
fullscreen = False
jump = True
revive_cost = 100

vertical_y = 0
player_movement = [0, 0]
true_scroll = -40
scroll = true_scroll

# initializing map
tile_map = []
boost_map = []
coin_map = []

tile_map.append(pygame.Rect(0, 670, 640, TILE))
boost_map.append(pygame.Rect(120, 630, 50, 50))
coin = pygame.image.load('Images/coin1.png')
coin.set_colorkey((0, 0, 0))
def generate_tile(height):
    for i in range(window[0] // TILE):
        temp = random.randrange(0, 10)
        if temp >= 1 and temp <= 5:
            tile_map.append(pygame.Rect(i * TILE, height, TILE, TILE // 2))
        elif temp == 9:
            coin_map.append(pygame.Rect(i * TILE + 8, height - 8, 16, 16))
# Game settings
screen_res = [[640, 960], [1200, 1000], [1920, 1080]]
cur_setting = 0
cur_res = 0
settings_options = [screen_size[cur_res],'Fullscreen', 'Confirm settings', 'Back']
def settings():
    global cur_setting
    global cur_res
    global settings_options
    global sc
    global fullscreen
    in_settings = True
    while in_settings:
        sc.fill(pygame.Color('orange'))
        display.fill(pygame.Color('orange'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_settings = False
                    break
                if cur_setting == 0:
                    if event.key == pygame.K_d:
                        cur_res += 1
                        if cur_res >= len(screen_res):
                            cur_res = 0
                    if event.key == pygame.K_a:
                        cur_res -= 1
                        if cur_res < 0:
                            cur_res = len(screen_res) - 1
                if event.key == pygame.K_w:
                    cur_setting -= 1
                    if cur_setting < 0:
                        cur_setting = len(settings_options) - 1
                if event.key == pygame.K_s:
                    cur_setting += 1
                    if cur_setting >= len(settings_options):
                        cur_setting = 0
                if event.key == pygame.K_SPACE:
                    if cur_setting == 1:
                        if fullscreen:
                            fullscreen = False
                        else:
                            fullscreen = True
                    if cur_setting == 2:
                        screen_size[0] = screen_res[cur_res][0]
                        screen_size[1] = screen_res[cur_res][1]
                        if fullscreen:
                            sc = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
                        else:
                            sc = pygame.display.set_mode(screen_size)
                        #sc = pygame.display.set_mode(screen_res[cur_res])
                    if cur_setting == 3:
                        in_settings = False
        settings_options[0] = '< ' + str(screen_res[cur_res][0]) + 'x' + str(screen_res[cur_res][1]) + ' >'
        display.blit(pygame.font.SysFont('Arial', 66, bold=True).render('SETTINGS', True, pygame.Color('black')), (140, 300))
        # Drawing settings options
        settings_options_y = 400
        for i in range(len(settings_options)):
            if i == 1:
                display.blit(pygame.font.SysFont('Arial', 36, bold=True).render(settings_options[i] + ': on'
                                                                                if fullscreen else settings_options[i] + ': off',
                                                                                True, pygame.Color('white' if cur_setting == i else 'black')),
                             (155, settings_options_y))
            else:
                display.blit(pygame.font.SysFont('Arial', 36, bold=True).render(settings_options[i],
                                                                                True, pygame.Color('white' if cur_setting == i else 'black')),
                         (155, settings_options_y))
            settings_options_y += 50
        sc.blit(display, ((screen_size[0] - window[0]) // 2, (screen_size[1] - window[1]) // 2))
        pygame.display.update()

# main menu
main_menu_options = ['Start new game', 'Settings', 'Exit game']
cur_main_menu_option = 0
def main_menu():
    global cur_main_menu_option
    in_main_menu = True
    while in_main_menu:
        sc.fill(pygame.Color('orange'))
        display.fill(pygame.Color('orange'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    cur_main_menu_option -= 1
                    if cur_main_menu_option < 0:
                        cur_main_menu_option = len(main_menu_options) - 1
                if event.key == pygame.K_s:
                    cur_main_menu_option += 1
                    if cur_main_menu_option >= len(main_menu_options):
                        cur_main_menu_option = 0
                if event.key == pygame.K_SPACE:
                    if cur_main_menu_option == 0:
                        restart_game()
                        in_main_menu = False
                        break
                    elif cur_main_menu_option == 1:
                        settings()
                    elif cur_main_menu_option == 2:
                        quit()
        display.blit(pygame.font.SysFont('Arial', 66, bold=True).render('MAIN MENU', True, pygame.Color('Black')), (140, 300))
        # Drawing main menu options
        main_menu_y = 400
        for i in range(len(main_menu_options)):
            display.blit(pygame.font.SysFont('Arial', 36, bold=True).render(main_menu_options[i],
                                                                            True, pygame.Color('white' if cur_main_menu_option == i else 'black')),
                         (155, main_menu_y))
            main_menu_y += 50
        display.blit(pygame.font.SysFont('Arial', 26, bold=True).render(f'MAX SCORE: {max_score}', True, pygame.Color('black')), (25, 50))
        display.blit(pygame.font.SysFont('Arial', 26, bold=True).render(f'TOTAL COINS: {total_coins}', True, pygame.Color('black')), (25, 75))
        sc.blit(display, ((screen_size[0] - window[0]) // 2, (screen_size[1] - window[1]) // 2))
        pygame.display.update()
# game pause
game_pause_options = ['Resume game','Return to main menu', 'Settings', 'Exit game']
cur_game_pause_option = 0
def game_pause():
    global cur_game_pause_option
    game_paused = True
    while game_paused:
        sc.fill(pygame.Color('orange'))
        display.fill(pygame.Color('orange'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = False
                    break
                if event.key == pygame.K_w:
                    cur_game_pause_option -= 1
                    if cur_game_pause_option < 0:
                        cur_game_pause_option = len(game_pause_options) - 1
                if event.key == pygame.K_s:
                    cur_game_pause_option += 1
                    if cur_game_pause_option >= len(game_pause_options):
                        cur_game_pause_option = 0
                if event.key == pygame.K_SPACE:
                    if cur_game_pause_option == 0:
                        game_paused = False
                        break
                    elif cur_game_pause_option == 1:
                        main_menu()
                        game_paused = False
                    elif cur_game_pause_option == 2:
                        settings()
                    elif cur_game_pause_option == 3:
                        quit()
        display.blit(pygame.font.SysFont('Arial', 66, bold=True).render('GAME PAUSED', True, pygame.Color('black')),
                     (140, 300))
        # Drawing game pause options
        game_pause_options_y = 400
        for i in range(len(game_pause_options)):
            display.blit(pygame.font.SysFont('Arial', 36, bold=True).
                         render(game_pause_options[i], True, pygame.Color('white' if cur_game_pause_option == i else 'black')),
                         (155, game_pause_options_y))
            game_pause_options_y += 50
        display.blit(
            pygame.font.SysFont('Arial', 26, bold=True).render(f'MAX SCORE: {max_score}', True, pygame.Color('black')),
            (25, 50))
        display.blit(pygame.font.SysFont('Arial', 26, bold=True).render(f'TOTAL COINS: {total_coins}', True,
                                                                        pygame.Color('black')), (25, 75))
        sc.blit(display, ((screen_size[0] - window[0]) // 2, (screen_size[1] - window[1]) // 2))
        pygame.display.update()

# game end and restart game
game_end_options = ['Continue run','Restart game', 'Return to main menu', 'Exit game']
def restart_game():
    global player_rect
    global true_scroll
    global scroll
    global tile_map
    global height
    global coin_map
    global score
    global coins
    global new_record
    player_rect.x = 307
    player_rect.y = 600
    true_scroll = -40
    scroll = true_scroll
    tile_map = [pygame.Rect(0, 670, 640, TILE)]
    coin_map = []
    score = 0
    coins = 0
    height = 570
    new_record = ''
    for i in range(10):
        generate_tile(height)
        height -= 100
    return
def game_end():
    global game_ended
    global revive_cost
    global total_coins
    cur_option = 0
    game_ended = True
    while game_ended:
        sc.fill(pygame.Color('orange'))
        display.fill(pygame.Color('Orange'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    cur_option -= 1
                    if cur_option < 0:
                        cur_option = len(game_end_options) - 1
                if event.key == pygame.K_s:
                    cur_option += 1
                    if cur_option >= len(game_end_options):
                        cur_option = 0
                if event.key == pygame.K_SPACE:
                    if cur_option == 0:
                        if total_coins >= revive_cost:
                            total_coins -= revive_cost
                            revive_cost += 50
                            for i in range(len(tile_map)):
                                if tile_map[i].top < tile_map[0].top:
                                    player_rect.bottom = tile_map[i].top
                                    player_rect.x = tile_map[i].x
                                    break
                            game_ended = False
                    elif cur_option == 1:
                        restart_game()
                        game_ended = False
                        break
                    elif cur_option == 2:
                        game_ended = False
                        main_menu()
                    elif cur_option == 3:
                        quit()
        display.blit(pygame.font.SysFont('Arial', 66, bold=True).render('GAME OVER', True, pygame.Color('black')),
                     (140, 300))
        # Drawing end game options
        if new_record != '':
            end_game_y =470
            display.blit(pygame.font.SysFont('Arial', 30, bold=True).render(f'NEW RECORD - {max_score}', True, (0,0,0)), (180,430))
        else:
            end_game_y = 450
        for i in range(len(game_end_options)):
            if i == 0:
                display.blit(pygame.font.SysFont('Arial', 36, bold=True).render(f'{game_end_options[i]} ({revive_cost} coins)', True,
                                                                                pygame.Color('white' if cur_option == i else 'black')),
                             (155, end_game_y))
            else:
                display.blit(pygame.font.SysFont('Arial', 36, bold=True).render(game_end_options[i],
                                                                                True, pygame.Color('white' if cur_option == i else 'black')), (155, end_game_y))
            end_game_y += 50
        display.blit(pygame.font.SysFont('Arial', 30, bold=True).render(f'TOTAL COINS: {total_coins}', True, (0, 0, 0)), (180,390))
        #display.blit(pygame.font.SysFont('Arial', 26, bold=True).render(f'MAX SCORE: {max_score}', True, pygame.Color('black')), (0, 0))
        sc.blit(display, ((screen_size[0] - window[0]) // 2, (screen_size[1] - window[1]) // 2))
        pygame.display.update()

# initializing animations
animation_frames = {}
def load_animation(path, frame_duration):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

animation_database = {}
animation_database['run'] = load_animation('Animations/run',[7,7])
animation_database['idle'] = load_animation('Animations/idle',[20,20])

# collisions
def collision_test(rect, tile_map):
    hit_list = []
    for tile in tile_map:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, tile_map, movement):
    collision_types = {'top':False, 'left':False, 'right':False, 'bottom':False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tile_map)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tile_map)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

collision_types = {'top':False, 'left':False, 'right':False, 'bottom':False}
main_menu()
game = True
while game:
    display.fill((120, 0, 250))
    true_scroll += (player_rect.y - true_scroll - 640) // 20
    scroll = min(scroll, int(true_scroll))

    # drawing map
    i = 0
    while i < len(tile_map):
        if tile_map[i].y - scroll >= 960:
            tile_map.remove(tile_map[i])
        else:
            pygame.draw.rect(display, pygame.Color('black'),
                             (tile_map[i].x, tile_map[i].y - scroll, tile_map[i].width, tile_map[i].height))
            i += 1
    #for i in range(len(tile_map)):
    #    if tile_map[i].y - scroll >= 960:
    #        tile_map.remove(tile_map[i])
    #        break
    #    pygame.draw.rect(display, pygame.Color('black'), (tile_map[i].x, tile_map[i].y - scroll, tile_map[i].width, tile_map[i].height))
    for i in range(len(coin_map)):
        display.blit(pygame.transform.scale(coin, (16, 16)), (coin_map[i].x, coin_map[i].y - scroll))
    for i in range(len(coin_map)):
        if player_rect.colliderect(coin_map[i]):
            coin_map.pop(i)
            coins += 1
            break

    #player_rect, collision_types = move(player_rect, tile_map, player_movement)

    if collision_types['top']:
        vertical_y = 0
    if collision_types['bottom']:
        air_timer = 0
        vertical_y = 0
        double_jump = True
        jump = True
    else:
        air_timer += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 4
    if moving_left:
        player_movement[0] -= 4

    if player_rect.x >= 627:
        player_rect.x = -12
    if player_rect.x <= -13:
        player_rect.x = 627

    player_movement[1] += vertical_y
    vertical_y += 0.5
    vertical_y = min(vertical_y, 7)

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect, collision_types = move(player_rect, tile_map, player_movement)

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False),
                 (player_rect.x, player_rect.y - scroll))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_w:
                if air_timer <= 6:
                    vertical_y = -12
            if event.key == pygame.K_ESCAPE:
                game_pause()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False
    if int(abs(player_rect.y - 600)) // 100 > score:
        generate_tile(height)
        height -= 100
    score = max(score, int(abs(player_rect.y - 600)) // 100)
    if score > max_score:
        new_record = 'NEW RECORD!'
    max_score = max(score, max_score)
    open('Data/Max score.txt', 'w').write(str(max_score))
    display.blit(pygame.font.SysFont('Arial', 26, bold=True).render(f'Score: {score}   {new_record}', True, pygame.Color('orange')),
                 (25, 20))
    display.blit(pygame.font.SysFont('Arial', 26, bold=True).render(f'Coins: {coins}', True, pygame.Color('orange')),
                 (25, 65))
    #sc.blit(display, (0, 0))
    if player_rect.y - scroll >= window[1]:
        total_coins += coins
        print(total_coins)
        open('Data/Total coins.txt', 'w').write(str(total_coins))
        moving_right = False
        moving_left = False
        coins = 0
        game_end()
    sc.blit(display, ((screen_size[0] - window[0]) // 2, (screen_size[1] - window[1]) // 2))

    pygame.display.update()
    clock.tick(60)