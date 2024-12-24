import requests
from aiogram import Router
from aiogram.enums import InlineQueryResultType
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedPhoto, \
    InlineKeyboardMarkup,InlineKeyboardButton
from models.database import fetch_post

router = Router(name="inline_handler")


@router.inline_query()
async def handle_inline_query(iquery: InlineQuery):
    if iquery.query.startswith("share"):
        try:
            post_id = iquery.query.split(" ")[1]
            try:
                message_details = fetch_post(post_id)
                if message_details['file_id'] !='None':
                    await iquery.answer( [
                    InlineQueryResultCachedPhoto(
                        type =InlineQueryResultType.PHOTO,
                        id = 'asfasdf',
                        title='Your Created Post',
                        description = 'Your Created Post',
                        photo_file_id=message_details['file_id'],
                        caption=message_details['text'],
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=eval(message_details['buttons']))
                    ),
                ])
                else:
                    await iquery.answer(
                        [InlineQueryResultArticle(id='14243143',
                                                  title="Your Created Post",
                                                  description="Here is the message you created.",
                                                  input_message_content=InputTextMessageContent(
                                                      message_text=message_details['text']),
                                                  reply_markup=InlineKeyboardMarkup(
                                                      inline_keyboard=eval(message_details['buttons'])))])

            except TypeError:
                pass
        except IndexError:
            pass
    else:
        await iquery.answer(
            [InlineQueryResultArticle(id='14243143', title="Invalid Command",
                                      description="This command is not recognized.",
                                      input_message_content=InputTextMessageContent(message_text='Hello! Please use a valid command.'))])
