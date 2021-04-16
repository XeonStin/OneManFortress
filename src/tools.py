# encoding: utf-8

from math import sqrt
import yaml


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Tools:
    @staticmethod
    def get_distance(pos1, pos2):
        return sqrt( (pos1[0] - pos2[0]) ** 2  +  (pos1[1] - pos2[1]) ** 2 )

    
    @staticmethod
    def dict_to_object(dict_obj):
        if not isinstance(dict_obj, dict):
            return dict_obj
        d = Dict()
        for k, v in dict_obj.items():
            d[k] = Tools.dict_to_object(v)
        return d


    @staticmethod
    def get_dict_from_yaml(path):
        # 读取yaml数据并返回dict
        with open(path, 'r', encoding="utf-8") as fo:
            file_data = fo.read()
            return yaml.load(file_data, Loader=yaml.FullLoader)

