from aiogram.fsm.state import State, StatesGroup


class default(StatesGroup):
    pic = State()

class MyChannels(StatesGroup):
    choose = State()
    show = State()
    edit = State()
    greet_msg_edit = State()
    greet_btn_edit = State()
    btn_edit = State()
    count = State()
    promo = State()
    run_promo = State()
    remove = State()

class AddChannel(StatesGroup):
    channel_id = State()
    greet_msg_confirm = State()
    greet_msg = State()
    btn_check = State()
    btn_handle = State()
    btn_enter = State()

class schedule(StatesGroup):
    yoyo = State()
    get_post = State()
    get_channel = State()


class my_users(StatesGroup):
    channels = State()
    user_count = State()
    channels_run = State()
    channels_run_send = State()
    channels_run_send_con = State()
    channels_run_send_conf = State()
    message = State()
    all_users = State()
