# encoding: utf-8

import pygame
from enum import Enum, unique
from tools      import Tools, Dict


@unique
class Action(Enum):
    undefined   = -1
    move_up     = 0
    move_down   = 1
    move_left   = 2
    move_right  = 3
    fire        = 4
    restart     = 5
    pause       = 6
    switch_weapon = 7


class Settings:
    def __init__(self):

        # 键位设置
        self.key_remapping_dict = {
            ord('w')        : Action.move_up, 
            ord('a')        : Action.move_left, 
            ord('s')        : Action.move_down,
            ord('d')        : Action.move_right, 
            pygame.K_UP     : Action.move_up,
            pygame.K_DOWN   : Action.move_down,
            pygame.K_LEFT   : Action.move_left,
            pygame.K_RIGHT  : Action.move_right,
            ord(' ')        : Action.fire,
            ord('r')        : Action.restart,
            ord('p')        : Action.pause,
            ord('q')        : Action.switch_weapon
        }

        for k, v in Tools.dict_to_object( Tools.get_dict_from_yaml('./setting/settings.yaml') ).items():
            setattr(self, k, v)

        self.image_background = pygame.image.load(self.image_background_path)
            #print(k, v)

    
    def get_action(self, key):
        return self.key_remapping_dict.get(key, -1)

