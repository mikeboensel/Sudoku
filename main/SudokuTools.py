'''
Created on Dec 5, 2016

@author: User
'''

def hasDupe(myList):
    s = set()
    for listItem in myList:
        if listItem in s and listItem != '_':
            return True
        s.add(listItem)
    return False
    
def checkPositionRange(pos, msg):
    if pos > 8 or pos < 0:
        print("Bad input " + pos + " " + msg)
        exit
        
def findNeighborsRanges (a):
    if a <= 2:
        return [0, 1, 2]
    elif a <= 5:
        return [3, 4, 5]
    elif a <= 8:
        return [6, 7, 8]
    return None
    
def getBoxNeighborCoordList(x, y):
    checkPositionRange(x, "GetBox x")
    checkPositionRange(y, "GetBox y")
    
    xRange = findNeighborsRanges(x)    
    yRange = findNeighborsRanges(y)

    return [(x, y) for x in xRange for y in yRange]
