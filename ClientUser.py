import mysql

from User import User


class ClientUser(User):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="banking_app"
    )
    cursor = conn.cursor()

    def showPossibleActions(User):
        print("---------------Client menu----------------")
        print("1. print your accounts")
        print("2. make a money transfer")
        print("3. print last login timestamp")
        print("9. logout ")
    def getUserAccountsDetails(self):
        query = ("SELECT account_table.account_id "
                 "      ,account_table.balance "
                 "      ,account_table.maximal_overdraft "
                 "      ,currency_table.name "
                 "      ,currency_table.convert_rate_to_pln "
                 "FROM account_table "
                 "INNER JOIN currency_table "
                 "on account_table.currency_code = currency_table.currency_code "
                 "WHERE account_table.client_id = %s")
        self.cursor.execute(query, (self.userName,))
        result = self.cursor.fetchone()
        print("-------------------ACCOUNT-LIST-START------------------------")
        self.accountList = []
        while (result):

            self.accountList.append({"Account":result[0], "Balance":result[1], "MaxOverdraft":result[2], "Currency":result[3], "ConverRateToPln":result[4] })
            print("Account id:", result[0]
                 ,"current balance:", result[1]
                 ,"maximal overdraft:", result[2]
                 ,"currency:",result[3]
                 ,"convert rate to PLN:",result[4])
            result = self.cursor.fetchone()
        print("-------------------ACCOUNT-LIST-END--------------------------")
    def getReceiverAccountData(self, receiverAccountId ):
        query = ("SELECT account_table.currency_code, currency_table.convert_rate_to_pln "
                 "from account_table "
                 "inner join currency_table "
                 "on account_table.currency_code = currency_table.currency_code "                 
                 "where account_table.account_id = %s")
        self.cursor.execute(query,(receiverAccountId,))
        return self.cursor.fetchone()
    def checkIfAccountBelongsToTheUser(self, senderAccount):
        for accountDictionary in self.accountList:
            if accountDictionary.get("Account") == senderAccount:
                return  [accountDictionary.get("Account")
                        ,accountDictionary.get("Balance")
                        ,accountDictionary.get("MaxOverdraft")
                        ,accountDictionary.get("Currency")
                        ,accountDictionary.get("ConverRateToPln")]

        return False
    def checkIfSufficientFunds(self, Balance, MaximalOverdraft, transferAmount):
        if (Balance + MaximalOverdraft) >= transferAmount:
            return True
        else:
            return False
    def ConvertTransferAmountToPln(self,transferAmount, convertRateToPln):
        return float(transferAmount * float(convertRateToPln))
    def transferMoney(self,senderAccount, transferAmountInSenderCurrency, transferAmountInPln, receiverAccountid, receiverCurrencyCode, receiverCurrencyRateToPln ):

        try:
            # in case of errors whole transaction will be reverted (rolled back)


            queryForSenderAccount= ("UPDATE account_table "
                                    "set balance = balance - %s "
                                    "WHERE account_id = %s")
            queryForReceiverAccount= ("UPDATE account_table "
                                   "set balance = balance + %s "
                                    "WHERE account_id = %s")

            amountToAddToReceiverAccount = float(transferAmountInPln / float(receiverCurrencyRateToPln))

            self.cursor.execute(queryForSenderAccount,(transferAmountInSenderCurrency, senderAccount,))

            self.cursor.execute(queryForReceiverAccount, (amountToAddToReceiverAccount, receiverAccountid,))

            self.conn.commit()

            print("Transfer completed successfully")

        except:
            self.conn.rollback()
            print("Transfer failed")

    def makeMoneyTransfer(self):
        receiverAccountid = input("Please provide receiver account id: ")

        result = self.getReceiverAccountData(receiverAccountid)
        if not result:
            print('Receiver account does not exist')
            return
        receiverCurrencyCode = result[0]
        receiverCurrencyRateToPln = result[1]

        self.getUserAccountsDetails()
        senderAccount = input("Please provide account id from which you wish to send money from the list above: ")
        senderAccountData = self.checkIfAccountBelongsToTheUser(senderAccount)
        if (senderAccountData):
            print("Correct account has been choosen")
        else:
            print("Chosen account does not belong to you")
            return


        transferAmount = 0
        try:
            transferAmount = float(
                input("How much money you wish to send (use dot as a decimal separator) in your account currency: "))
        except:
            print("Amount is not numeric value !!!")
            return
        if (transferAmount < 0.01):
            print("Amount is to small to transfer!")
            return
        if (transferAmount > 999999999):
            print("Maximal amount that can be transfered is 999999999!")
            return
                                        # account balance       #account maximal overdraft
        if not (self.checkIfSufficientFunds(senderAccountData[1], senderAccountData[1], transferAmount)):
            print("Insufficient funds")
            return
                                                           #convert rate to pln
        transferAmountInPln = self.ConvertTransferAmountToPln(transferAmount, senderAccountData[4])

        self.transferMoney(senderAccount, transferAmount, transferAmountInPln, receiverAccountid, receiverCurrencyCode, receiverCurrencyRateToPln)

    def printLastLoginTimestamp(self):
        query = "SELECT last_login_timestamp from login_table where client_id = %s"
        self.cursor.execute(query, (self.userName, ))
        result = self.cursor.fetchone()
        if result:
            print("Last login timestamp of user", self.userName, "is", result[0])
        else:
            raise Exception("Something went wrong error code #000005")
    def executeDesiredAction(self, choice):
        match choice:
            case '1': # 1. print your accounts
                self.getUserAccountsDetails()
            case '2': # 2. make a money transfer
                self.makeMoneyTransfer()
            case '3': # 3. print last login timestamp
                self.printLastLoginTimestamp()
            case '9':
                pass
            case _:
                print("Invalid option try again")


