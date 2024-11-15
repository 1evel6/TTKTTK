# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random


# 初始化游戏
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('飞机大战')

# 载入游戏音乐
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 载入背景图
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

# 设置玩家相关参数
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 玩家精灵图片区域
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 定义子弹对象使用的surface相关参数
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 定义敌机对象使用的surface相关参数
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

# 定义新的敌机对象使用的surface相关参数
enemy2_rect = pygame.Rect(0, 0, 72, 90)  # 新敌机的矩形
enemy2_img = plane_img.subsurface(enemy2_rect)  # 新敌机的图像
enemy2_down_imgs = []  # 新敌机下沉时的图像列表
enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(207, 743, 57, 43)))  # 下沉图像1
enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(950, 697, 57, 43)))  # 下沉图像2
enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(300, 296, 57, 43)))  # 下沉图像3
enemy2_down_imgs.append(plane_img.subsurface(pygame.Rect(400, 697, 57, 43)))  # 下沉图像4

enemies2 = pygame.sprite.Group()


enemy3_rect = pygame.Rect(335, 750, 170, 246)
enemy3_img = plane_img.subsurface(enemy3_rect)
enemy3_down_imgs = []
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy3_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies3 = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁精灵动画
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

clock = pygame.time.Clock()

running = True

# 设置文字字体
font = pygame.font.SysFont('Arial', 36)
text_color = (255, 0, 0)
welcome_text = font.render('WELCOME!', True, (255, 255, 255))
quit_text = font.render('press ESC to quit (Quit)', True, (255, 255, 255))
start_text = font.render('PRESS ANY KEY TO START', True, (255, 255, 255))
difficulty_text = pygame.font.SysFont("Arial", 36).render("Press 1 for Easy, 2 for Hard", True, (255, 255, 255))
# 显示初始选项界面
def show_start_screen():
    screen.fill(0)
    screen.blit(background, (0, 0))
    screen.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
    screen.blit(difficulty_text, (SCREEN_WIDTH // 2 - difficulty_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    difficulty = None
    waiting = True
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:  # 按下任意键时退出初始界面
                if event.key == pygame.K_1:
                    difficulty = "easy"  # 选择简单模式
                    waiting = False
                elif event.key == pygame.K_2:
                    difficulty = "hard"  # 选择困难模式
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
    return difficulty

difficulty = show_start_screen()  # 显示初始界面

if difficulty == "easy":
    enemy_frequency = 30  # 简单模式的敌人生成频率
    shoot_frequency1 = 5   # 简单模式下，玩家射击的频率较快
elif difficulty == "hard":
    enemy_frequency = 60  # 困难模式的敌人生成频率
    shoot_frequency1 = 10   # 困难模式下，玩家射击的频率较慢

# 进入游戏循环
shoot_frequency = 0
enemy_frequency = 0
player_down_index = 16
score = 0
clock = pygame.time.Clock()
running = True

while running:
    # 控制游戏最大帧率为60
    clock.tick(45)


    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 用户点击关闭按钮，退出程序
        if event.type == pygame.KEYDOWN:  # 用户按下任意键
            running = True  # 退出初始界面，开始游戏
    # 更新屏幕显示
    pygame.display.flip()
    
    # 控制发射子弹频率,并发射子弹
    if not player.is_hit:
        if shoot_frequency % shoot_frequency1 == 0:
            bullet_sound.play()
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    # 生成敌机
    if enemy_frequency % 50 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    if enemy_frequency % 50 == 0:  # 每100帧生成一次新敌机
        enemy2_pos = [random.randint(0, SCREEN_WIDTH - enemy2_rect.width), 0]
        enemy2 = Enemy(enemy2_img, enemy2_down_imgs, enemy2_pos)
        enemies2.add(enemy2)
    if enemy_frequency % 50 == 0:  # 每100帧生成一次新敌机
        enemy3_pos = [random.randint(0, SCREEN_WIDTH - enemy3_rect.width), 0]
        enemy3 = Enemy(enemy3_img, enemy3_down_imgs, enemy3_pos)
        enemies3.add(enemy3)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0
        

    # 移动子弹，若超出窗口范围则删除
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 移动敌机，若超出窗口范围则删除
    for enemy in enemies1:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)

    for enemy in enemies2:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies2.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies2.remove(enemy)

    for enemy in enemies3:
        enemy.move()
        # 判断玩家是否被击中
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies3.remove(enemy)
            player.is_hit = True
            game_over_sound.play()
            break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies3.remove(enemy)

    # 将被击中的敌机对象添加到击毁敌机Group中，用来渲染击毁动画
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)
    enemies2_down = pygame.sprite.groupcollide(enemies2, player.bullets, 1, 1)
    for enemy_down in enemies2_down:
        enemies_down.add(enemy_down) 
    enemies3_down = pygame.sprite.groupcollide(enemies3, player.bullets, 1, 1)
    for enemy_down in enemies3_down:
        enemies_down.add(enemy_down)    

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
        # 更换图片索引使飞机有动画效果
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # 绘制击毁动画
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 1000
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies1.draw(screen)
    enemies2.draw(screen)
    enemies3.draw(screen)
    # 绘制得分
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10, 10]
    screen.blit(score_text, text_rect)

    # 更新屏幕
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # 监听键盘事件
    key_pressed = pygame.key.get_pressed()
    # 若玩家被击中，则无效
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
