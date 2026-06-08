import pygame
import sys

# Main settings
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3Saints and 3Monsters:)")
clock = pygame.time.Clock()

# Colors
RIVER_BLUE = (70, 130, 180)
GRASS_GREEN = (34, 139, 34)
BOAT_BROWN = (139, 69, 19)
TEXT_WHITE = (255, 255, 255)
LOSE_RED = (200, 0, 0)

# Sprites
try:
    saint_img = pygame.image.load("saint.png").convert_alpha()
    monster_img = pygame.image.load("monster.png").convert_alpha()
    saint_img = pygame.transform.scale(saint_img, (50, 75))
    monster_img = pygame.transform.scale(monster_img, (50, 75))
except:
    print("Error: Missing 'saint.png' or 'monster.png' in game directory!")
    pygame.quit()
    sys.exit()

# State variables
left_bank = [3, 3]  # [Saints, Monsters]
right_bank = [0, 0]
boat = []
boat_side = "left"
game_state = "PLAYING" # Options: "PLAYING", "WIN", "LOSE"

def reset_match():
    global left_bank, right_bank, boat, boat_side, game_state
    left_bank = [3, 3]
    right_bank = [0, 0]
    boat = []
    boat_side = "left"
    game_state = "PLAYING"

while True:
    screen.fill(RIVER_BLUE)
    
    # --- Input Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            # If the match ended, only accept restart commands
            if game_state in ["WIN", "LOSE"]:
                if event.key == pygame.K_r:
                    reset_match()
                continue
            
            # Active game controls
            current_bank = left_bank if boat_side == "left" else right_bank
            
            if event.key == pygame.K_s:  # Load Saint
                if len(boat) < 2 and current_bank[0] > 0:
                    current_bank[0] -= 1
                    boat.append('S')
                    
            elif event.key == pygame.K_m:  # Load Monster
                if len(boat) < 2 and current_bank[1] > 0:
                    current_bank[1] -= 1
                    boat.append('M')
                    
            elif event.key == pygame.K_x:  # Unload character
                if boat:
                    dropped = boat.pop()
                    if dropped == 'S':
                        current_bank[0] += 1
                    elif dropped == 'M':
                        current_bank[1] += 1
                        
            elif event.key == pygame.K_SPACE:  # Cross river
                if boat:
                    boat_side = "right" if boat_side == "left" else "left"

    # --- Game Logic & Rules Checking ---
    if game_state == "PLAYING":
        # Account for boat occupants depending on where the boat currently sits
        left_s = left_bank[0] + (boat.count('S') if boat_side == "left" else 0)
        left_m = left_bank[1] + (boat.count('M') if boat_side == "left" else 0)
        
        right_s = right_bank[0] + (boat.count('S') if boat_side == "right" else 0)
        right_m = right_bank[1] + (boat.count('M') if boat_side == "right" else 0)
        
        # Check Win
        if right_s == 3 and right_m == 3:
            game_state = "WIN"
        # Check Loss
        elif (left_s > 0 and left_m > left_s) or (right_s > 0 and right_m > right_s):
            game_state = "LOSE"

    # --- Graphics Rendering ---
    # Banks
    pygame.draw.rect(screen, GRASS_GREEN, (0, 0, 200, HEIGHT))
    pygame.draw.rect(screen, GRASS_GREEN, (600, 0, 200, HEIGHT))
    
    # Boat position math
    boat_x = 210 if boat_side == "left" else 470
    pygame.draw.rect(screen, BOAT_BROWN, (boat_x, 420, 120, 40))
    
    # Instructions HUD
    if game_state == "PLAYING":
        font = pygame.font.SysFont(None, 24)
        hud = font.render("S: Load Saint | M: Load Monster | X: Unload | SPACE: Cross", True, TEXT_WHITE)
        screen.blit(hud, (130, 20))
        
    # Draw everyone on shores
    for i in range(left_bank[0]):
        screen.blit(saint_img, (20, 100 + i * 110))
    for i in range(left_bank[1]):
        screen.blit(monster_img, (110, 100 + i * 110))
        
    for i in range(right_bank[0]):
        screen.blit(saint_img, (620, 100 + i * 110))
    for i in range(right_bank[1]):
        screen.blit(monster_img, (710, 100 + i * 110))
        
    # Draw everyone in the boat
    for i, passenger in enumerate(boat):
        img = saint_img if passenger == 'S' else monster_img
        screen.blit(img, (boat_x + 10 + i * 55, 350))
        
    # --- Game Over Overlay Screen ---
    if game_state in ["WIN", "LOSE"]:
        # Translucent backdrop blackout
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        main_font = pygame.font.SysFont(None, 50)
        sub_font = pygame.font.SysFont(None, 30)
        
        if game_state == "WIN":
            title = main_font.render("YOU WIN! Everyone made it over.", True, TEXT_WHITE)
        else:
            title = main_font.render("GAME OVER! The saints got eaten.", True, LOSE_RED)
            
        sub = sub_font.render("Press 'R' to Play Again  |  'ESC' to Exit", True, TEXT_WHITE)
        
        # Center the text targets nicely
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 20))
        
    pygame.display.flip()
    clock.tick(60)