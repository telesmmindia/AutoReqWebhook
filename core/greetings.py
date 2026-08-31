"""Storage and delivery of owner-authored messages, preserving premium
(custom/animated) emoji.

Greetings used to live only as a pointer to the owner's own message -- the
per-channel join greeting as `cm_channel_data.greet_msg` + `greet_msg_chat`,
the bot's own /start welcome as `req_bots.u_w_msg_id` -- which we replayed with
`copy_message`. A copy is made server-side from a message the bot did not
author, so Telegram drops the custom-emoji entities in it and members see the
plain fallback emoji instead of the animated one.

So we additionally snapshot the message here: its text/caption is stored as
HTML, in which aiogram renders every premium emoji as
`<tg-emoji emoji-id="5368324170671202286">emoji</tg-emoji>` -- that emoji-id is
the custom emoji's document id -- plus the `file_id` of any attached media.
Sending that snapshot back out is a message the bot composes itself, so the
emoji ids survive and members get the animated emoji.

Every function takes the `bot` to send through, because this is a multibot
webhook service: there is no module-level bot, each update is handled by the
user's own bot instance.

Telegram only lets a bot put custom emoji in its own messages when the bot
purchased an additional username on Fragment, or the bot owner has Telegram
Premium. When it refuses, the send is retried without the `<tg-emoji>`
wrappers so the message still lands, just with plain emoji.
"""
import json
import re

from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import InlineKeyboardBuilder

SNAPSHOT_VERSION = 1

# Attachment kinds we can re-send from a stored file_id, mapped to the Bot API
# method that takes that file_id. Order matters: an animation also carries a
# `document`, so it has to be matched first.
_MEDIA_SENDERS = {
    'photo': 'send_photo',
    'video': 'send_video',
    'animation': 'send_animation',
    'audio': 'send_audio',
    'voice': 'send_voice',
    'document': 'send_document',
    'video_note': 'send_video_note',
    'sticker': 'send_sticker',
}

# These carry no caption, so a snapshot of one keeps only the file_id.
_CAPTIONLESS = ('sticker', 'video_note')

_TG_EMOJI_TAG = re.compile(r'<tg-emoji\s+emoji-id="\d+">(.*?)</tg-emoji>', re.DOTALL)


def _extract_media(message):
    """Returns (media_type, file_id) for the attachment on `message`, or
    (None, None) for a plain text message."""
    for media_type in _MEDIA_SENDERS:
        media = getattr(message, media_type, None)
        if not media:
            continue
        if media_type == 'photo':
            # Largest available size -- message.photo is ascending by size.
            return media_type, media[-1].file_id
        return media_type, media.file_id
    return None, None


def snapshot_message(message):
    """Serializes an owner's message into the JSON we store alongside the old
    message pointer. `message.html_text` is what carries the premium emoji:
    every custom_emoji entity comes back out as a <tg-emoji emoji-id="..."> tag."""
    try:
        media_type, file_id = _extract_media(message)
        html = '' if media_type in _CAPTIONLESS else (message.html_text or '')
        return json.dumps({
            'v': SNAPSHOT_VERSION,
            'media_type': media_type,
            'file_id': file_id,
            'html': html,
        })
    except Exception as e:
        # A message that can't be snapshotted still works via copy_message.
        print(f'Could not snapshot message: {e}')
        return None


def _load(snapshot):
    if not snapshot or snapshot in ('None', '0', 0):
        return None
    try:
        data = json.loads(snapshot)
    except (TypeError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    if not data.get('html') and not data.get('file_id'):
        return None
    return data


def strip_custom_emoji(html):
    """Replaces every <tg-emoji> wrapper with the plain emoji inside it, which
    is the fallback Telegram itself shows where a custom emoji can't render."""
    return _TG_EMOJI_TAG.sub(r'\1', html or '')


def greeting_markup(btns):
    """Rebuilds a saved inline keyboard, or None when there is none. The column
    holds a repr of the keyboard rows."""
    if btns in (None, 'None', '0', 0, ''):
        return None
    try:
        return InlineKeyboardBuilder(eval(btns)).as_markup()
    except Exception:
        return None


async def _send(bot, chat_id, data, html, reply_markup):
    media_type = data.get('media_type')
    file_id = data.get('file_id')
    if media_type and file_id:
        sender = getattr(bot, _MEDIA_SENDERS[media_type])
        if media_type in _CAPTIONLESS:
            return await sender(chat_id, file_id, reply_markup=reply_markup)
        return await sender(chat_id, file_id, caption=html or None,
                            parse_mode='HTML', reply_markup=reply_markup)
    return await bot.send_message(chat_id, html, parse_mode='HTML',
                                  disable_web_page_preview=True,
                                  reply_markup=reply_markup)


async def send_snapshot(bot, chat_id, snapshot, reply_markup=None):
    """Sends a stored snapshot to `chat_id`, keeping its premium emoji.
    Returns the sent Message, or None when there's no usable snapshot.
    Delivery errors other than a rejected custom emoji propagate, so callers
    can fall back to copy_message."""
    data = _load(snapshot)
    if data is None:
        return None
    html = data.get('html') or ''
    try:
        return await _send(bot, chat_id, data, html, reply_markup)
    except TelegramBadRequest as e:
        # This bot isn't allowed to use custom emoji (no Fragment username and
        # no Premium owner). Send it with the fallback emoji rather than not
        # at all.
        if 'emoji' not in str(e).lower():
            raise
        plain = strip_custom_emoji(html)
        if plain == html:
            raise
        return await _send(bot, chat_id, data, plain, reply_markup)


async def send_stored_message(bot, chat_id, snapshot, from_chat_id, message_id,
                              reply_markup=None):
    """Delivers a stored owner message to `chat_id`.

    Prefers the snapshot (premium emoji intact) and falls back to replaying the
    owner's original message for rows saved before snapshots existed. Raises if
    neither path works, so callers keep their existing error handling.

    Returns the sent Message on the snapshot path, or the MessageId that
    copy_message returns on the fallback path -- so a caller that wants to
    reply to what it just sent must check it actually got a Message."""
    try:
        sent = await send_snapshot(bot, chat_id, snapshot, reply_markup)
        if sent is not None:
            return sent
    except Exception as e:
        print(f'Snapshot send failed, falling back to copy: {e}')
    return await bot.copy_message(chat_id, from_chat_id, message_id,
                                  reply_markup=reply_markup)
