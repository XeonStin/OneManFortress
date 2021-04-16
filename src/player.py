# encoding: utf-8

import pygame
from pygame.sprite import Sprite
from time import time
from math import atan2
from settings import Settings, Action
from weapons import *


class Player(Sprite):
    # 玩家

    def __init__(self, game):
        super().__init__()
        self.game = game

        # 加载贴图，获取hitbox
        self.image = pygame.image.load(self.game.settings.image_player_path)
        self.rect = self.image.get_rect()             # 角色hitbox
        self.screen_rect = game.screen.get_rect()   # 屏幕hitbox

        # 设置初始位置
        self.reset_pos()
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        # 生命值
        self.hp = self.game.settings.player_default_hp
        self.hp_limit = self.game.settings.player_default_hp
        self.alive = True

        # 武器状态
        self.weapons = [Pistol(game), Shotgun(game), Laser(game)]
        self.current_weapon_id = 0
        self.firing = False

        # 闪烁状态
        self.blink = False
        self.blink_start_time = 0

        # 运动状态
        self.speed = self.game.settings.player_speed
        self.theta = 0

        self.move_stat = {
            Action.move_up     : False,
            Action.move_down   : False,
            Action.move_left   : False,
            Action.move_right  : False
        }
        
        self.key_to_move_dict_x = {
            Action.move_left   : -1., 
            Action.move_right  :  1.
        }

        self.key_to_move_dict_y = {
            Action.move_up     : -1., 
            Action.move_down   :  1.
        }


    def draw(self):
        # 绘制角色
        if self.blink:
            # 使角色闪烁
            current_time = time()
            if current_time > self.blink_start_time + self.game.settings.player_blink_duration:
                self.blink = False
            elif int(current_time * 200) % 100 < 50:
                self.game.screen.blit(self.image, self.rect)
        else:
            self.game.screen.blit(self.image, self.rect)
        
        # 绘制血条
        hp_gauge_length = self.rect.width
        hp_length = int(self.hp / self.hp_limit * hp_gauge_length)
        pygame.draw.rect(self.game.screen, (0, 128, 0), (self.rect.left, self.rect.top - 10, hp_gauge_length, 8))
        pygame.draw.rect(self.game.screen, (255, 0, 0), \
                         (self.rect.left + hp_gauge_length - hp_length, \
                             self.rect.top - 10, hp_length, 8))


    def update(self):
        # 根据运动状态更新位置
        for key, stat in self.move_stat.items():
            #print(key, stat)
            if stat:
                self.centerx += self.key_to_move_dict_x.get(key, 0.) * self.speed
                self.centery += self.key_to_move_dict_y.get(key, 0.) * self.speed

        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        # 运动边界限制
        self.rect.top       = max(self.rect.top,    self.screen_rect.top)
        self.rect.bottom    = min(self.rect.bottom, self.screen_rect.bottom)
        self.rect.left      = max(self.rect.left,   self.screen_rect.left)
        self.rect.right     = min(self.rect.right,  self.screen_rect.right)
        
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        if self.firing:
            self.fire()
        
        self.weapons[self.current_weapon_id].update()

    
    def reset_pos(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery


    def turn_to(self, pos):
        self.theta = atan2(pos[1] - self.centery, pos[0] - self.centerx)

    
    def switch_weapon(self, delta = 1):
        self.current_weapon_id += delta
        self.current_weapon_id %= len(self.weapons)


    def fire(self):
        self.weapons[self.current_weapon_id].fire((self.centerx, self.centery), self.theta)


    def change_hp(self, delta):
        self.hp += delta
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        self.hp = min(self.hp, self.hp_limit)


    def hit_zombie(self):
        self.change_hp(-self.game.settings.zombie_damage)
        if self.hp > 0:
            self.game.soft_reset()
            # 使玩家闪烁
            self.blink = True
            self.blink_start_time = time()


    def set_weapon(self, index):
        index -= 1
        if index >= 0 and index < len(self.weapons):
            self.current_weapon_id = index

