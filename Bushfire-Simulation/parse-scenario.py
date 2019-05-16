def dimension(length):
    ''' A function that calculates the total dimension of the field; coordinate
        of every block. '''
    dimensions = []
    for x in range(length):
        for y in range(length):
            coordinate = [x, y]
            dimensions.append(coordinate)
    return dimensions


def windflow(grid, coordinate, wind):
    ''' A function that calculates additional adjacent cells if there's wind.'''
    cell = []
    wind_adj = []
    x, y = coordinate[0], coordinate[1]
    dimensions = dimension(grid)

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


def ignition(adj_cells, b_grid, h_grid, i, j):
    ''' A function that calculates the iginiton factor. '''
    ignition_factor = 0

    for cells in adj_cells:
        row = cells[0]
        col = cells[1]

        burning = b_grid[row][col]
        height = h_grid[row][col]

        if (burning):
            if (height > h_grid[i][j]):
                ignition_factor += 0.5
            elif (height < h_grid[i][j]):
                ignition_factor += 2
            else:
                ignition_factor += 1
    return ignition_factor


def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
    ''' Main function. Return if cell [i, j] will ignite on t = 1 if the
        conditions at time = 0 is given. '''
    # Checking fuel load
    if (f_grid[i][j] < 1):
        return False

    # Size of the matrix
    grid = len(b_grid)
    # Coordinate of the cell we want to predict
    pair = [i, j]

    # Checks position and determine adjacent cells
    adj_cells = adjacent_cells(grid, pair)

    # Adding the adjacent cells with the wind
    wind_adj = windflow(grid, pair, w_direction)

    for items in wind_adj:
        adj_cells.append(items)

    # Determine the ignition factor
    ignition_factor = ignition(adj_cells, b_grid, h_grid, i, j)

    return ignition_factor >= i_threshold







