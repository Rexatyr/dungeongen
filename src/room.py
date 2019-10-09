from misc import dimensions, point, cr
from room_elements import element_type

class room_contents:
    def __init__(self):
        self.enemies = []
        self.traps = []
        self.treasure = []
        self.other = []

class room:
    def __init__(self):
        self.topleft = point()
        self.dims = dimensions()
        
        self.offset_left = 0 #offsets from "field" size (determine actual room size)
        self.offset_right = 0
        self.offset_top = 0
        self.offset_bottom = 0
        
        self.contents = room_contents()
    
    def add_enemy(self, p_enemy):
        self.contents.enemies.append(p_enemy)
        
    def add_trap(self, p_trap):
        self.contents.traps.append(p_trap)
    
    def add_treasure(self, p_treasure):
        self.contents.treasure.append(p_treasure)
    
    def add_other(self, p_other):
        self.contents.other.append(p_other)
        
    def add_element(self, p_element):
        if p_element.type == element_type.enemy:
            self.add_enemy(p_element)
        elif p_element.type == element_type.trap:
            self.add_trap(p_element)
        elif p_element.type == element_type.treasure:
            self.add_treasure(p_element)
        else:
            self.add_other(p_element)
        
    def eff_width(self):
        """
        Returns width of the actual room (minus horizontal offsets).
        """
        return self.dims.w - self.offset_right - self.offset_left
        
    def eff_height(self):
        """
        Returns height of the actual room (minus vertical offsets).
        """
        return self.dims.h - self.offset_top - self.offset_bottom
    
    def total_space(self):
        """
        Returns total area of the room's area on the map.
        """
        return self.dims.h * self.dims.w
        
    def eff_space(self):
        """
        Returns effective area of the room (disregarding offsets).
        """
        return self.eff_width() * self.eff_height()
        
    def rem_space(self):
        """
        Returns remaining unoccupied space in this room.
        """
        space = self.total_space()
        for enemy in self.contents.enemies:
            space -= enemy.space()
        
        for trap in self.content.traps:
            space -= trap.space()
        
        for treasure in self.contents.treasure:
            space -= treasure.space()
        
        for other in self.contents.other:
            space -= other.space()
            
        return space
    
    def total_cr(self, p_player_count):
        """
        Calculate CR of the entire room.
        """
        total_xp = 0
        total_xp += sum(map(lambda enemy: enemy.xp_value, self.contents.enemies))
        total_xp += sum(map(lambda trap: trap.xp_value, self.contents.traps))
        total_xp += sum(map(lambda treasure: treasure.xp_value, self.contents.treasures))
        total_xp += sum(map(lambda other: other.xp_value, self.contents.other))
        
        return cr(total_xp, p_player_count)