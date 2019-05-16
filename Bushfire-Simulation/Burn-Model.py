from reference import check_ignition


def dimension(length):
    ''' A function that calculates the total dimension of the field; coordinate
        of every block. '''
    dimensions = []
    for x in range(length):
        for y in range(length):
            coordinate = [x, y]
            dimensions.append(coordinate)
    return dimensions


def burn_state(grid, burn_seeds):
    '''A function which determines the current burning state of the grid'''
    state = []
    row_list = []
    # First create the whole grid with all the boolean set to False
    for row in range(grid):
        row_list = []
        for col in range(grid):
            row_list.append(False)
        state.append(row_list)
    # Changes the value to True to show that cell is burning
    for items in burn_seeds:
        x = items[0]
        y = items[1]
        state[x][y] = True
    
    return state


def windflow(grid, coordinate, wind):
    ''' A function that calculates additional adjacent cells if there's wind.
        '''
    cell = []
    wind_adj = []
    x, y = coordinate[0], coordinate[1]
    dimensions = dimension(grid)
    
    # Check for different wind directions and adject cell accordingly
    if (wind == 'N'):
        for i in range(y - 1, y + 2):
            pair = [x - 2, i]
            cell.append(pair)
    elif (wind == 'S'):
        for i in range(y - 1, y + 2):
            pair = [x + 2, i]
            cell.append(pair)
    elif (wind == 'E'):
        for i in range(x - 1, x + 2):
            pair = [i, y + 2]
            cell.append(pair)
    elif (wind == 'W'):
        for i in range(x - 1, x + 2):
            pair = [i, y - 2]
            cell.append(pair)
    elif (wind == 'NW'):
        cell.append([x - 1, y - 2])
        cell.append([x - 2, y - 2])
        cell.append([x - 2, y - 1])
    elif (wind == 'NE'):
        cell.append([x - 1, y + 2])
        cell.append([x - 2, y + 2])
        cell.append([x - 2, y + 1])
    elif (wind == 'SE'):
        cell.append([x + 1, y + 2])
        cell.append([x + 2, y + 2])
        cell.append([x + 2, y + 1])
    elif (wind == 'SW'):
        cell.append([x + 1, y - 2])
        cell.append([x + 2, y - 2])
        cell.append([x + 2, y - 1])
    
    # If the wind adjacent cells exists within the dimension, adds it to the
    # final list
    for item in cell:
        if item in dimensions:
            wind_adj.append(item)

return wind_adj


def adjacent_cells(grid, pair):
    ''' Calculate the adjacent cell of the target the cell. '''
    adjacent_cells = []
    dimensions = dimension(grid)
    i = pair[0]
    j = pair[1]
    
    # Determining all possible adjacent cells around target cell
    possible_cells = []
    for a in range(i - 1, i + 2):
        for b in range(j - 1, j + 2):
            ad_pair = [a, b]
            possible_cells.append(ad_pair)
    possible_cells.remove(pair)
    for items in possible_cells:
        if items in dimensions:
            adjacent_cells.append(items)

return adjacent_cells


def all_adjacent(grid, pair, wind):
    ''' Considers the wind direction and returns all the adjacent cells.'''
    adj_cells = adjacent_cells(grid, pair)
    wind_adj = windflow(grid, pair, wind)
    
    # Updates the wind factor to initial adjacent cells
    for items in wind_adj:
        adj_cells.append(items)
    
    return adj_cells


def ignition(adj_cells, b_grid, h_grid, i, j):
    ''' A function that calculates the iginiton factor of a burning cell '''
    ignition_factor = 0
    
    for cells in adj_cells:
        row = cells[0]
        col = cells[1]
        
        burning = b_grid[row][col]
        height = h_grid[row][col]
        
        # if the adjacent cell is burning then include it the ignition factor
        if (burning):
            if (height > h_grid[i][j]):
                ignition_factor += 0.5
            elif (height < h_grid[i][j]):
                ignition_factor += 2
            else:
                ignition_factor += 1
    return ignition_factor


def new_state(f_grid, burn_seeds):
    ''' A function which calculates the fuel load at t = t + 1. '''
    for cells in burn_seeds:
        x, y = cells[0], cells[1]
        
        if (f_grid[x][y] > 0):
            f_grid[x][y] -= 1
    return f_grid


def current_burn(grid, b_grid, f_grid, h_grid, i_threshold, w_direction,
                 burn_seeds):
    ''' A function which returns the cells which ignite at t = t + 1.
        '''
    # List to hold the possible burning cells
    possible_burn = []
    # List that holds the cells burning at t = t + 1
    now_burning = []
    for cells in burn_seeds:
        item = list(cells)
        adj_cells = all_adjacent(grid, item, w_direction)
        for items in adj_cells:
            if items not in possible_burn:
                possible_burn.append(items)

# Check which cells are burning
for cells in possible_burn:
    i, j = cells[0], cells[1]
    
    if (not b_grid[i][j]):
        state = check_ignition(b_grid, f_grid, h_grid, i_threshold,
                               w_direction, i, j)
                               if (b_grid[i][j] != state):
                                   now_burning.append([i, j])

return now_burning


def update_seeds(f_grid, burn_seeds, current):
    ''' A function to return the new burning seeds at time t = t + 1
        '''
    
    new_burn = []
    for items in burn_seeds:
        a, b = items[0], items[1]
        
        # Check its fuel load state
        if (f_grid[a][b] > 0):
            new_burn.append((a, b))

for items in current:
    new_burn.append(tuple(items))
    
    return new_burn


def burn_dict(dictionary, burn_seeds):
    ''' A function which counts the new burned cell and add it to the existing
        dictionary. '''
    for cells in burn_seeds:
        dictionary[cells] = 1
    return dictionary


def run_model(f_grid, h_grid, i_threshold, w_direction, burn_seeds):
    ''' Main function which gives the final state of the grid. '''
    # Calculate the Dimension
    grid = len(f_grid)
    
    # A dictionary which will contain all the burned cells including the
    # intial burn seeds
    burned_dict = {}
    
    # Run an infinite loop until there are no burning cells
    while True:
        # Check the current buring state of the grid
        b_grid = burn_state(grid, burn_seeds)
        
        # Determining the current fuel load
        f_grid = new_state(f_grid, burn_seeds)
        
        # Monitoring the total cells that have burned during model
        burned_dict = burn_dict(burned_dict, burn_seeds)
        
        # Calculate the burning cells at time t = t + 1
        currently_burning = current_burn(grid, b_grid, f_grid, h_grid,
                                         i_threshold, w_direction, burn_seeds)
            
                                         # Update burn seeds
                                         burn_seeds = update_seeds(f_grid, burn_seeds, currently_burning)
                                         
                                         # If no cells burning, exit loop
                                         if (len(burn_seeds) == 0):
                                             break

# Final state is final fuel load and number of cell burned in the process
final_state = (f_grid, len(burned_dict))
return final_state
