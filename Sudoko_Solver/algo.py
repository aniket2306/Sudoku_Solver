from copy import deepcopy

def get_presence(cells):
    present_in_row = [{i: False for i in range(1, 10)} for j in range(9)]
    present_in_column = [{i: False for i in range(1, 10)} for j in range(9)]
    present_in_grid = [{i: False for i in range(1, 10)} for j in range(9)]

    for row_num in range(9):
        for column_num in range(9):
            num = cells[row_num][column_num]

            if num:
                present_in_row[row_num][num] = True
                present_in_column[column_num][num] = True
                present_in_grid[row_num // 3 * 3 + column_num // 3][num] = True

    return present_in_row, present_in_column, present_in_grid

def get_possible_values(cells):
    present_in_row, present_in_column, present_in_grid = get_presence(cells)
    possible_values = {}

    for row_num in range(9):
        for column_num in range(9):
            if cells[row_num][column_num] == 0:
                possible_values[(row_num, column_num)] = [
                    num for num in range(1, 10) if
                    (not present_in_row[row_num][num]) and
                    (not present_in_column[column_num][num]) and
                    (not present_in_grid[row_num // 3 * 3 + column_num // 3][num])
                ]

    return possible_values

def update(cells):
    update_again = False

    possible_values = get_possible_values(cells)
    for location in possible_values:
        if len(possible_values[location]) == 1:
            update_again = True
            cells[location[0]][location[1]] = possible_values[location][0]
            break

    if update_again:
        cells = update(cells)

    return cells

def trial_plug_in(cells, location, value):
    copied_cells = deepcopy(cells)
    copied_cells[location[0]][location[1]] = value
    copied_cells = non_class_solve(copied_cells)

    return copied_cells

def non_class_solve(cells):
    cells = update(cells)
    possible_values = get_possible_values(cells)

    if not len(possible_values):
        return cells

    min_value_num = 10
    for location in possible_values:
        value_num = len(possible_values[location])

        if not value_num:
            return False

        if value_num < min_value_num:
            min_value_num = value_num
            min_location = location

    for value in possible_values[min_location]:
        tried_cells = trial_plug_in(cells, min_location, value)
        if tried_cells:
            return tried_cells

    return False

class Puzzle:
    def __init__(self, cells=None):
        if cells:
            self.cells = cells
        else:
            self.cells = [[0 for i in range(9)] for j in range(9)]

    def validate(self):
        row_count = [{num: 0 for num in range(1, 10)} for i in range(9)]
        column_count = [{num: 0 for num in range(1, 10)} for i in range(9)]
        grid_count = [{num: 0 for num in range(1, 10)} for i in range(9)]

        for row_num in range(9):
            for column_num in range(9):
                num = self.cells[row_num][column_num]

                if num:
                    row_count[row_num][num] += 1
                    column_count[column_num][num] += 1
                    grid_count[row_num // 3 * 3 + column_num // 3][num] += 1

                    if row_count[row_num][num] > 1 or column_count[column_num][num] > 1 or grid_count[row_num // 3 * 3 + column_num // 3][num] > 1:
                        return False

        return True

    def __str__(self):
        result = ''
        for row_num in range(9):
            for column_num in range(9):
                result += str(self.cells[row_num][column_num]) + ' '

            result += '\n'

        return result

    def solve(self):
        if not self.validate():
            raise ValueError('Input invalid.')

        result_cells = non_class_solve(self.cells)

        if not result_cells:
            raise ValueError('Input invalid.')
        else:
            self.cells = result_cells
