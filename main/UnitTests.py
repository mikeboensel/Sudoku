'''
Created on Dec 5, 2016

@author: User
'''
import unittest
# from main import Sudoku
from Sudoku import *

puzzleInputDir = "../puzzles/inputs/"
puzzleOutputDir = "../puzzles/outputs(expected)/"


class Test(unittest.TestCase):

    def simpleFrameWork(self, puzzleName):
        readInGame(deSerializeGame(puzzleInputDir + puzzleName))
        solve()
        proposedSolution = board.copy()
        readInGame(deSerializeGame(puzzleOutputDir + puzzleName))
        actualSolution = board
        self.assertEqual(proposedSolution, actualSolution)
        
    def testEasy(self):
        self.simpleFrameWork("Easy_8313081943")

    def testMed(self):
        self.simpleFrameWork("Med_8867043329")

    def testHard(self):
        self.simpleFrameWork("Hard_1956388974")

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testEasy']
    unittest.main()
