class bintree:
    def __init__(self):
        self.val = None
        self.left = None
        self.right = None
        self.level = 0
    
    def set_left(self, p_left):
        p_left.level = self.level + 1
        self.left = p_left
        
    def set_right(self, p_right):
        p_right.level = self.level + 1
        self.right = p_right
        
    def leafs(self):
        if self.left == None and self.right == None:
            return [self]
        else:
            left_leafs = self.left.leafs() if self.left != None else []
            right_leafs = self.right.leafs() if self.right != None else []
            return left_leafs + right_leafs