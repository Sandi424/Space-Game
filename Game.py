import pygame
import random
import sys
import math
import time

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player setup
player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (64, 64))
player_x = WIDTH // 2 - 32
player_y = HEIGHT - 100
player_speed = 5

# Enemy setup
enemy_img = pygame.image.load('enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (64, 64))
enemies = []
enemy_speed = 0.3
for i in range(6):
    enemies.append([random.randint(0, WIDTH-64), random.randint(50, 150), enemy_speed])

# Bullet setup
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (16, 32))
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"

# Sound
bullet_sound = pygame.mixer.Sound("shoot.wav")
bullet_sound.set_volume(0.5)

score = 0
font = pygame.font.Font(None, 36)
last_key_time = time.time()

# Draw Player
def player(x, y):
    screen.blit(player_img, (x, y))

# Draw Enemy
def enemy(x, y):
    screen.blit(enemy_img, (x, y))

# Fire Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 24, y - 20))

# Collision Check
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distance < 27

# ✅ Enhanced Button Class
class GlowButton:
    def __init__(self, x, y, width, height, text, color, glow_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.glow_color = glow_color
        self.glow_alpha = 0
        self.hover = False
        self.font = pygame.font.Font(None, 40)
        
    def draw(self, surface):
        # Glow Effect
        if self.hover:
            self.glow_alpha = min(self.glow_alpha + 15, 100)
            glow_surf = pygame.Surface((self.rect.width+40, self.rect.height+40), pygame.SRCALPHA)
            pygame.draw.ellipse(glow_surf, (*self.glow_color, self.glow_alpha), glow_surf.get_rect())
            surface.blit(glow_surf, (self.rect.x-20, self.rect.y-20))
        else:
            self.glow_alpha = max(self.glow_alpha - 15, 0)
        
        # Button Base
        pygame.draw.rect(surface, self.color, self.rect, border_radius=25)
        pygame.draw.rect(surface, WHITE, self.rect, 3, border_radius=25)
        
        # Text
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover


def draw_start_screen():
    screen.fill(BLACK)
    
    # Title
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("SPACE INVADER", True, WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 150))
    
    # Create Button
    start_btn = GlowButton(
        x=WIDTH//2 - 150, 
        y=HEIGHT//2 - 40, 
        width=300, 
        height=80,
        text="START GAME",
        color=(0, 150, 0),
        glow_color=(0, 255, 0)
    )
    
    mouse_pos = pygame.mouse.get_pos()
    start_btn.check_hover(mouse_pos)
    start_btn.draw(screen)
    
    pygame.display.update()
    return start_btn.rect


def quit_popup():
    popup_width, popup_height = 420, 220
    popup_rect = pygame.Rect(WIDTH//2 - popup_width//2, HEIGHT//2 - popup_height//2, popup_width, popup_height)
    
    # Create Buttons
    yes_btn = GlowButton(
        x=WIDTH//2 - 130, 
        y=HEIGHT//2 + 30, 
        width=110, 
        height=50,
        text="YES",
        color=(0, 150, 0),
        glow_color=(0, 255, 0)
    )
    
    no_btn = GlowButton(
        x=WIDTH//2 + 20, 
        y=HEIGHT//2 + 30, 
        width=110, 
        height=50,
        text="NO",
        color=(150, 0, 0),
        glow_color=(255, 0, 0)
    )
    
    while True:
        screen.fill(BLACK)
        

        pygame.draw.rect(screen, (30, 30, 30), popup_rect, border_radius=20)
        pygame.draw.rect(screen, WHITE, popup_rect, 3, border_radius=20)
        
        # Title
        title_font = pygame.font.Font(None, 38)
        msg = title_font.render("Do you want to quit the game?", True, WHITE)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 50))
        
        # Handle Buttons
        mouse_pos = pygame.mouse.get_pos()
        yes_btn.check_hover(mouse_pos)
        no_btn.check_hover(mouse_pos)
        
        yes_btn.draw(screen)
        no_btn.draw(screen)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_btn.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif no_btn.rect.collidepoint(event.pos):
                    return


game_started = False
running = True
last_key_time = time.time()

while running:
    if not game_started:
        button_rect = draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_started = True
        continue

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if any(keys):
        last_key_time = time.time()

    if keys[pygame.K_q]:
        quit_popup()

    # Player movement
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Fire bullet
    if keys[pygame.K_SPACE]:
        if bullet_state == "ready":
            bullet_x = player_x
            bullet_y = player_y
            bullet_sound.play()
            fire_bullet(bullet_x, bullet_y)

    # Auto quit popup if idle for 5 seconds
    if time.time() - last_key_time > 5:
        quit_popup()
        last_key_time = time.time()

    # Boundaries for player
    if player_x <= 0:
        player_x = 0
    if player_x >= WIDTH - 64:
        player_x = WIDTH - 64

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_state = "ready"

    # Enemy movement and collision
    for i in range(len(enemies)):
        enemies[i][0] += enemies[i][2]
        if enemies[i][0] <= 0 or enemies[i][0] >= WIDTH - 64:
            enemies[i][2] *= -1
            enemies[i][1] += 30

        enemy(enemies[i][0], enemies[i][1])

        if is_collision(enemies[i][0], enemies[i][1], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemies[i][0] = random.randint(0, WIDTH-64)
            enemies[i][1] = random.randint(50, 150)

    player(player_x, player_y)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.update()
