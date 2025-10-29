import unittest
from src.lab3.sudoku import group, get_row, get_col, get_block, find_empty_positions, find_possible_values, solve, check_solution, generate_sudoku

class SudokuTest(unittest.TestCase):



    def test_group_basic(self):
        self.assertEqual(group([1,2,3,4], 2), [[1,2],[3,4]])
        self.assertEqual(group([1,2,3,4,5,6,7,8,9], 3), [[1,2,3],[4,5,6],[7,8,9]])


if __name__ == "__main__":
    unittest.main()

