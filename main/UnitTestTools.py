'''
Created on Dec 12, 2016

@author: User
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from main import Sudoku


'''Parse the websudoku.com page
'''
def getPuzzle(driver):
    currBase = 0
    base = 0
    increment = 10
    
    id = ''
    
    puzzle = ''
    
    webEle = None
    while base < 100:
        if base <10:
            id = 'f0' + str(base)
        else:
            id = "f" +str(base)
        
        webEle = driver.find_element(by=By.ID, value=id)
         
        att = webEle.get_attribute("value")
        
        if att == None or att == '':
            puzzle+= ' _ '
        else:
            puzzle+= ' {} '.format(att)
        
        base += increment
        
        if base in range(30,39):
            puzzle += ' | '
        if base in range(60,69):
            puzzle += ' | '
            
        if base >= 90:
            puzzle+= '\n'
            if currBase == 2 or currBase == 5:
                puzzle+= '---------------------------------\n'
            if currBase < 8:
                currBase +=1
                base = currBase
            else:
                #read all rows
                break
            
    return puzzle


def getPuzzleName(driver):
    webEle = driver.find_element(by=By.CSS_SELECTOR, value='p font a[title="Copy link for this puzzle"]')
    
    # Expected element text format "{DifficultyLevel} puzzle {puzzleNum}"
    
    name = webEle.text.split(" ") 
    
    return name[0] + "_" + name[2] #name should be "{DifficultyLevel}_{puzzleNum}"

'''
Reaches out to websudoku.com, gets the puzzle, writes that out as an input (puzzle) file. Runs through the solver.
Submits the solution and if accepted writes out the solution file.
'''


def writeToFile(name, puzzle):
    with open("../../puzzles/inputs/" + name, "w") as f:
        f.write(puzzle)
    
#  C:\Users\User\Desktop\Dev\workspaces\LiClipse2\Sudoku\puzzles
#     C:\Users\User\Desktop\Dev\workspaces\LiClipse2\Sudoku\main\UnitTestTools.py
   

def verifyViaWebSudoku(driver):
    pass


def createTestCase():
    driver = webdriver.Firefox(firefox_binary='C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')
   
    driver.get("http://www.websudoku.com/")
    
    driver.switch_to_frame(0)
    
    puzzle = getPuzzle(driver)
    
    name = getPuzzleName(driver)
    
    print(puzzle)
    print(name)
    
    writeToFile(name, puzzle)
    
    Sudoku.readInGame(puzzle)
    
    Sudoku.solve()
    
    print("proposed solution:")
    Sudoku.printBoard()
    
    verifyViaWebSudoku(driver)
    
createTestCase()