import sqlite3
from account import Account

class DatabaseController:
    cur = None
    conn = None

    def __init__(self, cur_passed, conn_passed):
        global cur
        global conn
        cur = cur_passed
        conn = conn_passed


    def delete_account(self, acc):
        cur.execute(f"DELETE FROM card where number = {acc.get_card_num()}")
        conn.commit()

    def check_balance(self, acc):
        cur.execute(f"SELECT balance FROM card WHERE number = {acc.get_card_num()}")
        return cur.fetchone()[0]


    def update_balance(self, acc, newbalance):
        cur.execute(f"UPDATE card SET balance = {newbalance} WHERE number = {acc.get_card_num()}")
        conn.commit()


    def write_new_acc_to_table(self, acc):
        card_num = acc.get_card_num()
        PIN_num = acc.get_PIN()
        balance = acc.get_balance()
        cur.execute("SELECT COUNT(number) from card;")
        cards_inserted = int(cur.fetchone()[0])
        cur.execute(
            f"INSERT INTO card (id, number, pin, balance) VALUES({cards_inserted + 1}, {card_num}, {PIN_num}, {balance})")
        conn.commit()


    def get_accs(self):
        cur.execute("SELECT * FROM card")
        return cur.fetchall()


    def does_table_exist(self):
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='card';")
        if cur.fetchone()[0] == 0:
            print("SQL: Account table doesn't exist, initializing...")
            cur.execute("CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
            conn.commit()
            return False
        else:
            return True