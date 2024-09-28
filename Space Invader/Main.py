import pygame
import random
import math
from pygame import mixer


# Initialize Pygame
pygame.init()

# Background bg01 - 05
bg = pygame.image.load('img/bg01.jpg')
pygame.display.set_icon(bg)

# Background Sounds
mixer.music.load("sounds/Background.mp3")
mixer.music.play(-1)

# Create the screen
screenWidth = 600
screenHeight = 700
screen = pygame.display.set_mode((screenWidth,screenHeight))

# Title and the Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('img/spaceship.png')
pygame.display.set_icon(icon)

# Player Settings player01 - 05
playerImg = pygame.image.load('img/player1.png')
playerX = (screenWidth / 2) - 32
playerY = screenHeight - 64
playerX_change = 0
playerY_change = 0

# Enemy Settings  enemy01 - 05
enemy_speed = 1
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change =  []

num_of_enemies = 20
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("img/enemy4.png"))
    enemyX.append(random.randint(16,screenWidth - 16))
    enemyY.append(random.randint(0,32))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(16)

# Bullet Settings bullet01 - 05
bulletImg = pygame.image.load('img/bullet04.png')
bullet_speed = 2
bulletX = playerX
bulletY = screenHeight - 64
bulletY_change = -bullet_speed
bullet_state = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf",14)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score: " + str(score_value),True, (255,255,255))
    screen.blit(score, (x,y))

bullets_value = 500
bullets = pygame.font.Font("freesansbold.ttf",14)
bulletsX = screenWidth - 100
bulletsY = 10
def show_bullets(x,y):
    score = bullets.render("Bullets: " + str(bullets_value),True, (255,255,255))
    screen.blit(score, (x,y))

over_font = pygame.font.Font("freesansbold.ttf",48)
def show_game_over():
    game_over = over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(game_over, (screenWidth/2 - 140,screenHeight/2 - 50))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet( x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 24, y))
    screen.blit(bulletImg, (x - 24, y))
    screen.blit(bulletImg, (x + 12, y-12))
    screen.blit(bulletImg, (x - 12, y-12))
    screen.blit(bulletImg, (x, y - 24))
    # screen.blit(bulletImg, (x + 40, y + 8))
    # screen.blit(bulletImg, (x - 40, y + 8))
    # screen.blit(bulletImg, (x - 64, y - 8))
    # screen.blit(bulletImg, (x + 88, y + 8))
    # screen.blit(bulletImg, (x - 88, y + 8))
    # screen.blit(bulletImg, (x + 64, y - 8 ))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    x = enemyX - bulletX
    y = enemyY - bulletY
    distance = math.sqrt(x ** 2 + y ** 2)
    # print(distance)
    if distance <= 25:
        return True

# Game Loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check the pressed arrow key pressed arrow
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_UP:
                playerY_change = 1
            if event.key == pygame.K_DOWN:
                playerY_change = -1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("sounds/Blast.mp3")
                    bullet_sound.play()
                    bullets_value -= 3
                    bulletX = playerX + 24
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screenWidth - 64:
        playerX = screenWidth - 64

    # Enemy Movement
    for i in range(num_of_enemies):
        # Game over
        x = playerX - enemyX[i]
        y = playerY - enemyY[i]
        # if math.sqrt(x ** 2 + y ** 2) <= 1:
        if enemyY[i] >= screenHeight - 100 or  math.sqrt(x ** 2 + y ** 2) <= 10:
            for j in range(num_of_enemies):
                enemyY[j]= 2000
                bulletY= 2000

            show_game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemy_speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screenWidth - 16:
            enemyX_change[i] = -enemy_speed
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = screenHeight - 64
            bullet_state = "ready"
            score_value += 1
            bullets_value += 2
            shoot_sound = mixer.Sound("sounds/Shoot.mp3")
            shoot_sound.play()
            enemyX[i] = random.randint(16, screenWidth - 16)
            enemyY[i] = random.randint(0, 32)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = screenHeight - 64
        bullet_state = "ready"
    if bullet_state ==  "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    show_bullets(bulletsX,bulletsY)
    pygame.display.update()