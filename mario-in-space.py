import pygame  # Pygame Library for game development
import os  # Operating System module for file operations

# Initialize Pygame and font module and sound effects
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Define game window dimensions and title
WIDTH, HEIGHT = 1000, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario In Space")

# Define colors in RGB format
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define a border for the game window
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Load sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','sounds', 'bullet hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','sounds', 'bullet fire.mp3'))                                   

# Load a custom font for displaying health (ensure the font file exists in the given path)
HEALTH_FONT = pygame.font.Font(os.path.join('Assets', 'Font', 'SuperMario256.ttf'), 40)

# Game constants
FPS = 60
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 5
MARIO_WIDTH, MARIO_HEIGHT = 200, 200
BOO_WIDTH, BOO_HEIGHT = 200, 200

# Custom events for player hits
MARIO_HIT = pygame.USEREVENT + 1
BOO_HIT = pygame.USEREVENT + 2

# Load game assets (players, bullets, background)
MARIO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Players', 'mario.png')), (MARIO_WIDTH, MARIO_HEIGHT))
BOO_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Players', 'boo.png')), (BOO_WIDTH, BOO_HEIGHT))
MARIO_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'Weapons', 'Mario Weapon.png'))
BOO_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'Weapons', 'Boo Weapon.png'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background', 'space background.jpg')), (WIDTH, HEIGHT))

# Function to draw the game window
def draw_window(mario_rect, boo_rect, mario_bullets, boo_bullets, mario_health, boo_health):
    win.blit(SPACE, (0, 0))
    pygame.draw.rect(win, BLACK, BORDER)
    
    mario_health_text = HEALTH_FONT.render(f"Mario Health: {mario_health}", 1, WHITE)
    boo_health_text = HEALTH_FONT.render(f"Boo Health: {boo_health}", 1, WHITE)
    win.blit(mario_health_text, (WIDTH - mario_health_text.get_width() - 10, 10))
    win.blit(boo_health_text, (10, 10))
    
    win.blit(MARIO_IMAGE, mario_rect)
    win.blit(BOO_IMAGE, boo_rect)
    
    for bullet in mario_bullets:
        win.blit(MARIO_BULLET_IMAGE, (bullet.x, bullet.y))
    for bullet in boo_bullets:
        win.blit(BOO_BULLET_IMAGE, (bullet.x, bullet.y))
    
    pygame.display.update()

# Functions to handle player movement
def handle_movement(keys_pressed, rect, left_key, right_key, up_key, down_key, boundary):
    if keys_pressed[left_key] and rect.x - VEL > boundary[0]:  # Move left
        rect.x -= VEL
    if keys_pressed[right_key] and rect.x + VEL + rect.width < boundary[1]:  # Move right
        rect.x += VEL
    if keys_pressed[up_key] and rect.y - VEL > boundary[2]:  # Move up
        rect.y -= VEL
    if keys_pressed[down_key] and rect.y + VEL + rect.height < boundary[3]:  # Move down
        rect.y += VEL

# Function to handle bullets movement and collisions
def handle_bullets(mario_bullets, boo_bullets, mario_rect, boo_rect):
    for bullet in mario_bullets:
        bullet.x += BULLETS_VEL
        if bullet.colliderect(boo_rect):
            pygame.event.post(pygame.event.Event(BOO_HIT))
            mario_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            mario_bullets.remove(bullet)

    for bullet in boo_bullets:
        bullet.x -= BULLETS_VEL
        if bullet.colliderect(mario_rect):
            pygame.event.post(pygame.event.Event(MARIO_HIT))
            boo_bullets.remove(bullet)
        elif bullet.x < 0:
            boo_bullets.remove(bullet)

# Function to display the winner text
def draw_winner(text):
    font = pygame.font.Font(os.path.join('Assets', 'Font', 'SuperMario256.ttf'), 40)
    draw_text = font.render(text, 1, WHITE)
    win.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

# Main game function
def main():
    mario_rect = pygame.Rect(100, 300, MARIO_WIDTH, MARIO_HEIGHT)
    boo_rect = pygame.Rect(700, 300, BOO_WIDTH, BOO_HEIGHT)
    
    mario_bullets = []
    boo_bullets = []
    
    mario_health = 10
    boo_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(mario_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(mario_rect.x + MARIO_WIDTH, mario_rect.y + MARIO_HEIGHT // 2 - 5, MARIO_BULLET_IMAGE.get_width(), MARIO_BULLET_IMAGE.get_height())
                    mario_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(boo_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(boo_rect.x, boo_rect.y + BOO_HEIGHT // 2 - 5, BOO_BULLET_IMAGE.get_width(), BOO_BULLET_IMAGE.get_height())
                    boo_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == MARIO_HIT:
                mario_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == BOO_HIT:
                boo_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if mario_health <= 0:
            winner_text = "Boo wins!"
        if boo_health <= 0:
            winner_text = "Mario wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, mario_rect, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, (0, BORDER.x, 0, HEIGHT))
        handle_movement(keys_pressed, boo_rect, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, (BORDER.x + BORDER.width, WIDTH, 0, HEIGHT))
        
        handle_bullets(mario_bullets, boo_bullets, mario_rect, boo_rect)
        draw_window(mario_rect, boo_rect, mario_bullets, boo_bullets, mario_health, boo_health)
    
    main()

if __name__ == "__main__":
    main()
