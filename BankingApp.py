from random import choice
from typing import final

from Login import logUser, getUserForChoice


def printEndMessage():
    print("Thank you for using our system, wish you great day!")
def getUserChoice():
    return str(input("please proivde your choice: "))
def loopUserActions(u1):
    userChoice = '0'
    while(userChoice != '9'):
        u1.showPossibleActions()
        userChoice = getUserChoice()
        u1.executeDesiredAction(userChoice)




def run():
    u1 = logUser()
    if (u1):
        loopUserActions(u1)
    printEndMessage()