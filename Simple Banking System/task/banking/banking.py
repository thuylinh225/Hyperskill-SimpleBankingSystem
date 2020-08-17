import string
import random
import sqlite3

class Card:
    def __init__(self):

        self.conn_str = 'card.s3db'
        conn = sqlite3.connect(self.conn_str)
        cur = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS card (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)'
        cur.execute(sql)
        conn.commit()
        conn.close()

    def create_account(self):
        random.seed()
        chars = string.digits
        pin = str(''.join(random.choice(chars) for _ in range(4)))
        number = str(random.randint(4000000000000000,4000009999999999))
        other_sum = 0
        odd_sum = 0
        even_sum = 0
        for i in range(0, len(number) - 1, 2):
            i = int(i)
            x = int(number[i]) * 2
            if x > 9:
                y = x - 9
                even_sum += y
            else:
                other_sum += x
        for j in range(1, len(number) - 1, 2):
            w = int(number[j])
            odd_sum += w
        total= odd_sum + even_sum + other_sum
        if total % 10 > 0:
            number = number[:15] + str(10 - (total % 10))
        else:
            number = number[:15] + "0"
        if not self.checkNumberExist(number):
            self.insertCard(number, pin)
            self.print(number, pin)

    def checkNumberExist(self, number):
        sql = "select count() from card where number =" + number
        conn = sqlite3.connect(self.conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        record = cur.fetchone()
        cur.close()
        conn.close()
        if record[0] > 0:
            return True
        return False

    def insertCard(self, number, pin):
        sql = 'INSERT INTO card (number, pin, balance) VALUES ({0}, {1}, 0)'.format(number, pin)
        # sql = 'INSERT INTO card (number, pin, balance) VALUES (' + number + ' , ' + pin + ', 0)'
        conn = sqlite3.connect(self.conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()

    def print(self, number, pin):
        print()
        print("Your card has been created")
        print("Your card number:")
        print(f"{number}")
        print("Your card PIN:")
        print(f"{pin}")

    def log_in(self):
        print()
        login_number = str(input("Enter your card number:\n"))
        login_pin = str(input("Enter your PIN:"))
        print()
        sql = "select balance from card where number = {0} AND pin = {1}".format(login_number, login_pin)
        conn = sqlite3.connect(self.conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        record = cur.fetchone()
        cur.close()
        conn.close()
        if record is not None:
            print("You have successfully logged in!")
            self.act_acc(record[0], login_number)
            self.close(login_number)
        else:
            print("Wrong card number or PIN!")
            self.action()

    def act_acc(self, balance, login_number):
        while True:
            print()
            act = int(input("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit\n"""))
            print()
            if act == 1:
                print("Balance: {}".format(balance))
                continue
            if act == 2:
                income = int(input("Enter income:\n"))
                balance += income
                sql = "update card set balance = {} where number = {}".format(balance, login_number)
                conn = sqlite3.connect(self.conn_str)
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
                print("Income was added!")
                continue
            if act == 3:
                self.transfer(balance, login_number)
                continue
            if act == 4:
                self.close(login_number)
            if act == 5:
                print("You have successfully logged out!")
                break
            else:
                print("Bye!")
                exit()

    def Luhn_check(self, receiver_number):
        other_sum = 0
        odd_sum = 0
        even_sum = 0
        for i in range(0, len(receiver_number) - 1, 2):
            i = int(i)
            x = int(receiver_number[i]) * 2
            if x > 9:
                y = x - 9
                even_sum += y
            else:
                other_sum += x
        for j in range(1, len(receiver_number), 2):
            w = int(receiver_number[j])
            odd_sum += w
        total= odd_sum + even_sum + other_sum
        if total % 10 == 0:
            return True
        return False

    def transfer(self, balance, login_number):
        print("Transfer")
        receiver_number = str(input("Enter card number:\n"))
        if receiver_number == login_number:
            print("You can't transfer money to the same account!")
            self.act_acc(balance, login_number)
        if not self.Luhn_check(receiver_number):
            print("Probably you made mistake in the card number. Please try again!")
            self.act_acc(balance, login_number)
        if not self.checkNumberExist(receiver_number):
            print("Such a card does not exist.")
            self.act_acc(balance, login_number)
        else:
            amount = int(input("Enter how much money you want to transfer:\n"))
            if amount > balance:
                print("Not enough money!")
            else:
                print("Success!")
                balance -= amount
                sql = "update card set balance = {} where number = {}".format(balance, login_number)
                conn = sqlite3.connect(self.conn_str)
                cur = conn.cursor()
                cur.execute(sql)
                sql1 = "update card set balance = balance + {} where number = {}".format(amount, receiver_number)
                cur.execute(sql1)
                conn.commit()
                cur.close()
                self.act_acc(balance, login_number)

    def close(self, login_number):
        sql = "delete from card where number = {}".format(login_number)
        conn = sqlite3.connect(self.conn_str)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("The account has been closed!")
        self.action()

    def action(self):
        print()
        action_input = input("""1. Create an account
2. Log into account
0. Exit:\n""")
        if action_input == "1":
            self.create_account()
        elif action_input == "2":
            self.log_in()
        else:
            print()
            print("Bye!")
            exit()

if __name__ == "__main__":
    anatomy = Card()
    while True:
        anatomy.action()
