import random
import time

class Account:

    def __init__(self, card_num, pin_num, balance=0):
        self.card_num = card_num
        self.pin_num = pin_num
        self.balance = balance


    def get_PIN(self):
        return self.pin_num


    def get_card_num(self):
        return self.card_num


    def get_balance(self):
        return self.balance


    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False


    def deposit(self, amount):
        self.balance += amount
        return self.balance


    def __str__(self):
        return "Your card has been created\n" + \
            "Your card number:\n" + \
            self.get_card_num() + \
            "\nYour card PIN:\n" + \
            self.get_PIN()


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.get_card_num() == other.get_card_num()
        else:
            return False


class NumberGenerator:
    random.seed(time.time())

    def __init__(self):
        pass


    def generate_IIN(self):
        return '400000'


    def generate_customer_acc_number(self):
        number = ""
        for i in range(0, 9):
            number += str(random.randint(0, 9))
        return number


    def generate_PIN(self):
        number = ""
        for i in range(0, 4):
            number += str(random.randint(0, 9))
        return number


    def generate_checksum(self, IIN, acc_num): # Luhn Algorithm
        digits = []
        [digits.append(int(digit)) for digit in IIN + acc_num]
        for idx in range(0, len(digits), 2):
            digits[idx] *= 2
        for idx in range(0, len(digits)):
            if digits[idx] > 9:
                digits[idx] -= 9
        total = sum(digits)
        return (10 - (total % 10)) % 10


    def is_checksum_valid(self, full_acc_number): # Luhn Algorithm
        checksum = int(full_acc_number[-1])
        acc_num = []
        [acc_num.append(int(digit)) for digit in full_acc_number[0:15]]
        for idx in range(0, len(acc_num), 2):
            acc_num[idx] *= 2
        for idx in range(0, len(acc_num)):
            if acc_num[idx] > 9:
                acc_num[idx] -= 9
        total = sum(acc_num)
        return (total + checksum) % 10 == 0