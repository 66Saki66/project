import pygame
import random
#pygame initializin
pygame.init()

#display stuff
screen_width = 800
screen_height= 600

#colors
blk = (0, 0, 0)
white = (255, 255, 255)

#required textures/images
bg_img = pygame.image.load('background.png')
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load('luce.png')
player_img = pygame.transform.scale(player_img, (25, 25))

ammo_img = pygame.image.load('laser.png')
ammo_img = pygame.transform.scale(ammo_img, (2, 6))

enemy_img = pygame.image.load('light.png')
enemy_img = pygame.transform.scale(enemy_img, (25, 25))

#you/playing person/player
player_width = player_img.get_width()
player_height = player_img.get_height()
player_x =(screen_width -player_width)/70
player_y =(screen_height -player_height)- 150
player_speed = 5

#pewpew/bullets
ammo_speed = 7
ammos = []

#npc
enemy_width = enemy_img.get_width()
enemy_height = enemy_img.get_height()
enemy_x=(screen_width -enemy_width)/70
enemy_y=(screen_height -enemy_height)-1000
enemies = []
enemy_speed = 2

#score/points
score = 0

#display setup panna porom makkale
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("One piece invaders")

#tharamana bgm
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # -1 will make sure music is looped

#game over bgm 
game_over_music = 'game_over_music.mp3'  

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
#creating custom functions to create images
def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_lasers(ammos):
    for laser in ammos:
        screen.blit(ammo_img, (laser[0], laser[1]))

def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

def check_collision(ammos, enemies):
    global score
    for laser in ammos:
        for enemy in enemies:
            if (laser[0] > enemy[0] and laser[0] < enemy[0] + enemy_width) and \
               (laser[1] > enemy[1] and laser[1] < enemy[1] + enemy_height):
                ammos.remove(laser)
                enemies.remove(enemy)
                score += 1
                break

def check_game_over(player_x, player_y, enemies):
    for enemy in enemies:
        if (player_x < enemy[0] + enemy_width and player_x + player_width > enemy[0]) and \
           (player_y < enemy[1] + enemy_height and player_y + player_height > enemy[1]):
            return True
    return False

def game_over_screen():
    pygame.mixer.music.stop()
    pygame.mixer.music.load(game_over_music)
    pygame.mixer.music.play()

    screen.blit(bg_img, (0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, white)
    screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)
#main loop for control and working of game
def main():
    global player_x, score
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            lasers.append([player_x + player_width / 2 - ammo_img.get_width() / 2, player_y])

        for laser in ammos:
            laser[1] -= ammo_speed
            if laser[1] < 0:
                ammos.remove(laser)
        
        if len(enemies) < 10:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(-100, -40)
            enemies.append([enemy_x, enemy_y])

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > screen_height:
                enemies.remove(enemy)

        check_collision(ammos, enemies)

        if check_game_over(player_x, player_y, enemies):
            game_over_screen()
            running = False

        screen.blit(bg_img, (0, 0))
        draw_player(player_x, player_y)
        draw_lasers(lasers)
        draw_enemies(enemies)

        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
