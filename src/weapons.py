# encoding: utf-8

import pygame
from time import time
from math import sin, cos
from settings import Settings
from bullet import Bullet


class Weapon:
    # 武器，默认生成手枪
    def __init__(self, game, name = 'Pistol'):
        self.game = game
        self.parameters = getattr(self.game.settings.weapons, name, None)
        self.name = name
        self.ammo = self.parameters.ammo_limit    
        self.firing = False
        self.last_fire_time = time() - self.parameters.fire_interval
        self.image = pygame.image.load(self.parameters.image_path)
        self.reload_time = time() - self.parameters.reload_duration
    

    def generate_bullet(self, pos, theta):
        new_bullet = Bullet(self.game, pos, theta, self.parameters.damage, self.parameters.range, self.parameters.speed, self.game.settings.image_bullet_path)
        self.game.bullets.add(new_bullet)
    

    def fire(self, pos, theta):
        if time() > self.last_fire_time + self.parameters.fire_interval:
            self.last_fire_time = time()
            if self.parameters.ammo_limit == -1:
                self.generate_bullet(pos, theta)
                self.game.sounds.play(self.name)
            else:
                if self.ammo > 0:
                    self.ammo -= 1
                    self.generate_bullet(pos, theta)
                    self.game.sounds.play(self.name)
                    if self.ammo == 0:
                        self.reload_time = time()

                elif self.ammo == 0:
                    self.game.sounds.play('dryfire')
            
        #print(len(self.game.bullets.sprites()))


    def update(self):
        # 换弹结束
        if self.ammo == 0 and time() > self.reload_time + self.parameters.reload_duration:
            self.ammo = self.parameters.ammo_limit


class Pistol(Weapon):
    # 手枪，一次一发，射程中等，无限弹药，默认
    def __init__(self, game):
        super().__init__(game)


class Shotgun(Weapon):
    # 霰弹，一次多发，射程较近
    def __init__(self, game):
        super().__init__(game, 'Shotgun')
    

    def generate_bullet(self, pos, theta):
        for theta_offset in [-self.parameters.spread, 0, self.parameters.spread]:
            new_bullet = Bullet(self.game, pos, theta + theta_offset, self.parameters.damage, self.parameters.range, self.parameters.speed, self.game.settings.image_bullet_path)
            self.game.bullets.add(new_bullet)
        #print(len(self.game.bullets.sprites()))


class Laser(Weapon):
    # 霰弹，一次多发，射程较近
    def __init__(self, game):
        super().__init__(game, 'Laser')
    

    def generate_bullet(self, pos, theta):
        for i in range(self.parameters.generate_bullet_number):
            new_pos = (pos[0] + i * self.parameters.generate_bullet_interval * cos(theta), pos[1] + i * self.parameters.generate_bullet_interval * sin(theta))
            new_bullet = Bullet(self.game, new_pos, theta, self.parameters.damage, self.parameters.range, self.parameters.speed, self.game.settings.image_bullet_path)
            self.game.bullets.add(new_bullet)
        #print(len(self.game.bullets.sprites()))