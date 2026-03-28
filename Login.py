from BankUser import BankUser
from ClientUser import ClientUser
from User import User


def displayPrimaryMenu():
    print('Welcome in our banking system choose user option: ')
    print(' 1. bank user')
    print(' 2. client (normal user)')
def getUserForChoice():

    choice = 0
    isInputOk = False
    while not isInputOk:
        try:
            choice = int(input("Your choice: "))
            if (choice in (1,2)):
                isInputOk = True
            else:
                print("you have to provide 1 or 2!!!")
        except:
            print("you have to provide 1 or 2!!!")
    return choice



def logUser():
    displayPrimaryMenu()
    choice = getUserForChoice()
    u1 = User()
    match choice:
        case 1:
            u1 = BankUser()
        case 2:
            u1 = ClientUser()
        case _:
            raise Exception("Something went wrong error code #000001")

    output = u1.logIn(choice)
    if output == True:
        return u1
    elif output == -1:
        return False
    else:
        return False


