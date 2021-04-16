# encoding: utf-8

import pygame
from pygame.sprite import Sprite
from settings import Settings


class Level_Control(Sprite):
    # 游戏等级、难度调节
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.origial_settings = Settings()
        self.level = 0
        self.screen_rect = self.game.screen.get_rect()

        # 显示字体设置
        self.text_color = (20, 20, 20)                  # 设置文本的颜色
        self.font = pygame.font.SysFont("SimHei", 40)   # 字体为黑体大小为40像素


    def update(self):
        new_level = self.game.stats.score // 1000
        if new_level > self.level:
            # Level up!
            self.level = new_level
            self.game.player.hp_limit   = self.origial_settings.player_default_hp + self.level * 20
            self.game.player.hp         = self.game.player.hp_limit
            self.game.settings.zombie_speed = self.origial_settings.zombie_speed + self.level * 0.1
            self.game.player.speed          = self.origial_settings.player_speed + self.level * 1
            for weapon in self.game.player.weapons:
                weapon.parameters.damage = int(self.origial_settings.weapons[weapon.name].damage * (1 + self.level * 0.1))
        

        level_str = '等级：' + str(self.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        # 将等级放到屏幕的右下角
        self.level_rect         = self.level_image.get_rect()
        self.level_rect.right   = self.screen_rect.right
        self.level_rect.bottom  = self.screen_rect.bottom
    

    def draw(self):
        self.game.screen.blit(self.level_image, self.level_rect)
