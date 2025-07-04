from aiogram.types import ChatAdministratorRights, KeyboardButtonRequestChat
from aiogram.utils.keyboard import ReplyKeyboardBuilder

required_admin_rights = ChatAdministratorRights(
    is_anonymous=False,
    can_manage_chat=True,
    can_delete_messages=False,
    can_manage_video_chats=False,
    can_restrict_members=False,
    can_promote_members=True,
    can_change_info=True,
    can_invite_users=True,
    can_post_stories=False,
    can_edit_stories=False,
    can_delete_stories=False,
    can_post_messages=True,
    can_edit_messages=False,
    can_pin_messages=False,
    can_manage_topics=False
)

required_bot_rights = ChatAdministratorRights(
    is_anonymous=False,
    can_manage_chat=True,
    can_delete_messages=False,
    can_manage_video_chats=False,
    can_restrict_members=False,
    can_promote_members=False,
    can_change_info=False,
    can_invite_users=True,
    can_post_stories=False,
    can_edit_stories=False,
    can_delete_stories=False,
    can_post_messages=False,
    can_edit_messages=False,
    can_pin_messages=False,
    can_manage_topics=False
)

def get_n_cancel() :
    return ReplyKeyboardBuilder().button(text='❌ Cancel').as_markup()

def back_button():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='⬅️ Back')
    return keyboard_builder.as_markup(resize_keyboard=True)

def add_channel_request():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='➕ Add Channel',
                            request_chat=KeyboardButtonRequestChat(
                                request_id=1,
                                chat_is_channel=True,
                                bot_is_member=False,
                                user_administrator_rights=required_admin_rights,
                                bot_administrator_rights= required_bot_rights,
                                request_title=True,
                                request_username=True
                            ))
    keyboard_builder.button(text='❌ Cancel')
    return keyboard_builder.as_markup()