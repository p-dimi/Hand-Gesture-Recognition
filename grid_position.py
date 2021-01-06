# tracks given hand movement and positions it on the grid

'''
Potential solution to the "skipping location" problem - only allow for a certain maximum of movement consideration,
and if a delta exceeds that - simply do not take that specific delta into account
'''

class GridPos:
    def __init__(self, cols, rows, span = 6, min_move = 7, max_move = 20):
        # span determines over how many frames it considers the movement (5 frames means 4 differences, 1 to 2, 2 to 3, 3 to 4, 4 to 5, for example)
        # min_move determines what is the minimal movement in pixels to consider a position change
        # max_move determines the maximum considered pixel range, to prevent any jumps and skips
        # time_per_tick determines how many X seconds it takes before performing a tick. only considers calculating movement on the grid
        self.cols = cols
        self.rows = rows
        self.span = span
        self.min_move = min_move
        self.max_move = max_move
        
        # stores all positions up to a list length of self.span
        self.positions = []
        
        # considers what was last seen (a closed fist gesture will only be considered if it comes right after an open palm gesture).
        # considers the majority within a list of the length of self.span
        self.last_seen = []
        
        # keeps track of current position on grid
        self.curr_pos = (0,0)
        
        # counts how many ticks (frames) have passed since the last movement action
        self.ticks = 0
        
    def track_position(self, position, last_seen):
        self.positions.append(position)
        self.last_seen.append(last_seen)
        
        if len(self.positions) > self.span:
            del self.positions[0]
        if len(self.last_seen) > self.span:
            del self.last_seen[0]
            
        # iterate ticks
        self.ticks += 1
    
    def get_move(self):
        # movement measured over x and y axes in that order
        avg_x = 0
        avg_y = 0
        
        skip_reduction_x = 0
        skip_reduction_y = 0
        
        for i in range(len(self.positions) - 1):
            # if we go left, the number will be lower (below zero)
            # if we go down, the number will be lower too (below zero)
            dif_x = self.positions[i + 1][0] - self.positions[i][0] 
            dif_y = self.positions[i][1] - self.positions[i + 1][1] 
            
            # check whether the delta is larger than the allowed delta to consider. if it is - reduce 1 from the calculated average divider, and do not consider this delta in the average sum
            if abs(dif_x) > self.max_move:
                skip_reduction_x += 1
                avg_x += 0
            else:
                avg_x += dif_x
            
            if abs(dif_y) > self.max_move:
                skip_reduction_y += 1
                avg_y += 0
            else:
                avg_y += dif_y
            
        # get average of movement across (self.span - 1) number of frames
        if (self.span - 1 - skip_reduction_x) == 0:
            div = 1
        else:
            div = (self.span - 1 - skip_reduction_x)
        
        avg_x = avg_x / div
        
        if (self.span - 1 - skip_reduction_y) == 0:
            div = 1
        else:
            div = (self.span - 1 - skip_reduction_y)
        
        avg_y = avg_y / div
        
        # store movement parameters
        x_movement = 0
        y_movement = 0
        
        # confirm whether movement is counted (by comparing with self.min_move)
        if abs(avg_x) >= self.min_move:
            # we have movement on the x axis. check whether left or right (below or above zero)
            if avg_x > 0:
                # right
                x_movement = 1
            elif avg_x < 0:
                # left
                x_movement = -1
            else:
                # we should not have any instances of avg_x == 0, but just in case include and exception
                x_movement = 0
        
        if abs(avg_y) > self.min_move:
            # we have movement on the y axis
            if avg_y > 0:
                # up
                y_movement = 1
            elif avg_y < 0:
                # down
                y_movement = -1
            else:
                # should not have instances of avg_y == 0, but just in case include an exception
                y_movement = 0
                
        # return tuple of movement, each movement being -1, 0, or 1
        return (x_movement, y_movement)
                
    def move(self, movement_tuple):
        # performs the movement across the defined grid of columns and rows
        x_move, y_move = movement_tuple
        
        current_x, current_y = self.curr_pos
        
        current_x += x_move
        current_y += y_move
        
        # clamp position between the max and min values of the grid
        if current_x >= self.cols:
            current_x = self.cols - 1
        elif current_x < 0:
            current_x = 0
            
        if current_y >= self.rows:
            current_y = self.rows - 1
        elif current_y < 0:
            current_y = 0
            
        self.curr_pos = (current_x, current_y)
        
    def confirm_select(self):
        # confirms selection if one has been made
        # if the last element of last_seen is closed_palm, and most elements beforehand is open_palm, selection is confirmed
        curr_status = self.last_seen[-1]
        
        open_palm = 0
        closed_palm = 0
        none = 0
        for idc in range(len(self.last_seen) - 1):
            if self.last_seen[idc] == 'open':
                open_palm += 1
            elif self.last_seen[idc] == 'closed':
                closed_palm += 1
            elif self.last_seen[idc] == 'NA':
                none += 1
        
        if open_palm > closed_palm and open_palm > none and curr_status == 'closed':
            # if open_palm is the most of all, confirm selection
            return True
        else:
            return False

    def run(self, position, status):
        self.track_position(position, status)
        
        # if ticks reached span size, perform movement and reset ticks
        if self.ticks == self.span:
            movement_tuple = self.get_move()
            self.move(movement_tuple)
            self.ticks = 0
        
        selection = self.confirm_select()
        
        return self.curr_pos, selection
        