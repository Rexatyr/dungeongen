class dimensions:
    """
    Width/Height pair.
    """
    def __init__():
        self.w = 0
        self.h = 0
        
class point:
    """
    X/Y coordinate.
    """
    def __init__():
        self.x = 0
        self.y = 0
        
def cr(p_xp_amount, p_player_count):
    """
    Returns the specified elements' CR for the specified number of players.
    Note that this always returns an integral CR - CR 1/8 through 1/2 are represented by 
    1-3, all higher values are equivalent to X - 3 as CR.
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