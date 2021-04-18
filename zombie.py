# encoding: utf-8

import pygame
from pygame.sprite import Sprite
from math import atan2, sin, cos
from time import time
from random import random
from settings import Settings, Action


class Zombie(Sprite):
    # 丧尸

    def __init__(self, game, spawn_pos = (-1, -1)):
        super().__init__()
        self.game = game

        # 加载贴图，获取hitbox
        self.image = pygame.image.load(self.game.settings.image_zombie_path)
        self.rect = self.image.get_rect()             # 角色hitbox
        self.screen_rect = game.screen.get_rect()   # 屏幕hitbox

        # 设置初始位置
        if spawn_pos == (-1, -1):
            self.rect.centerx = self.screen_rect.centerx
            self.rect.centery = self.screen_rect.centery
        else:
            self.rect.centerx = spawn_pos[0]
            self.rect.centery = spawn_pos[1]

        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # 生命值
        self.hp = self.game.settings.zombie_default_hp
        self.hp_limit = self.game.settings.zombie_default_hp
        self.alive = True
        
        # 运动状态
        self.speed = self.game.settings.zombie_speed
        self.theta = 0

        self.turn_to((self.game.player.centerx, self.game.player.centery)) 
        self.miss_time = 0
    

    def draw_miss(self):
        # 显示闪避信息

        # 字体设置
        text_color = (20, 20, 20)                      # 设置文本的颜色
        font = pygame.font.SysFont("Courier New", 20)  # 字体
        font.set_bold(True)

        name_str = 'MISS'
        self.name_image = font.render(name_str, True, text_color)
        self.name_rect  = self.name_image.get_rect()
        self.name_rect.left = self.rect.right
        self.name_rect.top  = (self.rect.top + self.rect.centery) // 2
        
        self.game.screen.blit(self.name_image, self.name_rect)


    def draw(self):
        # 绘制角色
        self.game.screen.blit(self.image, self.rect)
        
        # 绘制血条
        hp_gauge_length = self.rect.width
        hp_length = int(self.hp / self.hp_limit * hp_gauge_length)
        pygame.draw.rect(self.game.screen, (0, 128, 0), (self.rect.left, self.rect.top - 10, hp_gauge_length, 8))
        pygame.draw.rect(self.game.screen, (255, 0, 0), \
                         (self.rect.left + hp_gauge_length - hp_length, \
                             self.rect.top - 10, hp_length, 8))
        
        # 显示闪避信息
        if time() - self.miss_time < self.game.settings.zombie_miss_display_duration:
            self.draw_miss()


    def update(self):
        # 更新状态

        # 判断死亡
        if self.hp <= 0:
            self.alive = False
            return

        # 始终朝向玩家
        self.turn_to((self.game.player.centerx, self.game.player.centery)) 

        # 根据运动状态更新位置，加入碰撞检测
        oldx = self.centerx
        oldy = self.centery

        self.centerx += self.speed * cos(self.theta)
        self.centery += self.speed * sin(self.theta)
        
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        self.game.zombies.remove(self)

        if pygame.sprite.spritecollideany(self, self.game.zombies) != None:
            self.rect.centerx   = oldx
            self.centerx        = oldx
            self.rect.centery   = oldy
            self.centery        = oldy

        self.game.zombies.add(self)


        # 运动边界限制，加上后低速无法斜行
        '''
        self.rect.top       = max(self.rect.top,    self.screen_rect.top)
        self.rect.bottom    = min(self.rect.bottom, self.screen_rect.bottom)
        self.rect.left      = max(self.rect.left,   self.screen_rect.left)
        self.rect.right     = min(self.rect.right,  self.screen_rect.right)
        
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        '''
        

    def turn_to(self, pos):
        self.theta = atan2(pos[1] - self.centery, pos[0] - self.centerx)


    def hit_bullet(self, bullet):
        # 概率闪避
        if random() < self.game.settings.zombie_miss_chance:
            # 闪避
            self.miss_time = time()
        else:
            self.hp -= bullet.damage
            if self.hp < 0:
                self.alive = False

