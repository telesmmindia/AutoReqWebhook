import asyncio
import traceback

from aiogram.enums import ChatMemberStatus
from colorama import Fore, Style

from core.texts import BROADCAST_SUMMARY
from models.database import udpate_message_state


async def is_bot_admin(channel_id,bot):
    try:
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=bot.id)
        return chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
    except:
        return False


async def send_message_broad(clients=0, forward_from=0, message_id=0, btn=0, usr_count=0,bot=None):
        try:
            error_count = 0
            count = 0
            for i in clients:
                if i > 0:
                    if int(count) < int(usr_count):
                        try:
                            print(i)
                            # Add timeout for each task
                            await asyncio.wait_for(
                                bot.copy_message(
                                    i, forward_from, message_id, reply_markup=btn if btn != 0 else None
                                ),
                                timeout=5  # Set timeout (e.g., 5 seconds)
                            )
                            count += 1
                        except asyncio.TimeoutError:
                            print(Fore.RED + f"Timeout while sending to {i}" + Style.RESET_ALL)
                            udpate_message_state(i)
                            error_count += 1
                        except Exception as e:
                            print(Fore.RED + f"Error sending to {i}: {e}" + Style.RESET_ALL)
                            udpate_message_state(i)
                            error_count += 1

            # Send completion message
            await bot.send_message(
                forward_from,
                BROADCAST_SUMMARY.format(count, error_count)
            )
        except Exception as error:
            print(Fore.RED + str(error) + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        finally:
            # Ensure the bot closes properly
            await bot.close()