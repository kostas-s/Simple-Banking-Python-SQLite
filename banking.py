import sys
import sqlite3
from account import Account, NumberGenerator
from database import DatabaseController


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
saved_accounts = dict()     #dictionary holding key:card num -> val:account object
curr_account = None         #currently logged in account
dbc = DatabaseController(cur_passed=cur, conn_passed=conn)


def load_accs_from_table():
    acc_list_db = dbc.get_accs()
    for acc in acc_list_db:
        #print(acc)
        curr_acc = Account(card_num=acc[1], pin_num=acc[2], balance=acc[3])
        saved_accounts[acc[1]] = curr_acc


def check_if_table_exists():
    if dbc.does_table_exist():
        print("SQL: Connected to database successfully!")
        load_accs_from_table()


def print_menu():
    print()
    if curr_account == None:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
    else:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")


def add_income():
    print()
    print("Enter income:")
    try:
        income = int(input())
        curr_account.deposit(income)
        dbc.update_balance(curr_account, curr_account.get_balance())
        print("Income was added!")
    except ValueError:
        print("Invalid input", file=sys.stderr)
        return


def create_account():   #Generate new card number that satisfies conditions, Generate PIN from 0000 to 9999
    ng = NumberGenerator()
    while True:         #Ensure no identical account numbers can exist
        IIN = ng.generate_IIN()
        customer_acc_number = ng.generate_customer_acc_number()
        checksum = str(ng.generate_checksum(IIN, customer_acc_number))
        PIN = ng.generate_PIN()
        acc_id = IIN + customer_acc_number + checksum
        if acc_id not in saved_accounts:
            break
    acc = Account(IIN + customer_acc_number + checksum, PIN)
    dbc.write_new_acc_to_table(acc)
    saved_accounts[acc_id] = acc
    print(acc)


def check_balance():
    if curr_account == None:
        print("Unexpected Error", file=sys.stderr)
        return
    balance = dbc.check_balance(curr_account)
    print("Balance: ", str(balance))


def log_in_account():
    global curr_account
    print("Enter your card number:")
    card_entered = input()
    print("Enter your PIN:")
    PIN_entered = input()
    if card_entered in saved_accounts and PIN_entered == saved_accounts.get(card_entered).get_PIN():
        print("\nYou have successfully logged in!")
        curr_account = saved_accounts.get(card_entered)
    else:
        print("\nWrong card number or PIN!")


def do_transfer():
    ng = NumberGenerator()
    print("Enter your card number:")
    other_acc_num = input()
    if not ng.is_checksum_valid(full_acc_number=other_acc_num):
        print("\nProbably you made a mistake in the card number.\nPlease try again!")
        return
    if other_acc_num not in saved_accounts: #here you have to check checksum too and display different error if mistake in card no
        print("\nSuch a card does not exist.")
        return
    other_account = saved_accounts[other_acc_num]
    print("Enter how much money you want to transfer:")
    amount = int(input())
    if curr_account.withdraw(amount):
        other_account.deposit(amount)
        dbc.update_balance(curr_account, curr_account.get_balance())
        dbc.update_balance(other_account, other_account.get_balance())
        print("Success!")
    else:
        print("Not enough money!")
        return


def close_account():
    global curr_account
    dbc.delete_account(curr_account)
    del saved_accounts[curr_account.get_card_num()]
    curr_account = None
    print("\nThe account has been closed!")


def log_out_account():
    global curr_account
    curr_account = None
    print("\nYou have successfully logged out!")


def handle_input():
    try:
        option = int(input())
        print()
        if curr_account == None:
            if option == 1:
                create_account()
            elif option == 2:
                log_in_account()
            elif option == 0:
                print("Bye!")
                sys.exit()
            else:
                raise ValueError
        else:
            if option == 1:
                check_balance()
            elif option == 2:
                add_income()
            elif option == 3:
                do_transfer()
            elif option == 4:
                close_account()
            elif option == 5:
                log_out_account()
            elif option == 0:
                print("Bye!")
                conn.close()
                sys.exit()
            else:
                raise ValueError
    except ValueError:
        print("Invalid Input", file=sys.stderr)


check_if_table_exists()
while True:
    print_menu()
    handle_input()