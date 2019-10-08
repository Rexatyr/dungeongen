from enum import Enum

from misc import dimensions

class element_type(Enum):
    enemy = 0
    trap = 1
    treasure = 2
    other = 3
    
class room_element:
    def __init__():
        self.dims = dimensions()
        self.type = element_type.other
        self.xp_value = 0
        self.name = "NONAME"
        
    def space(self):
        return self.dims.w * self.dims.h

def cr(p_xp_amount, p_player_count):
    """
    Returns the specified elements' CR for the specified number of players.
    """
    base_cr_xp = [25, 50, 100, 200, 450,
        700, 1100, 1800, 2300, 2900,
        3900, 5000, 5900, 7200, 8400, 
        10000, 11500, 13000, 15000, 18000, 
        20000, 22000, 25000, 33000, 41000,
        50000, 62000, 75000, 90000, 105000
        120000, 135000, 155000] #cr xp for 4 players
    base_cr_xp = [x for x in map(lambda y: y // 4)] #normalize to 1 player
    
    i = 0
    while i != len(base_cr_xp): #find appropriate cr
        if p_xp_amount <= (base_cr_xp[i] * p_player_count):
            return i + 1
    return len(base_cr_xp) #max cr
    
class enemy(room_element):
    def __init__():
        self.type = element_type.enemy
        
class trap(room_element):
    def __init__():
        self.type = element_type.trap
        
class treasure(room_element):
    def __init__():
        self.type = element_type.treasure
        self.gp_value = 0