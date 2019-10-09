from enum import Enum

from bintree import bintree
from room import room
from misc import dimensions, point

class rejected_exception(Exception): #Raised when a generated dungeon cannot fulfill the requirements defined by the config.
    pass

class generator_config:
    def __init__(self):
        self.dims = dimensions()
        self.min_span = 2 #minimum width/height for any room (after deducting offsets)
        self.corridor_min_width = 1
        self.corridor_max_width = 4 #min/max width for corridors
        self.max_depth = 2 #maximum amount of "splits" in the dungeon tree (higher = more, smaller rooms)
        self.early_stop_chance = 0.1 #chance to stop splitting before reaching max depth. 
        self.early_stop_factor = 2 #factor for early_stop_chance - multiplied with early_stop_chance every level beyond the first
                                   #i.e. with a factor of 2 and a chance of 0.1, level 2 has a stop chance of 0.1 * 2 * 2 = 0.4.
        self.max_attempts = 50 #maximum number of attempts to generate a valid dungeon before quitting
        
class split_types(Enum):
    vertical = 0
    horizontal = 1

def _flip_split_type(p_type):
    return split_types.vertical if p_type == split_types.horizontal else split_types.horizontal

def _pick_split_point(p_span, p_config):
    """
    Picks a point at which to split the specified span into two 'intervals' [a, b) and [b, c).
    Return value is b, i.e. exclusive for first interval, inclusive for second.
    Returns -1 if the span is not wide enough to fit two new rooms with any split.
    """
    #new rooms each need at least p_config.min_span tiles
    if p_span < p_config.min_span * 2:
        return -1
    min = p_config.min_span
    max = p_span - p_config.min_span
    return (min + max) // 2 #TODO return center for now, make random later

def _pick_split_dir(): #TODO make this random
    return split_types.vertical

def _do_split(p_room, p_split_dir, p_config):
    """
    Internal implementation of _split_room in the specified direction.
    """
    room_dims = p_room.dims
    if p_split_dir == split_types.vertical:
        span = room_dims.w
    else:
        span = room_dims.h
    
    split_point = _pick_split_point(span, p_config)
    if split_point == -1:
        return None
    
    topleft = p_room.topleft
    dims = p_room.dims
    first_room = room() #left or top
    second_room = room() #bottom or right
    first_room.topleft = point(topleft.x, topleft.y)
    #remaining properties depend on split direction
    if p_split_dir == split_types.vertical:
        first_room.dims = dimensions(split_point, dims.h)
        second_room.topleft = point(topleft.x + split_point, topleft.y)
        second_room.dims = dimensions(dims.w - split_point, dims.h)
    else:
        first_room.dims = dimensions(dims.w, split_point)
        second_room.topleft = point(topleft.x, topleft.y + split_point)
        second_room.dims = dimensions(dims.w, dims.h - split_point)
    
    return (first_room, second_room)
    
def _split_room(p_room, p_config):
    """
    Split the room into two subrooms. 
    Returns a tuple containing left/right or 
    top/bottom room if successful, None otherwise.
    """
    dir = _pick_split_dir()
    new_rooms = _do_split(p_room, dir, p_config)
    if not new_rooms:
        #cannot split along this axis - try different direction
        new_rooms = _do_split(p_room, _flip_split_type(dir), p_config)
        if not new_rooms:
            #it's hopeless! give up
            return None
    return new_rooms

def _gen_tree_impl(p_tree, p_config):
    """
    Internal implementation of dungeon tree generation.
    """
    if p_tree.level >= p_config.max_depth: #abort if too low in the tree...
        return p_tree
    new_rooms = _split_room(p_tree.val, p_config) #...or splitting is not possible
    if not new_rooms:
        return p_tree
        
    first_room, second_room = new_rooms
        
    left = bintree() #set new room attributes
    right = bintree()
    left.val = first_room
    right.val = second_room
    p_tree.set_left(left)
    p_tree.set_right(right)
    
    _gen_tree_impl(p_tree.left, p_config) #recurse for new child rooms
    _gen_tree_impl(p_tree.right, p_config)
    
def _add_offset_single(p_room, p_config): #TODO make this random
    p_room.offset_left = 1
    p_room.offset_right = 1
    p_room.offset_top = 1
    p_room.offset_bottom = 1
    
def _add_offsets(p_dungeon, p_config):
    """
    Add random offsets from total field dimensions for all leafs of the dungeon tree
    """
    leafs = p_dungeon.leafs()
    for leaf in leafs:
        _add_offset_single(leaf.val, p_config)
    
def _print_room(p_room):
    print("topleft: ({}, {})".format(p_room.topleft.x, p_room.topleft.y))
    print("dims: ({}, {})".format(p_room.dims.w, p_room.dims.h))
    
def _print_tree(p_tree):
    leafs = p_tree.leafs()
    for leaf in leafs:
        _print_room(leaf.val)
        print("")
    
class map:
    def __init__(self, p_dims):
        self.dungeon = bintree()
        root_room = room()
        root_room.dims = p_dims
        self.dungeon.val = root_room
    
    def generate_tree(self, p_config):
        _gen_tree_impl(self.dungeon, p_config)
        _add_offsets(self.dungeon, p_config)
    
    def generate(self, p_config):
        self.generate_tree(p_config)
        
if __name__ == "__main__":
    mymap = map(dimensions(50, 50))
    mymap.generate(generator_config())
    _print_tree(mymap.dungeon)