import hmac
from abc import abstractmethod
from logging import raiseExceptions

import mysql.connector
import  mysql.connector.cursor

from PasswordHasher import PasswordHasher


class User():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="banking_app"
    )
    cursor = conn.cursor()

    @abstractmethod
    def showPossibleActions(self):
        pass
    def checkIfusertypesOk(self, userTypeFromDb, UserType):
        if userTypeFromDb != UserType:
            print("User priviliges are invalid for specified login option")
            raise Exception("Something went wrong error code #000004")
    def getUserCredentials(self, userType):
        self.userName  = input("provide user name: ")
        self.userPassword = input("provide your password: ")
        return [self.userName, self.userPassword, userType]
    def checkIfUserValidInDataBase(self, credentials):
        #print("in check if user valid in databse; ")
        #print("username: ", credentials[0])
        userName = credentials[0]
        #print("password: ", credentials[1])
        userPassword = credentials[1]
        userType = credentials[2]
        #get salt from the database
        query = ("SELECT login_table.password_salt"
                 "      ,login_table.password_hash"
                 "      ,client_table.user_type "
                 "       FROM "
                 "       login_table"
                 "       inner join client_table "
                 "       on login_table.client_id = client_table.client_id  "
                 "       where login_table.client_id = %s")

        self.cursor.execute(query, (userName,))
        result = self.cursor.fetchone()
        saltFromDb = 0
        passwordHashFromDb = 0
        userTypeFromDb = 0
        if result:
            saltFromDb = result[0]
            passwordHashFromDb = result[1]
            userTypeFromDb = result[2]
          #  print("user type from db: " , userTypeFromDb)
            self.checkIfusertypesOk( userTypeFromDb, userType)
          #  print(type(saltFromDb))
          #  print("pobrana wartosc salt ", saltFromDb)
          #  print(type(passwordHashFromDb))
          #  print("pobrana wartosc password hash ", passwordHashFromDb)
        else:
            print("Login data is incorrect !!!")
            return False

        hashedUserPassword = PasswordHasher.compute_hash(userPassword, saltFromDb)
        #print("compare of passwords")
        #print("form db: ", passwordHashFromDb)
        #print("form us: ", hashedUserPassword)
        if hmac.compare_digest(hashedUserPassword, passwordHashFromDb):
            #print("Login operation correct!!!")
            return True
        else:
            #print("Login data is incorrect !!!")
            return False

    def checkIfUserWantsToLogIn(self):
        userWishToContinue = True
        choice = input("if you wish to log in the system please write 'Y': ")
        if (choice.upper() != 'Y'):
            userWishToContinue = False
        return userWishToContinue

    def updateLastLoginTimestamp(self, userName):
        updateQuery = "UPDATE login_table set last_login_timestamp = current_timestamp where client_id = %s"

        self.cursor.execute(updateQuery, (userName,))
    def logIn(self, userType):

        while(True):
            userWishToContinue = self.checkIfUserWantsToLogIn()
            if (userWishToContinue):
                if self.checkIfUserValidInDataBase(self.getUserCredentials( userType)):
                    self.updateLastLoginTimestamp(self.userName)
                    return True
            else:
                return -1
            print("try again")

