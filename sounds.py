# encoding: utf-8

import pygame
from settings import Settings


class Sounds:
    def __init__(self, game):
        self.game = game
        self.sounds = {}

        for name, path in self.game.settings.sound_path.items():
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(0.2)

        for weapon in self.game.settings.weapons:
            self.sounds[weapon] = pygame.mixer.Sound(self.game.settings.weapons[weapon].sound_path)
            self.sounds[weapon].set_volume(0.2)
    

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
