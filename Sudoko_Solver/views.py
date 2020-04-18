from django.shortcuts import render
from .algo import algo
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
def sudoku(request):
    res = request.POST

    if res:
        cells = []

        for row_num in range(9):
            cells.append([])

            for column_num in range(9):
                current_location = 'cell-%i-%i' % (row_num + 1, column_num + 1)

                try:
                    current_num = int(res[current_location])
                except ValueError:
                    current_num = 0

                cells[row_num].append(current_num)

        my_algo = algo(cells=cells)

        try:
            my_algo.solve()
            return render(request, 'sudoku/sudoku.html', {'cells': my_puzzle.cells, 'new': False, 'error': False})

        except ValueError:
            return render(request, 'sudoku/sudoku.html', {'cells': [[0 for i in range(9)] for j in range(9)], 'new': True, 'error': True})

    else:
        return render(request, 'sudoku/sudoku.html', {'cells': [[0 for i in range(9)] for j in range(9)], 'new': True, 'error': False})
