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
        query = f"SELECT * FROM req_bots where bot_token='{bot_token}'"
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as error:
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        logging.error(error)
    finally:
        con.close()

def check_premium(user_id):
    try:
        con = get_connection()
        cursor = con.cursor()
        query = f"SELECT is_premium FROM cm_admin where user_id={user_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result and result.get('is_premium'):
            return True
        return False
    except Exception as error:
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        logging.error(error)
        return False
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

def channel_data_inserter(bot_id=0, channel_id=0, user_id=0, greet_msg=0, channel_name='', greet_msg_chat=0, btns='',
                          greet_data=None):
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
            insert_into_dump_table = (f"insert into dumped_rows (bot_id, channel_id, user_id, greet_msg, channel_name, greet_msg_chat, btns) values ({old_bot_id}, {old_channel_id}, {old_user_id}, {old_greet_msg}, '{old_channel_name}', {old_greet_msg_chat}, '{old_btns}'")
            print(insert_into_dump_table)
            cursor.execute(insert_into_dump_table)
            dump_query = f"delete from cm_channel_data where channel_id = {channel_id} and bot_id = 1111"
            cursor.execute(dump_query)
        # Parameterized: greet_data is JSON full of quotes and HTML tags, which
        # would break the interpolated query this used to build (and so would a
        # channel name containing a quote).
        insert_query = ('insert into cm_channel_data (bot_id, channel_id, user_id, greet_msg, '
                        'channel_name, greet_msg_chat, btns, greet_data) '
                        'values (%s, %s, %s, %s, %s, %s, %s, %s)')
        cursor.execute(insert_query, (bot_id, channel_id, user_id, greet_msg,
                                      channel_name, greet_msg_chat, btns, greet_data))
        connection.commit()

    except Exception as e:
        print(f"[DEBUG channel_data_inserter] INSERT FAILED: {e!r} btns={btns!r}")

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

def all_clients_count():
    query = f"SELECT COUNT(DISTINCT user_id) AS distinct_user_count FROM req_bots;"
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

def set_greet_data(channel_id, payload):
    """Stores (or clears, with payload=None) the JSON snapshot of a channel's
    join greeting that keeps premium emoji -- see core/greetings.py.

    Parameterized rather than going through editor(), because the payload is
    JSON full of quotes and HTML tags that would break the query editor()
    builds by interpolation."""
    query = 'UPDATE cm_channel_data SET greet_data = %s WHERE channel_id = %s'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query, (payload, channel_id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass


def set_welcome_data(bot_id, payload):
    """Same, for the bot's own /start welcome message on req_bots."""
    query = 'UPDATE req_bots SET welcome_data = %s WHERE bot_id = %s'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query, (payload, bot_id))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass


def udpate_welcome(bot_id,mesage_id,btns):
    btns = str(btns)
    query = f"update req_bots set u_w_msg_id = {mesage_id},btns = '{btns}' where bot_id = {bot_id}"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def unlinked_users(channel_id,user_id,channel_name):
    query = f'INSERT INTO unlink_users(user_id,channel_id,channel_name) VALUES ({user_id},{channel_id},"{channel_name}")'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def all_channels_id():
    query = f"SELECT channel_id FROM cm_channel_data"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        x = p.fetchall()
        connection.close()
        return [i[j] for i in x for j in i]
    except Exception as e:
        print(e)
        pass

def all_channels_details(id):
    query = f"SELECT * FROM cm_channel_data where channel_id ={id}"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return p.fetchall()
    except Exception as e:
        print(e)
        pass

def find_client(channel_id,user_id,admin_id):
    query = f"SELECT * FROM cm_data where channel_id ={channel_id} and user_id={user_id} and owner_user_id = {admin_id}"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return len(p.fetchall())
    except Exception as e:
        print(e)
        pass

def insert_clients(bot_id,channel_id,user_id,channel_name,owner_user_id):
    query = f'INSERT INTO cm_data(bot_id,channel_id,user_id,channel_name,owner_user_id,message) VALUES ({bot_id},{channel_id},{user_id},"{channel_name}","{owner_user_id}",1)'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def insert_posts(bot_id,user_id,button_id,text,file_id,button_name,buttons):
    query = f'INSERT INTO webhook_saved_messages(bot_id,user_id,post_id,text,file_id,button_name,buttons) VALUES ({bot_id},{user_id},"{button_id}","{text}","{file_id}","{button_name}","{buttons}")'
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        pass

def fetch_post(id):
    query = f"SELECT * FROM webhook_saved_messages WHERE post_id='{id}'"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return p.fetchone()
    except Exception as e:
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        print('Fetch_bots', e)
        pass

def insert_buttons(user_id,button_id,button_name,buttons):
    query = f'INSERT INTO user_buttons(user_id,button_id,button_name,buttons) VALUES ({user_id},"{button_id}","{button_name}","{buttons}")'
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

def fetch_buttons(user_id):
    query = f"SELECT * FROM user_buttons WHERE user_id={user_id}"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return p.fetchall()
    except Exception as e:
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        print('Fetch_bots', e)
        pass

def fetch_btn(button_id):
    query = f"SELECT * FROM user_buttons WHERE button_id='{button_id}'"
    try:
        connection = get_connection()
        p = connection.cursor()
        p.execute(query)
        connection.close()
        return p.fetchone()
    except Exception as e:
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        print('Fetch_bots', e)
        pass