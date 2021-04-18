# encoding: utf-8

import sys
import pygame
from pygame.sprite import Group
from random     import random
from settings   import Settings, Action
from tools      import Tools
from stats      import Stats
from scoreboard import Scoreboard
from weapon_ui  import Weapon_UI
from sounds     import Sounds
from player     import Player
from zombie     import Zombie
from level_control import Level_Control


class Game:
    # 游戏类
    def __init__(self):
        # 初始化
        pygame.init()
        
        # 设置
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)

        self.stats      = Stats(self)
        self.sounds     = Sounds(self)

        self.bullets    = Group()           # 创建子弹编组

        self.player     = Player(self)      # 创建玩家

        self.zombies    = Group()           # 创建僵尸组
        #self.zombies.add(Zombie(self, (random()*200, random()*200)))

        self.level_control = Level_Control(self)

        self.ui         = Group()           # 创建UI组
        self.ui.add(Scoreboard(self))       # 向UI组中添加计分板
        self.ui.add(Weapon_UI(self))        # 向UI组中添加武器状态
        self.ui.add(self.level_control)

        self.framerate  = pygame.time.Clock()        # 实例化一个时钟对象

        while True:	
            # 主循环
            self.framerate.tick(60)     # 设置60帧刷新

            self.check_events()

            if self.stats.restart:
                print('Restart')
                break 

            if not self.stats.paused:
                self.update()

                if self.stats.game_over:
                    self.game_over()
                    print('Game Over')
                    break
                
            self.draw()

        with open(self.settings.score_path, 'w') as score_file:
            score_file.write(str(self.stats.highscore))


    def check_events(self):
        # 处理输入事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # 按下按键
                # print('Key pressed: ' + str(event.key) + ', ' + chr(event.key))
                action = self.settings.get_action(event.key)

                # 暂停时不允许处理
                if not self.stats.paused:
                    if action in self.player.move_stat:
                        self.player.move_stat[action] = True
                    '''
                    elif action == Action.fire:
                        self.player.fire()
                    '''
                    if event.key >= 49 and event.key <= 57:
                        self.player.set_weapon(event.key - 48)
                    

                if action == Action.pause:
                    print('Paused')
                    self.stats.paused = not self.stats.paused
                
                elif action == Action.restart:
                    self.stats.restart = True
                    return
                
                elif action == Action.switch_weapon:
                    self.player.switch_weapon()

            elif event.type == pygame.KEYUP:
                # 松开按键
                #print('key pressed')
                action = self.settings.get_action(event.key)
                if action in self.player.move_stat:
                    self.player.move_stat[action] = False

            # 暂停时不允许处理
            if not self.stats.paused:
                if event.type == pygame.MOUSEMOTION:
                    # 移动鼠标
                    #print('mouse motion')
                    self.player.turn_to(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 按下鼠标
                    self.player.firing = True
                    #print(len(self.bullets.sprites()))
                elif event.type == pygame.MOUSEBUTTONUP:
                    # 按下鼠标
                    self.player.firing = False
                    #print(len(self.bulledts.sprites()))


    def draw(self):
        # 更新屏幕缓冲区

        self.screen.blit(self.settings.image_background, [0, 0])

        self.player.draw()

        self.bullets.draw(self.screen)

        for component in self.ui.sprites():
            component.draw()

        for zombie in self.zombies.sprites():
            zombie.draw()
        
        # 更新屏幕
        pygame.display.flip()


    def update(self):
        # 更新对象
        # 补足僵尸
        if len(self.zombies) < self.settings.zombie_number:
            new_zombie = Zombie(self, (random()*200, random()*200))
            if pygame.sprite.spritecollideany(new_zombie, self.zombies) == None:
                self.zombies.add(new_zombie)
        
        # 更新各对象状态
        self.player.update()
        self.bullets.update()
        self.zombies.update()

        # 计算子弹击中僵尸
        bullets_zombies_collisions = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
        
        for bullet, zombies in bullets_zombies_collisions.items():
            for zombie in zombies:
                zombie.hit_bullet(bullet)

        # 去除死亡僵尸
        for zombie in self.zombies.copy():
            if not zombie.alive:
                self.zombies.remove(zombie)
                self.stats.score += self.settings.zombie_kill_score
                
                # 奖励
                if random() < self.settings.zombie_kill_bonus_change:
                    self.player.change_hp(int(self.player.hp_limit * 0.1))


        # 更新最高分
        self.stats.update()

        if not self.player.blink:
            # 计算僵尸碰撞玩家，闪烁时玩家无敌，不计算
            player_zombies_collisions  = pygame.sprite.spritecollideany(self.player, self.zombies)

            if player_zombies_collisions:
                self.player.hit_zombie()
        
        # 判断游戏结束
        if self.player.alive == False:
            self.stats.game_over = True
            return 

        # 去除出界子弹
        for bullet in self.bullets.copy():
            if not bullet.alive:
                self.bullets.remove(bullet)
        
        self.ui.update()


    def soft_reset(self):
        # 重置子弹与僵尸
        self.zombies.empty()
        self.bullets.empty()
        self.player.reset_pos()
    

    def game_over(self):
        # 游戏结束，待完成
        pass
