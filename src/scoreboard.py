# encoding: utf-8

import pygame
from pygame.sprite import Sprite
from settings import Settings


class Scoreboard(Sprite):
    # 游戏统计信息
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen_rect = self.game.screen.get_rect()

        # 显示得分的字体设置
        self.text_color = (20, 20, 20)                  # 设置文本的颜色
        self.font = pygame.font.SysFont("SimHei", 40)   # 字体为黑体大小为40像素


    def update(self):
        # 将得分转换为图像
        score_str = '得分：' + str(self.game.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # 将得分放到屏幕的右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20   # 与右边差20 像素
        self.score_rect.top   = 70                            # 与顶部差20像素

        highscore_str = '最高分：' + str(self.game.stats.highscore)
        self.highscore_image = self.font.render(highscore_str, True, self.text_color)

        # 将得分放到屏幕的右上角
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.right = self.screen_rect.right - 20   # 与右边差20 像素
        self.highscore_rect.top   = 20                            # 与顶部差20像素


    def draw(self):
        # 在屏幕上显示得分
        #self.update()
        self.game.screen.blit(self.score_image, self.score_rect)
        self.game.screen.blit(self.highscore_image, self.highscore_rect)
