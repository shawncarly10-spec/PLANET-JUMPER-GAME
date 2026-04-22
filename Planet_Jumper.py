import pygame
import random
import math
import os
import sys
from player import Player
from planet import Planet

#===============================
# EXE format
#===============================
def resource_path(relative_path):
    #Gets absolute path to resource, works for dev and for PyInstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Use the helper function so it looks in the temp folder (_MEIxxxx)
cover_img = pygame.image.load(resource_path("planetary_descent_cover.png"))
pygame.display.set_icon(cover_img)

pygame.init()
pygame.mixer.init()
# ==========================================
# WINDOW SETUP
# ==========================================
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Jumper")

clock = pygame.time.Clock()

# ==========================================
# FONTS
# ==========================================
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 20)

# ==========================================
# CREATE PLAYER
# ==========================================
player = Player(400, 100)
#===========================================
# MUSIC TRACK
#===========================================
# Track the currently playing song to avoid restarts
current_track = "Planet_Jumper_OST_Planetary_Descent.mp3"
# --- Star Layers ---
# Far stars: many, tiny, and very slow
far_stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), 1) for _ in range(100)]
# Near stars: fewer, slightly larger, and faster
near_stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(2, 3)) for _ in range(40)]
# shooting stars
shooting_stars = []
def draw_stars(screen, camera_x, camera_y):
    
   
    for star in far_stars:
        x, y, size = star
        draw_x = int(x - camera_x * 0.05) % WIDTH
        draw_y = int(y - camera_y * 0.05) % HEIGHT
        star_pulse = (math.sin(pygame.time.get_ticks() * 0.002 + draw_x) + 1) / 2  # Pulsate between 0 and 1
        brightness = 100 + (155 * star_pulse)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (draw_x, draw_y), size)
    for star in near_stars:
        x, y, size = star
        draw_x = int(x - camera_x * 0.1) % WIDTH
        draw_y = int(y - camera_y * 0.1) % HEIGHT
        fast_pulse = (math.sin(pygame.time.get_ticks() * 0.003 + draw_x) + 1) / 2
        brightness = 100 + (155 * fast_pulse)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (draw_x, draw_y), size)
def draw_goal_arrow(screen, player, goal):
    if not goal: return

    # Get direction vector from player to goal
    dx = goal.x - player.x
    dy = goal.y - player.y
    dist = math.sqrt(dx**2 + dy**2)
    
    # Only show arrow if the goal is off-screen (e.g., further than 500 pixels)
    if dist > 450:
        angle = math.atan2(dy, dx)
        
        # Place arrow at the edge of a circle around the player
        # (keeping it 100 pixels away from player, but inside the screen)
        arrow_dist = 150 
        arrow_x = (WIDTH // 2) + math.cos(angle) * arrow_dist
        arrow_y = (HEIGHT // 2) + math.sin(angle) * arrow_dist
        
        # Draw a simple triangle pointing at the goal
        points = [
            (arrow_x + math.cos(angle) * 15, arrow_y + math.sin(angle) * 15), # Tip
            (arrow_x + math.cos(angle + 2.5) * 10, arrow_y + math.sin(angle + 2.5) * 10),
            (arrow_x + math.cos(angle - 2.5) * 10, arrow_y + math.sin(angle - 2.5) * 10)
        ]
        pygame.draw.polygon(screen, (255, 255, 0), points)
# ==========================================
# CREATE PLANETS
# x, y, radius, color, gravity, friction
# ==========================================
levels = [
    
    {
        #==========================================
        # LEVEL 1 - BASIC GRAVITY AND JUMPING DO NOT TOUCH
        #==========================================
        
        "planets": [
            Planet(400, 500, 100, (100, 100, 255), gravity_strength=0.5, friction=0.02),## Blue planet is the starting point
            Planet(600, 300, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01),
            Planet(200, 700, 50, (0, 0, 0,), gravity_strength=1.0, friction=1.0),
            Planet(600, 700, 50, (255, 255, 255), gravity_strength=-0.5, friction=-0.01),
            Planet(200, 300, 50, (0, 255, 0), gravity_strength=0.7, friction=0.01) ## GREEN planet is the goal
        ]
    },
    {
        
        "planets": [
            Planet(400, 500, 100, (100, 100, 255), gravity_strength=0.5, friction=0.02),## Blue planet is the starting point
            Planet(600, 300, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(1000, 500, 180, (0, 0, 255), gravity_strength=0.3, friction=0.01), 
            Planet(1500, 300, 50, (255, 71, 26), gravity_strength=0.5, friction=0.04), 
            Planet(2000, 600, 80, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(2500, 100, 50, (0,0,0), gravity_strength=1.0, friction=1.0), 
            Planet(3000, 400, 100, (0, 255, 0), gravity_strength=0.4, friction=0.01) ## GREEN planet is the goal
        ]
    },
    {
        
        "planets": [
            Planet(3000, 400, 100, (100, 100, 255), gravity_strength=0.5, friction=0.02),## Blue planet is the starting point
            Planet(3200, 200, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(3500, 500, 90, (255, 71, 26), gravity_strength=0.5, friction=0.04), 
            Planet(4000, 300, 70, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(4500, 600, 100, (255, 255,  0), gravity_strength=0.3, friction=0.01), 
            Planet(5000, 100, 90, (0,0,0), gravity_strength=1.0, friction=1.0), 
            Planet(5000, 400, 60, (60,60,12), gravity_strength=0.5, friction=0.09), 
            Planet(5500, 400, 100, (0, 255, 0), gravity_strength=0.4, friction=0.01) ## GREEN planet is the goal
        ]
    },
    {
        "planets": [
            Planet(5500, 400, 100, (100, 100, 255), gravity_strength=0.5, friction=0.02),## Blue planet is the starting point
            Planet(5700, 200, 30, (0, 25, 100), gravity_strength=0.3, friction=0.01), 
            Planet(5725, -100, 30, (255, 255, 255), gravity_strength=-0.5, friction=-0.01),
            Planet(6000, 500, 180, (255, 100, 255), gravity_strength=0.3, friction=0.01), 
            Planet(6200, 300, 50, (249, 7, 69), gravity_strength=0.5, friction=0.04), 
            Planet(6500, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(6700, 500, 70, (10, 50, 200), gravity_strength=0.7, friction=0.01),
            Planet(7000, 600, 100, (15, 10, 20,), gravity_strength=1.0, friction=0.10),
            Planet(7010, 800, 50, (0, 0, 0), gravity_strength=1.5, friction=1.00),
            Planet(7200, 300, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(7500, 100, 50, (0, 40, 80), gravity_strength=0.5, friction=0.04),
            Planet(8000, 400, 100, (0, 255, 0), gravity_strength=0.4, friction=0.01) ## GREEN planet is the goal
        ]
    },
    {
        "planets": [
            Planet(8000, 400, 100, (100, 100, 255), gravity_strength=0.5, friction=0.02),## Blue planet is the starting point
            Planet(8200, -150, 30, (255, 255, 255), gravity_strength=-0.3, friction=-0.01), 
            Planet(8500, 200, 180, (100, 0, 150), gravity_strength=0.3, friction=0.01), 
            Planet(8700, -150, 50, (70, 180, 125), gravity_strength=0.5, friction=0.04), 
            Planet(9000, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(9200, 700, 70, (20, 63, 138), gravity_strength=0.7, friction=0.01),
            Planet(9300, 900, 50, (255, 255, 255), gravity_strength=-0.9, friction=-0.01),
            Planet(9500, 500, 100, (219, 173, 225), gravity_strength=0.4, friction=0.05),
            Planet(9700, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(10000, 400, 50, (200, 70, 10), gravity_strength=0.5, friction=0.05),
            Planet(10200, 150, 50, (0, 0, 0), gravity_strength=1.5, friction=1.00),
            Planet(10500 ,400 ,100 ,(0 ,255 ,0) ,gravity_strength =1.5 ,friction =0.01) ## GREEN planet is the goal with very strong gravity
        ]
    },
    {
        "planets":[
            Planet(10500 ,400 ,100 ,(100 ,100 ,255) ,gravity_strength =0.5 ,friction =0.01),## Blue planet is the starting point
            Planet(600, 300, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(1000, 500, 180, (0, 0, 255), gravity_strength=0.3, friction=0.01), 
            Planet(1500, 300, 50, (255, 71, 26), gravity_strength=0.5, friction=0.04), 
            Planet(2000, 600, 80, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(2500, 100, 50, (0,0,0), gravity_strength=1.0, friction=1.0),
            Planet(3000, 400, 100, (100, 10, 25), gravity_strength=0.5, friction=0.02),##------------------------------------
            Planet(3200, 200, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(3500, 500, 90, (255, 71, 26), gravity_strength=0.5, friction=0.04), 
            Planet(4000, 300, 70, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(4500, 600, 100, (255, 255,  0), gravity_strength=0.3, friction=0.01), 
            Planet(5000, 100, 90, (0,0,0), gravity_strength=1.0, friction=1.0), 
            Planet(5000, 400, 60, (60,60,12), gravity_strength=0.5, friction=0.09),
            Planet(5500, 400, 100, (100, 100, 100), gravity_strength=0.5, friction=0.02),## ---------------------------------
            Planet(5700, 200, 30, (0, 25, 100), gravity_strength=0.3, friction=0.01), 
            Planet(5725, -100, 30, (255, 255, 255), gravity_strength=-0.5, friction=-0.01),
            Planet(6000, 500, 180, (255, 100, 255), gravity_strength=0.3, friction=0.01), 
            Planet(6200, 300, 50, (249, 7, 69), gravity_strength=0.5, friction=0.04), 
            Planet(6500, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(6700, 500, 70, (10, 50, 200), gravity_strength=0.7, friction=0.01),
            Planet(7000, 600, 100, (15, 10, 20,), gravity_strength=1.0, friction=0.10),
            Planet(7010, 800, 50, (0, 0, 0), gravity_strength=1.5, friction=1.00),
            Planet(7200, 300, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(7500, 100, 50, (0, 40, 80), gravity_strength=0.5, friction=0.04),
            Planet(8000, 400, 100, (0, 100, 255), gravity_strength=0.5, friction=0.02),## ----------------------------------------
            Planet(8200, -150, 30, (255, 255, 255), gravity_strength=-0.3, friction=-0.01), 
            Planet(8500, 200, 180, (100, 0, 150), gravity_strength=0.3, friction=0.01), 
            Planet(8700, -150, 50, (70, 180, 125), gravity_strength=0.5, friction=0.04), 
            Planet(9000, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(9200, 700, 70, (20, 63, 138), gravity_strength=0.7, friction=0.01),
            Planet(9300, 900, 50, (255, 255, 255), gravity_strength=-0.9, friction=-0.01),
            Planet(9500, 500, 100, (219, 173, 225), gravity_strength=0.4, friction=0.05),
            Planet(9700, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(10000, 400, 50, (200, 70, 10), gravity_strength=0.5, friction=0.05),
            Planet(10200, 150, 50, (0, 0, 0), gravity_strength=1.5, friction=1.00),
            Planet(8000, 400, 100, (100, 255, 255), gravity_strength=0.5, friction=0.02),##=---------------------------------------
            Planet(8200, -150, 30, (255, 255, 255), gravity_strength=-0.3, friction=-0.01), 
            Planet(8500, 200, 180, (100, 0, 150), gravity_strength=0.3, friction=0.01), 
            Planet(8700, -150, 50, (70, 180, 125), gravity_strength=0.5, friction=0.04), 
            Planet(9000, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(9200, 700, 70, (20, 63, 138), gravity_strength=0.7, friction=0.01),
            Planet(9300, 900, 50, (255, 255, 255), gravity_strength=-0.9, friction=-0.01),
            Planet(9500, 500, 100, (219, 173, 225), gravity_strength=0.4, friction=0.05),
            Planet(9700, 600, 50, (255, 0, 0), gravity_strength=0.7, friction=0.01), 
            Planet(10000, 400, 50, (200, 70, 10), gravity_strength=0.5, friction=0.05),
            Planet(10200, 150, 50, (0, 0, 0), gravity_strength=1.5, friction=1.00),
            Planet(400, 500, 100, (0, 255, 0), gravity_strength=0.5, friction=0.02),## GREEN planet is the goal
        ]
    }

]
#==========================================
# LOAD FIRST LEVEL
#==========================================
current_level = 0
def load_level(level_index):
    global current_track, level_timer, player, planets, camera_x, camera_y, goal_planet
    # A security check to see if there are any levels after current one
    if level_index >= len(levels):
        return
    target_song = "Planet_Jumper_OST_Return_Home.mp3" if level_index == 5 else "Planet_Jumper_OST_Planetary_Descent.mp3"
    if current_track != target_song:
        pygame.mixer.music.load(resource_path(target_song))
        pygame.mixer.music.play(-1)
        current_track = target_song
    level_data = levels[level_index]
    planets = level_data["planets"]
    starting_planet = None
    goal_planet = None
    player.did_win = False
    player.is_alive = True

    if level_index == 5:
        player.fuel = 500.0
        player.max_fuel = 500.0
        level_timer = 120.0 # 2 minute timer for level 5
        #pygame.mixer.music.load(resource_path(final_level_music))
        #pygame.mixer.music.play(-1)
    else:
        player.fuel = 100.0
        player.max_fuel = 100.0
        level_timer = None # No timer for other levels
        #pygame.mixer.music.load("Planet_Jumper_OST_Planetary_Descent.mp3")
        #pygame.mixer.music.play(-1)

    for p in planets:
        if p.color == (0, 255, 0):
            goal_planet = p
            break
        if p.color == (100, 100, 255):
            starting_planet = p

    if starting_planet:
        
        player.x, player.y = starting_planet.x, starting_planet.y - (starting_planet.radius + player.size / 2 + 1)
        player = Player(player.x, player.y)  # Reset player state when loading level 
    else:
        player.x, player.y = 400, 400

    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

# ==========================================
# CAMERA POSITION
# ==========================================
camera_x = 0
camera_y = 0

# ==========================================
# MENU SETTINGS
# ==========================================
game_state = "menu"
menu_options = ["PLAY", "RULES", "CREDITS", "QUIT"]#"LEVEL SELECT",
death_options = ["RETRY?", "MENU", "QUIT"]
victory_options = ["REPLAY?", "MENU", "QUIT"]
Level_complete_options = ["NEXT LEVEL?", "MENU", "QUIT"]
pause_options = ["RETRY?","RESUME", "MENU", "QUIT"]
#level_select= ["Level 2", "level 4", "level 5", "level 6"]
selected_option = 0

running = True
#==========================================
# LOAD MUSIC
#==========================================
pygame.mixer.music.load(resource_path("Planet_Jumper_OST_Planetary_Descent.mp3"))
#Loop the music indefinitely and set volume
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)
final_level_music = "Planet_Jumper_OST_Return_Home.mp3"
# ==========================================
# MAIN GAME LOOP
# ==========================================
while running:

    # ======================================
    # HANDLE EVENTS
    # ======================================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # ----------------------------------
            # MENU CONTROLS
            # ----------------------------------
            if game_state in ["menu", "Game Over", "Victory", "Level Complete", "pause", "Credits",]: #"level select"]:

                if event.key == pygame.K_w:
                    selected_option = (selected_option - 1) % 4

                elif event.key == pygame.K_s:
                    selected_option = (selected_option + 1) % 4

                elif event.key == pygame.K_RETURN:

                    if game_state == "menu":

                        if selected_option == 0: # PLAY
                            current_level = 0
                            load_level(current_level)
                            game_state = "game"
                            camera_x = 0
                            camera_y = 0
                        elif selected_option == 1: # RULES
                            game_state = "rules"
                            selected_option = 0
                        elif selected_option == 2: # QUIT
                            game_state = "Credits"
                            selected_option = 0
                        #elif selected_option == 3:
                            #game_state = "level select"
                            #selected_option = 0
                        elif selected_option == 3:
                            running = False

                    elif game_state in ["Game Over", "Victory"]:

                        if selected_option == 0: # RETRY
                            if game_state == "Victory":
                                
                                load_level(current_level)
                                game_state = "game"
                            
                                camera_x = 0
                                camera_y = 0
                            else:
                                load_level(current_level)
                                game_state = "game"
                                camera_x = 0
                                camera_y = 0
                                selected_option = 0
                        elif selected_option == 1: # MENU
                            game_state = "menu"
                            # Force the music back to the main theme when returning to menu
                            if current_track != "Planet_Jumper_OST_Planetary_Descent.mp3":
                                pygame.mixer.music.load(resource_path("Planet_Jumper_OST_Planetary_Descent.mp3"))
                                pygame.mixer.music.play(-1)
                                current_track = "Planet_Jumper_OST_Planetary_Descent.mp3"
                            selected_option = 0
                        elif selected_option == 2: # QUIT
                            running = False
                    elif game_state == "Level Complete":

                        if selected_option == 0: # NEXT LEVEL
                            
                            if selected_option == 0:  # "NEXT LEVEL"
                                current_level += 1    
                                load_level(current_level)
                                game_state = "game"
                            elif selected_option == 1:  # "RETRY"
                                load_level(current_level)
                                game_state = "game"
                            elif selected_option == 2:  # "MENU"
                                game_state = "menu"
                    elif game_state == "pause":

                        if selected_option == 0: # RETRY
                            load_level(current_level)
                            game_state = "game"
                            
                            selected_option = 0
                        elif selected_option == 1: 
                            #game_state = "resume"
                            game_state = "game"
                            selected_option = 0
                        elif selected_option == 2: # MENU
                            game_state = "menu"
                            # Force the music back to the main theme when returning to menu
                            if current_track != "Planet_Jumper_OST_Planetary_Descent.mp3":
                                pygame.mixer.music.load(resource_path("Planet_Jumper_OST_Planetary_Descent.mp3"))
                                pygame.mixer.music.play(-1)
                                current_track = "Planet_Jumper_OST_Planetary_Descent.mp3"
                            selected_option = 0
                        elif selected_option == 3: #QUIT
                            running = False
                    #elif game_state == "level select":
                        #if selected_option == 0:
                            #load_level(1)
                            #game_state = "game"
                        #elif selected_option == 1:
                            #load_level(2)
                            #game_state = "game"
                        #elif selected_option == 2:
                            #load_level(4)
                            #game_state = "game"
                        #elif selected_option == 3:
                            #load_level(5)
                           # game_state = "game"

            # ----------------------------------
            # ESC goes to pause menu from game, and back to menu from rules
            # ----------------------------------
            if event.key == pygame.K_ESCAPE and game_state not in ["menu", "rules", "Credits"]:#, "level select"]:
                game_state = "pause"
            if event.key == pygame.K_ESCAPE and game_state == "rules":
                game_state = "menu"
                selected_option = 0
            if event.key == pygame.K_ESCAPE and game_state == "Credits":
                game_state = "menu"
                selection_option = 0
            #if event.key == pygame.K_ESCAPE and game_state == "level select":
                #game_state = "menu"
                #selection_option = 0

    # ======================================
    # UPDATE GAME
    # ======================================
    if game_state == "game":
        dt = clock.get_time() / 1000.0  # Delta time in seconds
        if level_timer is not None:
            level_timer -= dt
            if level_timer <= 0:
                level_timer = 0
                player.is_alive = False


        player.update(planets)
        if player.did_win:
            game_state = "Level Complete"
            if current_level < len(levels) - 1:
                #current_level += 1
                load_level(current_level)
                player.did_win = False
            else:
                game_state = "Victory"
                selected_option = 0
        elif not player.is_alive:
            game_state = "Game Over"
            selected_option = 0
        # Smooth camera movement
        camera_x += (player.x - WIDTH // 2 - camera_x) * 0.1
        camera_y += (player.y - HEIGHT // 2 - camera_y) * 0.1

    # ======================================
    # DRAW BACKGROUND
    # ======================================
    screen.fill((0, 0, 0))

    #=======================================
    # Initiate a Flash for selected options
    #=======================================
    # Create a pulsing value between 0 and 255
    # 0.01 controls the speed of the flash
    flash_value = int((math.sin(pygame.time.get_ticks() * 0.09) + 1) * 127.5)
    flash_color = (flash_value, 255, flash_value) # This mixes Green (0,255,0) with White (255,255,255)
    # ======================================
    # DRAW MENU
    # ======================================
    if game_state == "menu":

        decor_planets = [
            (100, 100, 30, (100, 50, 160)),
            (200, 200, 10, (255, 150, 150)),
            (600, 300, 20, (155, 10, 10)),
            (700, 400, 50, (0,60,152)),
            (500, 250, 30, (255, 255, 255)),
            (500, 500, 30, (0, 0, 0)),
            (1000, 500, 40, (140, 60, 200)),
            (2000, 800, 100, (255, 180, 100))
        ]

        for px, py, prad, pcol in decor_planets:
            pygame.draw.circle(screen, pcol, (px, py), prad)
            # Add a tiny "shine" to make them look 3D
            pygame.draw.circle(screen, (237, 237, 237), (px - prad//3, py - prad//3), prad//10)
            #pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), 3)

        for star in far_stars:
            x, y, size = star
            draw_x = int(x - camera_x * 0.05) % WIDTH
            draw_y = int(y - camera_y * 0.05) % HEIGHT
            star_pulse = (math.sin(pygame.time.get_ticks() * 0.002 + draw_x) + 1) / 2  # Pulsate between 0 and 1
            brightness = 100 + (155 * star_pulse)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (draw_x, draw_y), size)
        for star in near_stars:
            x, y, size = star
            draw_x = int(x - camera_x * 0.1) % WIDTH
            draw_y = int(y - camera_y * 0.1) % HEIGHT
            fast_pulse = (math.sin(pygame.time.get_ticks() * 0.003 + draw_x) + 1) / 2
            brightness = 100 + (155 * fast_pulse)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (draw_x, draw_y), size)
        # Randomly spawn a new shooting star (about once every 60 frames)
        if random.randint(1, 60) == 4:
            shooting_stars.append([random.randint(0, WIDTH), 0, random.randint(-5, 5), random.randint(7, 12), random.randint(10, 30)])

        # Update and Draw
        for star in shooting_stars[:]:
            star[0] += star[2] # Move X
            star[1] += star[3] # Move Y
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (star[0], star[1]),
                (star[0] - star[2]*2, star[1] - star[3]*2),
                2
        )
        # Draw the "tail"
            pygame.draw.line(screen, (255, 255, 200), (star[0], star[1]), (star[0] - star[2]*2, star[1] - star[3]*2), 2)
    
        # Remove if it leaves the screen
            if star[1] > HEIGHT:
                shooting_stars.remove(star)

        title_surface = font.render(
            "PLANET JUMPER",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title_surface,
            (
                WIDTH // 2 - title_surface.get_width() // 2,
                100
            )
        )

        for i, option in enumerate(menu_options):

            color = flash_color if i == selected_option else (200, 200, 200)

            text_surface = font.render(option, True, color)

            screen.blit(
                text_surface,
                (
                    WIDTH // 2 - text_surface.get_width() // 2,
                    250 + i * 60
                )
            )

    # ======================================
    # DRAW RULES SCREEN
    # ======================================
    elif game_state == "rules":

        rules = [
            "W / A / D = Rocket Thrusters (Uses Fuel)",
            "LEFT / RIGHT ARROWS = Walk On Surface",
            "Travel between planets using gravity",
            "Green planets are goals, Red planets are deadly",
            "Avoid dark planets, they will NEVER let you go",
            "white planets have anti-gravity, they will push you away",
            "A yellow arrow will point you towards the goal if you are off-screen",
            "HAVE FUN EXPLORING THE COSMOS!",
            "ESC = Return To Menu"
        ]

        for i, line in enumerate(rules):

            rule_surface = small_font.render(
                line,
                True,
                (255, 255, 255)
            )

            screen.blit(
                rule_surface,
                (100, 150 + i * 40)
            )
    #=======================================
    # DRAW CREDITS
    #=======================================
    elif game_state == "Credits":
        Credits = [
            "Music created by: Shawn G. Garcia",
            "",
            "Game development by: Shawn G. Garcia",
            "",
            "If you want to check out more music creation serach:",
            "Youtube/Spotify: Rustic Rabbit Records",
            "",
            "ESC = Return to menu"
        ]
        for i, line in enumerate(Credits):

            rule_surface = small_font.render(
                line,
                True,
                (255, 255, 255)
            )

            screen.blit(
                rule_surface,
                (100, 150 + i * 40)
            )
    #=======================================
    # Tempoary level select for testing levels
    #=======================================
    #elif game_state == "level select":
        #for i, option in enumerate(level_select):

            #color = flash_color if i == selected_option else (200, 200, 200)

            #text_surface = font.render(option, True, color)

            #screen.blit(
                #text_surface,
                #(
                    #WIDTH // 2 - text_surface.get_width() // 2,
                    #250 + i * 60
                #)
            #)
    # ======================================
    # DRAW GAME
    # ======================================
    elif game_state == "game":
        
        screen.fill((10, 10, 20))
        draw_stars(screen, camera_x, camera_y)
        if game_state == "game" and current_level == 0:
            instr = small_font.render("Use W/A/D to control thrusters, LEFT</RIGHT> to walk","", True, (255, 255, 255))
            screen.blit(instr,(WIDTH // 2 - instr.get_width() // 2, 50))        
        # Draw planets
        for planet in planets:
            planet.draw(screen, camera_x, camera_y)

        # Draw player
        player.draw(screen, camera_x, camera_y)
        draw_goal_arrow(screen, player, goal_planet)

        # ----------------------------------
        # DRAW FUEL BAR BACKGROUND
        # ----------------------------------
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (20, 20, 200, 25)
        )

        # Width of green/red fuel bar
        fuel_width = ((player.fuel / player.max_fuel) * 200)

        fuel_color = (
            (0, 255, 0)
            if (player.fuel / player.max_fuel) > 0.25
            else (255, 0, 0)
        )
        draw_wdith = max(0, int(fuel_width))
        pygame.draw.rect(screen,fuel_color,(20, 20, draw_wdith, 25)
        )

        # Fuel text
        fuel_text = small_font.render(
            f"FUEL: {int(player.fuel)}%",
            True,
            (255, 255, 255)
        )

        screen.blit(fuel_text, (25, 22))
        # Level text
        level_text = small_font.render(f"LEVEL: {current_level + 1}/{len(levels)}", True, (255, 255, 255))
        screen.blit(level_text, (25, 50))
        
        # Player position text
        pos_str = f"POS: ({int(player.x)}, {int(player.y)})"
        pos_text = small_font.render(pos_str, True, (255, 255, 255))
        screen.blit(pos_text, (25, 80))

        # --- DRAW TIMER AND DIALOGUE ---
        if level_timer is not None:
            # 1. Draw the Timer
            timer_str = f"OXYGEN LOSS IN: {int(level_timer)}s"
            timer_surface = font.render(timer_str, True, (255, 255, 255))
            screen.blit(timer_surface, (WIDTH // 2 - timer_surface.get_width() // 2, 20))

            # 2. Draw the Dialogue (only for the first 5 seconds of the level)
            # Assuming level_timer starts at 120
            if level_timer > 115:
                dialog_text = "Return to cords 400,400 and COME HOME!"
                dialog_surface = small_font.render(dialog_text, True, (255, 255, 255))
                
                # Draw a simple background box for the text
                box_rect = pygame.Rect(100, HEIGHT - 80, 600, 50)
                pygame.draw.rect(screen, (0, 0, 50), box_rect) # Dark blue fill
                pygame.draw.rect(screen, (0, 255, 255), box_rect, 2) # Cyan border
                
                screen.blit(dialog_surface, (120, HEIGHT - 65))
    elif game_state == "Game Over":

        game_over_surface = font.render(
            "GAME OVER",
            True,
            (255, 0, 0)
        )

        screen.blit(
            game_over_surface,
            (
                WIDTH // 2 - game_over_surface.get_width() // 2,
                100
            )
        )

        for i, option in enumerate(death_options):

            color = flash_color if i == selected_option else (200, 200, 200)

            text_surface = font.render(option, True, color)

            screen.blit(
                text_surface,
                (
                    WIDTH // 2 - text_surface.get_width() // 2,
                    250 + i * 60
                )
            )
    elif game_state == "Victory":

        victory_surface = font.render(
            "VICTORY!",
            True,
            (0, 255, 0)
        )

        screen.blit(
            victory_surface,
            (
                WIDTH // 2 - victory_surface.get_width() // 2,
                100
            )
        )

        for i, option in enumerate(victory_options): # Use the correct list name
            # Change 'flash_value' to 'flash_color' to match your menu
            color = flash_color if i == selected_option else (200, 200, 200)

            text_surface = font.render(option, True, color)

            screen.blit(
                text_surface,
                (
                    WIDTH // 2 - text_surface.get_width() // 2,
                    250 + i * 60
                )
            )
    elif game_state == "Level Complete":

        level_complete_surface = font.render(
            "LEVEL COMPLETE!",
            True,
            (0, 255, 0)
        )

        screen.blit(
            level_complete_surface,
            (
                WIDTH // 2 - level_complete_surface.get_width() // 2,
                100
            )
        )

        for i, option in enumerate(Level_complete_options):

            color = flash_color if i == selected_option else (200, 200, 200)

            text_surface = font.render(option, True, color)

            screen.blit(
                text_surface,
                (
                    WIDTH // 2 - text_surface.get_width() // 2,
                    250 + i * 60
                )
            )
    elif game_state == "pause":
        pause_surface = font.render("PAUSED",True,(255, 255, 0)
        )
        screen.blit(
            pause_surface,
            (
                WIDTH // 2 - pause_surface.get_width() // 2,
                100
            )
        
        )
        for i, option in enumerate(pause_options):

            color = flash_color if i == selected_option else (200, 200, 200)

            text_surface = font.render(option, True, color)

            screen.blit(
                text_surface,
                (
                    WIDTH // 2 - text_surface.get_width() // 2,
                    250 + i * 60
                )
            )  
    # ======================================
    # UPDATE DISPLAY
    # ======================================
    pygame.display.update()
    clock.tick(60)

pygame.quit()
