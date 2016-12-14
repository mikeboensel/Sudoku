'''
Created on Dec 12, 2016

@author: User
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from main import Sudoku
from time import sleep
import time

def generateWebSudokuBoxNumbers():
    boxIndex = 0
    ids = []
    while boxIndex <= 88:
        if boxIndex < 10: #Should always be a 3 character ID
            ids.append('f0' + str(boxIndex))
        else:
            ids.append("f" + str(boxIndex))

        if boxIndex % 10 == 8:#Only have 9 squares (0->8 inclusive)
            boxIndex += 2
        else:
            boxIndex += 1
    return ids
    
'''
Return (x,y) tuple that indicates box coordinate
'''
def getWebSodukuBoxCoords(id):
    return (int(id[1]), int(id[2]))
    
'''Parse the websudoku.com page
websudoku rows are labeled:
f00, f10, f20, | ... 
f01, f11, f21, | ...
kind of a pain (and confusing) because I want to read by rows, so we increment by 10s until its time to 
'''
def getPuzzle(driver):
    
    Sudoku.createEmptyGame()

    for id in generateWebSudokuBoxNumbers():
        webEle = driver.find_element(by=By.ID, value=id)
        att = webEle.get_attribute("value")
    
        if att != None and att != '':
            Sudoku.updateUnknownCell(int(id[1]), int(id[2]), att)

def getPuzzleName(driver):
    webEle = driver.find_element(by=By.CSS_SELECTOR, value='p font a[title="Copy link for this puzzle"]')
    
    # Expected element text format "{DifficultyLevel} puzzle {puzzleNum}"
    name = webEle.text.split(" ") 

    #returned name should be "{DifficultyLevel}_{puzzleNum}"
    return name[0] + "_" + name[2] 
'''
Reaches out to websudoku.com, gets the puzzle, writes that out as an input (puzzle) file. Runs through the solver.
Submits the solution and if accepted writes out the solution file.
'''

def writeToFile(name, puzzle, isSolution):
    if isSolution:
        name = "../puzzles/outputs(expected)/" + name
    else:
        name = "../puzzles/inputs/" + name
        
    with open(name, "w") as f:
        f.write(puzzle)



def getButton(driver):
    try:
        return driver.find_element(by=By.CSS_SELECTOR, value = 'p input[value=" How am I doing? "]')
    except: #Want to swallow the element not found exception.
        return None  

def verifyViaWebSudoku(driver):
    
    for id in generateWebSudokuBoxNumbers():
        webEle = driver.find_element(by=By.ID, value=id)
        att = webEle.get_attribute("value")

        if att == '' or att == " " or att == None: #if websudoku has no value in that cell, and we do, write it out
            xy = getWebSodukuBoxCoords(id)
            solvedVal = Sudoku.getPosition(xy[0], xy[1])
            if solvedVal != '_':
                webEle.send_keys(solvedVal)
    
    webEle = getButton(driver)
    webEle.click()
    
    #Need to allow for loading time. Upon full load the button will be gone. So loop until it is
    while getButton(driver) != None: 
        time.sleep(5)
    
    webEle = driver.find_element(by=By.CSS_SELECTOR, value = '#message')
    print(webEle.text)
        
    if "Congratulations" in webEle.text:
        return True
    else:
        return False


def createTestCase():
    driver = webdriver.Firefox(firefox_binary='C:\Program Files (x86)\Mozilla Firefox\Firefox.exe')

    driver.get("http://www.websudoku.com/")
    
    driver.switch_to_frame(0)

    getPuzzle(driver)
    
    name = getPuzzleName(driver)
    
    Sudoku.printBoard()
    print(name)
    
    writeToFile(name, Sudoku.boardToString(), False)
    
    Sudoku.solve()
    
    print("proposed solution:")
    Sudoku.printBoard()
    
    if Sudoku.weHaveSolution:
        if verifyViaWebSudoku(driver):
            writeToFile(name, Sudoku.boardToString(), True)
    else:
        print("Couldn't solve. Good test of any added functionality")
    
createTestCase()
