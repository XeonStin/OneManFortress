# encoding: utf-8

import pygame
from pygame.sprite import Sprite
from settings import Settings


class Weapon_UI(Sprite):
    # 武器部分UI
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen_rect = self.game.screen.get_rect()

        # 显示得分的字体设置
        self.text_color = (20, 20, 20)                      # 设置文本的颜色
        self.font = pygame.font.SysFont("Courier New", 40)  # 字体


    def update(self):
        # 显示武器图片
        self.weapon_image   = self.game.player.weapons[self.game.player.current_weapon_id].image
        self.weapon_rect    = self.weapon_image.get_rect()
        self.weapon_rect.left   = self.screen_rect.left
        self.weapon_rect.bottom = self.screen_rect.bottom


        # 显示弹药量
        ammo_str = '{:4d}/{:4d}'.format(self.game.player.weapons[self.game.player.current_weapon_id].ammo, self.game.player.weapons[self.game.player.current_weapon_id].parameters.ammo_limit)
        self.ammo_image = self.font.render(ammo_str, True, self.text_color)
        self.ammo_rect = self.ammo_image.get_rect()
        self.ammo_rect.left     = self.weapon_rect.right
        self.ammo_rect.bottom   = self.screen_rect.bottom

        # 显示名称
        name_str = self.game.player.weapons[self.game.player.current_weapon_id].name
        self.name_image = self.font.render(name_str, True, self.text_color)
        self.name_rect = self.name_image.get_rect()
        self.name_rect.right    = self.ammo_rect.right
        self.name_rect.bottom   = self.ammo_rect.top


    def draw(self):
        # 在屏幕上显示
        #self.update()
        self.game.screen.blit(self.weapon_image , self.weapon_rect)
        self.game.screen.blit(self.name_image   , self.name_rect)
        self.game.screen.blit(self.ammo_image   , self.ammo_rect)
