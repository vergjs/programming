import unittest
from src.lab3.sudoku import group, get_row, get_col, get_block, find_empty_positions, find_possible_values, solve, check_solution, generate_sudoku

class SudokuTest(unittest.TestCase):

    def setUp(self):

        self.small_grid = [
            ['1','2','.'],
            ['4','.','6'],
            ['.','8','9']
        ]

        self.full_grid = [
            ['5','3','4','6','7','8','9','1','2'],
            ['6','7','2','1','9','5','3','4','8'],
            ['1','9','8','3','4','2','5','6','7'],
            ['8','5','9','7','6','1','4','2','3'],
            ['4','2','6','8','5','3','7','9','1'],
            ['7','1','3','9','2','4','8','5','6'],
            ['9','6','1','5','3','7','2','8','4'],
            ['2','8','7','4','1','9','6','3','5'],
            ['3','4','5','2','8','6','1','7','9']
        ]

    def test_group_basic(self):
        self.assertEqual(group([1,2,3,4], 2), [[1,2],[3,4]])
        self.assertEqual(group([1,2,3,4,5,6,7,8,9], 3), [[1,2,3],[4,5,6],[7,8,9]])

    def test_get_row(self):
        self.assertEqual(get_row(self.small_grid, (0,0)), ['1','2','.'])
        self.assertEqual(get_row(self.small_grid, (1,0)), ['4','.','6'])

    def test_get_col(self):
        self.assertEqual(get_col(self.small_grid, (0,0)), ['1','4','.'])
        self.assertEqual(get_col(self.small_grid, (0,1)), ['2','.','8'])

    def test_get_block(self):
        grid = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
            ['4', '5', '6', '7', '8', '9', '1', '2', '3'],
            ['7', '8', '9', '1', '2', '3', '4', '5', '6'],
            ['2', '3', '4', '5', '6', '7', '8', '9', '1'],
            ['5', '6', '7', '8', '9', '1', '2', '3', '4'],
            ['8', '9', '1', '2', '3', '4', '5', '6', '7'],
            ['3', '4', '5', '6', '7', '8', '9', '1', '2'],
            ['6', '7', '8', '9', '1', '2', '3', '4', '5'],
            ['9', '1', '2', '3', '4', '5', '6', '7', '8'],
        ]
        self.assertEqual(set(get_block(grid, (0, 0))), set(['1', '2', '3', '4', '5', '6', '7', '8', '9']))
        self.assertEqual(set(get_block(grid, (4, 4))), set(['1', '2', '3', '4', '5', '6', '7', '8', '9']))

    def test_find_empty_positions(self):
        self.assertEqual(find_empty_positions(self.small_grid), (0,2))
        full = [['1','2','3'],['4','5','6'],['7','8','9']]
        self.assertIsNone(find_empty_positions(full))

    def test_find_possible_values(self):
        grid = [
            ['1','2','.'],
            ['4','.','6'],
            ['.','8','9']
        ]
        pos = (0,2)
        values = find_possible_values(grid, pos)
        self.assertTrue(values.issubset(set("123456789")))
        self.assertNotIn('1', values)
        self.assertNotIn('2', values)
        self.assertIn('3', values)

    def test_solve_and_check(self):
        puzzle = [
            ['5','3','.','.','7','.','.','.','.'],
            ['6','.','.','1','9','5','.','.','.'],
            ['.','9','8','.','.','.','.','6','.'],
            ['8','.','.','.','6','.','.','.','3'],
            ['4','.','.','8','.','3','.','.','1'],
            ['7','.','.','.','2','.','.','.','6'],
            ['.','6','.','.','.','.','2','8','.'],
            ['.','.','.','4','1','9','.','.','5'],
            ['.','.','.','.','8','.','.','7','9']
        ]
        solution = solve(puzzle)
        self.assertTrue(solution is not None)
        self.assertTrue(check_solution(solution))

    def test_check_solution(self):
        self.assertTrue(check_solution(self.full_grid))
        broken = [row[:] for row in self.full_grid]
        broken[0][0] = '9'
        self.assertFalse(check_solution(broken))

    def test_generate_sudoku_counts(self):
        grid = generate_sudoku(30)
        empty_cells = sum(row.count('.') for row in grid)
        self.assertEqual(empty_cells, 30)

if __name__ == "__main__":
    unittest.main()

