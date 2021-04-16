# encoding: utf-8

import pygame
from settings import Settings


class Stats:
    # 游戏状态信息
    def __init__(self, game):
        self.game = game
        self.paused = False
        self.game_over = False
        self.restart = False
        self.score = 0
        self.highscore = 0

        try:
            with open(self.game.settings.score_path, 'r') as score_file:
                self.highscore = int(score_file.read())
        except:
            print('No Score File Found')
    

    def __del__(self):
        with open(self.game.settings.score_path, 'w') as score_file:
            score_file.write(str(self.highscore))
    

    def update(self):
        self.highscore = max(self.highscore, self.score)