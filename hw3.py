''' Programming assignment ( Q-Learning ) 
    Author: John Maloy '''
from __future__ import print_function
import sys
import os
import random

# Global Variables
REWARD = -.1
DISCOUNT_RATE = .5
LEARNING_RATE = .1
PROBABILITY = .1
FORBIDDEN_STATE_REWARD = -100
GOAL_STATE_REWARD = 100

# Class for node class for individual space
class node:
    def __init__(self, label, north, east, south, west, qN, qE, qS, qW):
        self.label = label
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.qN = qN
        self.qE = qE
        self.qS = qS
        self.qW = qW

# Creating the basic environment 
def createEnvironment(goal, forbidden, wall):

    # This is extremely ugly but all it is doing is creating individual nodes
    # Looking at one another as north, south, east or west
    # Python is weird with having nodes point to one another or point to a null object so 
    # I set everything to zero and will work on re evalutaing it later
    nS = node('S', 0, 0, 0, 0, 0, 0, 0, 0)
    n2 = node('2', 0, 0, 0, 0, 0, 0, 0, 0)
    n3 = node('3', 0, 0, 0, 0, 0, 0, 0, 0)
    n4 = node('4', 0, 0, 0, 0, 0, 0, 0, 0)
    n5 = node('5', 0, 0, 0, 0, 0, 0, 0, 0)
    n6 = node('6', 0, 0, 0, 0, 0, 0, 0, 0)
    n7 = node('7', 0, 0, 0, 0, 0, 0, 0, 0)
    n8 = node('8', 0, 0, 0, 0, 0, 0, 0, 0)
    n9 = node('9', 0, 0, 0, 0, 0, 0, 0, 0)
    n10 = node('10', 0, 0, 0, 0, 0, 0, 0, 0)
    n11 = node('11', 0, 0, 0, 0, 0, 0, 0, 0)
    n12 = node('12', 0, 0, 0, 0, 0, 0, 0, 0)

    nS.north = n5
    nS.east = n2
    n2.north = n6
    n2.east = n3
    n2.west = nS
    n3.north = n7
    n3.east = n4
    n3.west = n2
    n4.north = n8
    n4.west = n3
    n5.north = n9
    n5.east = n6
    n5.south = nS
    n6.north = n10
    n6.east = n7
    n6.south = n2
    n6.west = n5
    n7.north = n11
    n7.east = n8
    n7.south = n3
    n7.west = n6
    n8.north = n12
    n8.south = n4
    n8.west = n7
    n9.east = n10
    n9.south = n5
    n10.east = n11
    n10.south = n6
    n10.west = n9
    n11.east = n12
    n11.south = n7
    n11.west = n10
    n12.south = n8
    n12.west = n11

    env = [[n9, n10, n11, n12], [n5, n6, n7, n8], [nS, n2, n3, n4]]

    for x in range(3):
        for y in range(4):
            if(goal == env[x][y].label):
                env[x][y].label = "G"
            
            if(forbidden == env[x][y].label):
                env[x][y].label = "F"
            
            if(wall == env[x][y].label):
                env[x][y].label = "W"
    
    print("\n")
    print("#################### Starting Environment #######################")
    for x in range(3):
        for y in range(4):
            if(env[x][y].label != "G" and env[x][y].label != "F" and env[x][y].label != "W" and env[x][y].label != "S"):
                print("[ ]", end="")
            elif(env[x][y].label == "G"):
                print("[G]", end="")
            elif(env[x][y].label == "F"):
                print("[F]", end="")
            elif(env[x][y].label == "W"):
                print("[W]", end="")
            else:
                print("[S]", end="")
        
        print("\n")
        
    print("##################################################################\n")
    return env

def checkGoalNode(aNode):
    if(aNode.label == "G"):
        return True
    else:
        return False

def checkWallNode(aNode):
    if(aNode.label == "W"):
        return True
    else:
        return False

def checkForbiddenNode(aNode):
    if(aNode.label == "F"):
        return True
    else:
        return False

# Used for checking if a movement is eligable pertaining to the gridworld layout
def checkCanMove(aNode, action):
    if(action == "N" and aNode.north != 0):
        return True
    elif(action == "E" and aNode.east != 0):
        return True
    elif(action == "S" and aNode.south != 0):
        return True
    elif(action == "W" and aNode.west != 0):
        return True
    else:
        return False

def findBestAction(aNode):

    # Looks at the best action possible in the current node and returns which node should be next based of all qvalues
    # At the beginning since all Q Values are 0 north will be chosen as a tie breaker
    actionN = aNode.qN
    actionE = aNode.qE
    actionS = aNode.qS
    actionW = aNode.qW

    if(actionN >= actionE and actionN >= actionS and actionN >= actionW):
        return "N"
    elif(actionE >= actionN and actionE >= actionS and actionE >= actionW):
        return "E"
    elif(actionS >= actionN and actionS >= actionE and actionS >= actionW):
        return "S"
    else:
        return "W"
    
# Implements randomness into the movement process and decides where to go next
def move(aNode):
    rValue = random.randint(1, 10)
    action = findBestAction(aNode)

    if(rValue <= 9):
        return action
    else:
        rValue = random.randint(1,4)
        if(rValue == 1):
            return "N"
        elif(rValue == 2):
            return "E"
        elif(rValue == 3):
            return "S"
        else:
            return "W"

def calculateQValues(previous, current, action):
    
    #qVal = (1 - PROBABILITY)(current)
    print('Hi')

# Function used to learn q values during 10000 iterations
def learn(env):

    #Each time it will start at the starting node
    currentNode = env[2][0]
    
    #Run until you get to the goal node
    while(checkGoalNode(currentNode) == False):

        # Find next action
        action = move(currentNode)
        
        # Check constaints and assign nextNode
        if(action == "N" and checkCanMove(currentNode, action) == True):
            nextNode = currentNode.north
        elif(action == "E" and checkCanMove(currentNode, action) == True):
            nextNode = currentNode.east
        elif(action == "S" and checkCanMove(currentNode, action) == True):
            nextNode = currentNode.south
        elif(action == "W" and checkCanMove(currentNode, action) == True):
            nextNode = currentNode.west
        else:
            nextNode = currentNode
        
        #Check if nextNode is wall, if so stay put ai
        if(checkWallNode(nextNode) == True):
            nextNode = currentNode
        
        # Calculate Q Value for previous node based of action
        calculateQValues(currentNode, nextNode, action)

        # Reset current node and go again until goal is reached
        currentNode = nextNode
        print(currentNode.label)
        
    return env    
        
        

def main():
    userInput = raw_input("Input a environment in the form # # # <q or p> #\nWhere the first # is the goal state, the second \n# is the forbidden state and the third #\nIs the wall. p or q will determine \nwhich output you would like to recieve. \nIf you choose q the additonal number will show\nthe Q Values for that given place.\n")
    goalState, forbiddenState, wallState, outputFormat = userInput.split()

    userInput = list(userInput)
    if(len(userInput) == 5):
        qValueDisplay = userinput[4]

    env = createEnvironment(goalState, forbiddenState, wallState)

    for i in range(4):
        env = learn(env)


if __name__ == "__main__":
    main()