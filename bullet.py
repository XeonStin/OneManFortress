# encoding: utf-8

import pygame
from pygame.sprite import Sprite
from math import sin, cos, degrees
from tools import Tools
from settings import Settings


class Bullet(Sprite):
    # 子弹

    def __init__(self, game, pos, theta, damage, range_limit, speed, image_path):
        super().__init__()
        self.game = game

        # 加载贴图，获取hitbox
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.rotate(self.image, -degrees(theta))
        self.rect = self.image.get_rect()             # 子弹hitbox
        self.screen_rect = game.screen.get_rect()   # 屏幕hitbox

        # 设置初始位置
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        #self.color = self.settings.bullet_color

        # 运动状态
        self.start_pos = pos
        self.theta = theta
        self.alive = True

        # 子弹特性
        self.damage = damage
        self.range  = range_limit
        self.speed  = speed


    def draw(self):
        # 绘制角色
        self.game.screen.blit(self.image, self.rect)


    def update(self):
        # 根据运动状态更新位置
        self.centerx += self.speed * cos(self.theta)
        self.centery += self.speed * sin(self.theta)

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        if  self.rect.bottom   <   self.screen_rect.top or \
            self.rect.top      >   self.screen_rect.bottom or \
            self.rect.right    <   self.screen_rect.left or \
            self.rect.left     >   self.screen_rect.right or \
            Tools.get_distance(self.start_pos, (self.centerx, self.centery)) > self.range :
            
            self.alive  = False
