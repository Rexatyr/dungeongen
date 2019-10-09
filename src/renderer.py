import pdb

class render:
    def __init__(self):
        self._tile_size = 16
        self._grid_size = 1
        self._tile_colour = 0
        self._grid_colour = 127
        self._bg_colour = 255
        self._border_colour = 64
    
    def _paint_grid(self, p_canvas):
        for i in range(self._tile_size, len(p_canvas), self._tile_size + self._grid_size): 
            p_canvas[i] = [self._grid_colour] * len(p_canvas[i])
        for i in range(self._tile_size, len(p_canvas[0]), self._tile_size + self._grid_size):
            for row in p_canvas:
                row[i] = self._grid_colour
            
    def _paint_tile(self, p_x, p_y, p_canvas, p_colour):
        x_px = p_x * (self._tile_size + self._grid_size)
        y_px = p_y * (self._tile_size + self._grid_size)
        for y in range(y_px, y_px + self._tile_size):
            for x in range(x_px, x_px + self._tile_size):
                p_canvas[y][x] = p_colour
            
    def _paint_room_tile(self, p_x, p_y, p_canvas):
        self._paint_tile(p_x, p_y, p_canvas, self._tile_colour)
        
    def _render_room(self, p_room, p_canvas):
        for y in range(p_room.topleft.y + p_room.offset_top, p_room.topleft.y + p_room.dims.h - p_room.offset_bottom):
            for x in range(p_room.topleft.x + p_room.offset_left, p_room.topleft.x + p_room.dims.w - p_room.offset_right):
                self._paint_room_tile(x, y, p_canvas)
                #p_canvas[y_px : y_px + self._tile_size][x_px : x_px + self._tile_size] = [[self._tile_colour] * self._tile_size] * self._tile_size
                
    def _render_dungeon_rooms(self, p_dungeon, p_canvas):
        self._paint_grid(p_canvas)
        for leaf in p_dungeon.leafs():
            self._render_room(leaf.val, p_canvas)
    
    def _render_border_single(self, p_room, p_canvas):
        #sides
        for y in range(p_room.topleft.y, p_room.topleft.y + p_room.dims.h):
            self._paint_tile(p_room.topleft.x, y, p_canvas, self._border_colour)
            self._paint_tile(p_room.topleft.x + p_room.dims.w - 1, y, p_canvas, self._border_colour)
        #top/bottom
        for x in range(p_room.topleft.x, p_room.topleft.x + p_room.dims.w):
            self._paint_tile(x, p_room.topleft.y, p_canvas, self._border_colour)
            self._paint_tile(x, p_room.topleft.y + p_room.dims.h - 1, p_canvas, self._border_colour)
    
    def _render_borders(self, p_dungeon, p_canvas):
        if p_dungeon == None:
            return
        self._render_border_single(p_dungeon.val, p_canvas)
        self._render_borders(p_dungeon.left, p_canvas)
        self._render_borders(p_dungeon.right, p_canvas)
    
    def render_to_file(self, p_map, p_filename):
        w = p_map.dungeon.val.dims.w
        h = p_map.dungeon.val.dims.h
        w_px = w * self._tile_size + (w - 1) * self._grid_size
        h_px = h * self._tile_size + (h - 1) * self._grid_size
        canvas = []
        for _ in range(h_px):
            canvas.append([self._bg_colour] * w_px)
    
        self._render_dungeon_rooms(p_map.dungeon, canvas)
        self._render_borders(p_map.dungeon, canvas)
        import png
        writer = png.Writer(w_px, h_px, greyscale = True)
        with open(p_filename, "wb") as f:
            writer.write(f, canvas)