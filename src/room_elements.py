from enum import Enum

from misc import dimensions

class element_type(Enum):
    enemy = 0
    trap = 1
    treasure = 2
    other = 3
    
class room_element:
    def __init__(self):
        self.dims = dimensions()
        self.type = element_type.other
        self.xp_value = 0
        self.name = "NONAME"
        
    def space(self):
        return self.dims.w * self.dims.h
    
class enemy(room_element):
    def __init__(self):
        self.type = element_type.enemy
        
class trap(room_element):
    def __init__(self):
        self.type = element_type.trap
        
class treasure(room_element):
    def __init__(self):
        self.type = element_type.treasure
        self.gp_value = 0