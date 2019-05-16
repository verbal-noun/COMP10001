def dimension(length):
    dimensions = []
    for x in range(length):
        for y in range(length):
            coordinate = [x, y]
            dimensions.append(coordinate)
    return dimensions



def windflow(grid, coordinate, wind):
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





return adjacent_cells


def check_ignition(b_grid, f_grid, h_grid, i_threshold, w_direction, i, j):
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
    ignition_factor = ignition(adj_cells, b_grid, i, j)

    return ignition_factor >= i_threshold



