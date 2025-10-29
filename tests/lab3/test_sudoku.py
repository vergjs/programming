import unittest
from src.lab3.sudoku import group, get_row, get_col, get_block, find_empty_positions, find_possible_values, solve, check_solution, generate_sudoku

class SudokuTest(unittest.TestCase):



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
            ['1','2','3','4'],
            ['4','5','6','7'],
            ['7','8','9','1'],
            ['2','3','4','5']
        ]
        self.assertEqual(get_block(grid, (0,0)), ['1','2','3','4','5','6','7','8','9'])
        self.assertEqual(get_block(grid, (3,3)), ['9','1','4','5'])

if __name__ == "__main__":
    unittest.main()

