from locale import currency

import mysql

from PasswordHasher import PasswordHasher
from User import User


class BankUser(User):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="banking_app"
    )
    cursor = conn.cursor()

    def showPossibleActions(User):
        print("1. Add new user")
        print("2. Add an account for a user")
        print("3. delete an user")
        print("9. logout")
    def addNewUser(self):
        userName = input("Please provide user name: ")
        userPassword = input("Please provide user password: ")
        userType = input("Please provide user type (1 - bank clerk, 2 - client): ")
        if (len(userName) > 50 or len(userPassword) > 50 or userType not in ('1','2')):
            print("Client data is invalid")
            return
        result = PasswordHasher.hashPassword(userPassword)
        passwordHash = 0
        saltHash = 0
        if result:
            passwordHash = result[0]
            saltHash = result[1]
        else:
            raise Exception("Something went wrong error code #000006")

        try:
            insertQueryClientTable = "INSERT INTO client_table(client_id, user_type) values(%s, %s)"

            self.cursor.execute(insertQueryClientTable, (userName, userType,))
            # Insert to table login_table
            insertQueryLoginTable = "INSERT INTO login_table(client_id, password_hash, password_salt) values(%s,%s,%s)"

            self.cursor.execute(insertQueryLoginTable,(userName,passwordHash,saltHash,))
            self.conn.commit()
            print("User", userName,"added successfully!")
        except:
            self.conn.rollback()
            raise Exception("Something went wrong error code #000006")
    def printCurrencies(self):
        query = ("select currency_code, name, convert_rate_to_pln "
                 "from currency_table")
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        self.currencyList = []
        while(result):
            print("currency code:", result[0], "currency name:", result[1], "convert rate to pln:", result[2])
            self.currencyList.append( result[0]) # currencies will be stored in the list
            result = self.cursor.fetchone()


    def addAccountForUser(self):
        newAccountId = input("New account id: ")
        forClientId = input("provide for which client id account should be added?: ")
        initialBalance = float(input("provide initial balance for account: "))
        maxOverdraft = float(input("please provide maximal overdraft: "))
        if maxOverdraft < 0:
            print("Maximal overdraft cannot be negative")
            return
        self.printCurrencies()
        currency = int(input("pleae provide currency for an account (currency code from above): "))
        if currency not in self.currencyList:
            print("Unknown currency code!")
            return
        query = ("INSERT INTO account_table(account_id, client_id, balance, maximal_overdraft, currency_code) "
                 "values(%s,%s,%s,%s,%s)")
        #try:
        self.cursor.execute(query,(newAccountId,forClientId,initialBalance,maxOverdraft,currency, ))
        self.conn.commit()
        print("Account created successfully")
        # except:
        #     print("Account could not be created")
        #     self.conn.rollback()
        #     return

    def deleteUserData(self):
        userName = input("provide user name that you want to delete: ")
        confirmation = input("to confirm that you want to delete this user, please write theirs name again: ")
        if userName == confirmation:
            # start deletions
            queryToDeleteAccounts = "DELETE FROM account_table where client_id = %s"
            queryToDeleteLoginData = "DELETE FROM login_table where client_id = %s"
            queryToDeleteClientData = "DELETE FROM client_table where client_id = %s"
            try:
                self.cursor.execute(queryToDeleteAccounts, (userName,))
                self.cursor.execute(queryToDeleteLoginData, (userName,))
                self.cursor.execute(queryToDeleteClientData, (userName,))
                self.conn.commit()
                print("User has been deleted")
            except:
                self.conn.rollback()
                print("Impossible to delete this client")
                return

        else:
            print("confirmation failed")
            return

    def executeDesiredAction(self, userChoice):
        print("bank user, user choice, ", userChoice)
        match userChoice:
            case '1':
                self.addNewUser()
            case '2':
                self.addAccountForUser()
            case '3':
                self.deleteUserData()
            case '9':
                pass
            case _:
                print("Invalid option try again")
