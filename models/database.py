import logging
import traceback

import pymysql
from colorama import Fore, Style


def get_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='3kkxb7jdfh',
                           db='channel_manager',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def bal_increment():
    query = f"update aduser set count = count + 1"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def bot_fetcher(bot_token):
    try:
        con = get_connection()
        cursor = con.cursor()
        query = f"SELECT * FROM req_bots where bot_token = '{bot_token}'"
        print(query)
        cursor.execute(query)
        return cursor.fetchone()

    except Exception as error:
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        logging.error(error)
    finally:
        con.close()

def channel_checker(channel_id):
    query = f"SELECT * FROM cm_channel_data where channel_id ={channel_id}"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        result = p.fetchall()
        if result and result[0]['bot_id'] == 1111:
            return []
        return result
    except Exception as e:
        print(e)
        pass

def channel_data_inserter(bot_id=0, channel_id=0, user_id=0, greet_msg=0, channel_name='', greet_msg_chat=0, btns=''):
    btns = str(btns)
    try:
        connection = get_connection()
        cursor = connection.cursor()
        if_in_channel_guru = f"select * from cm_channel_data where channel_id = {channel_id} and bot_id = 1111"
        print(if_in_channel_guru)
        cursor.execute(if_in_channel_guru)
        existing_data = cursor.fetchone()
        if existing_data:
            old_bot_id, old_channel_id, old_user_id, old_greet_msg, old_channel_name, old_greet_msg_chat, old_btns = existing_data
            insert_into_dump_table = (f"insert into dumped_rows (bot_id, channel_id, user_id, greet_msg, channel_name, greet_msg_chat, btns) values ({old_bot_id}, {old_channel_id}, {old_user_id}, {old_greet_msg}, '{old_channel_name}', {old_greet_msg_chat}, \'{old_btns.replace("'","\'")}\')")

            cursor.execute(insert_into_dump_table)
            dump_query = f"delete from cm_channel_data where channel_id = {channel_id} and bot_id = 1111"
            cursor.execute(dump_query)
        insert_query = (f"insert into cm_channel_data (bot_id, channel_id, user_id, greet_msg, channel_name, greet_msg_chat, btns) values ({bot_id}, {channel_id}, {user_id}, {greet_msg}, '{channel_name}', {greet_msg_chat}, \'{btns.replace("'", "''")}\')")
        cursor.execute(insert_query)
        connection.commit()

    except Exception as e:
        print(f"Here in channel_data_inserter func : {e}")

def get_channels(id=0,name=0):
    if name == 0:
        query = f"SELECT * FROM cm_channel_data WHERE user_id='{id}'"
    else:
        query = f"SELECT * FROM cm_channel_data WHERE user_id='{id}' and channel_id = '{name}'"

    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return p.fetchall()
    except Exception as e:
        print(e)
        pass

def all_clients(owner=0,channel=0,col=0):
    if col==0:
        if channel == 0:
            query = f"select count(*) from cm_data where owner_user_id = {owner}"
        else:
            query = f"select count(*) from cm_data where owner_user_id = {owner} and channel_id = '{channel}'"
    elif col == "*":
        query = f"select * from cm_data where owner_user_id = {owner}"

    else:
        query = f"select {col} from cm_data where owner_user_id = {owner} and channel_id = '{channel}'"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return p.fetchall()
    except Exception as e:
        print(e)
        pass

def channel_remover(user_id,channel_id):
    query = f'delete from cm_channel_data where user_id = {user_id} and channel_id={channel_id}'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def editor(table,col,val,con):
    if val.isnumeric():
        query = f'update {table} set {col} = {int(val)} where channel_id = {con}'
    else:
        query = f'update {table} set {col} = \'{val}\' where channel_id = {con}'
    print(query)
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def udpate_message_state(user_id):
    query = f'update cm_data set message = 0 where user_id = {user_id}'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass