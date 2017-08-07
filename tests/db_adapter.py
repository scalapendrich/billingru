import os
import sqlite3

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

db_path = '../web/clients.db'

try:
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()
except:
    logger.error('Failed to connect to database located at "{}". Check if database exist'.format(db_path))
    raise


def get_clients_with_balance_positive():
    params = (0,)
    cursor.execute('Select clients_client_id from balances where balance > ?', params)
    return cursor.fetchall()


def create_new_client_with_balance(client_name, balance_value):
    params = (client_name, )
    cursor.execute('insert into clients (client_name) values(?)', params)
    client_id = cursor.lastrowid
    params = (client_id, balance_value)
    cursor.execute('insert into balances (clients_client_id, balance) values(?, ?)', params)
    db_connection.commit()
    return client_id


def get_balance(client_id):
    params = (client_id,)
    cursor.execute('select balance from balances where clients_client_id =?', params)
    res = cursor.fetchall()
    return float(res[0][0])


def update_balance(user_id, new_balance):
    params = (new_balance, user_id,)
    cursor.execute('update balances set balance = ? where clients_client_id =?', params)
    db_connection.commit()


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    user_id = get_clients_with_balance_positive()[0][0]
    balance = get_balance(user_id)
    update_balance(user_id, balance + float(10.6))
    pass