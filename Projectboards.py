import pygame
import random
#pygame initializin
pygame.init()

#display stuff
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#required textures/images
background_img = pygame.image.load('background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_img = pygame.image.load('luce.png')
player_img = pygame.transform.scale(player_img, (50, 50))

laser_img = pygame.image.load('laser.png')
laser_img = pygame.transform.scale(laser_img, (5, 10))

enemy_img = pygame.image.load('light.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))

#you/playing person/player
player_width = player_img.get_width()
player_height = player_img.get_height()
player_x =(SCREEN_WIDTH -player_width)/70
player_y =(SCREEN_HEIGHT -player_height)- 150
player_speed = 5

#pewpew/bullets
laser_speed = 7
lasers = []

#npc
enemy_width = enemy_img.get_width()
enemy_height = enemy_img.get_height()
enemy_x=(SCREEN_WIDTH -enemy_width)/70
enemy_y=(SCREEN_HEIGHT -enemy_height)-1000
enemies = []
enemy_speed = 2

#score/points
score = 0

#display setup panna porom makkale
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Knockoff with Lasers and Light Yagami")

#tharamana bgm
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # -1 will make sure music is looped

#game over bgm 
game_over_music = 'game_over_music.mp3'  

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_lasers(lasers):
    for laser in lasers:
        screen.blit(laser_img, (laser[0], laser[1]))

def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

def check_collision(lasers, enemies):
    global score
    for laser in lasers:
        for enemy in enemies:
            if (laser[0] > enemy[0] and laser[0] < enemy[0] + enemy_width) and \
               (laser[1] > enemy[1] and laser[1] < enemy[1] + enemy_height):
                lasers.remove(laser)
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

    screen.blit(background_img, (0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)

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
            lasers.append([player_x + player_width / 2 - laser_img.get_width() / 2, player_y])

        for laser in lasers:
            laser[1] -= laser_speed
            if laser[1] < 0:
                lasers.remove(laser)
        
        if len(enemies) < 10:
            enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy_y = random.randint(-100, -40)
            enemies.append([enemy_x, enemy_y])

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > SCREEN_HEIGHT:
                enemies.remove(enemy)

        check_collision(lasers, enemies)

        if check_game_over(player_x, player_y, enemies):
            game_over_screen()
            running = False

        screen.blit(background_img, (0, 0))
        draw_player(player_x, player_y)
        draw_lasers(lasers)
        draw_enemies(enemies)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
