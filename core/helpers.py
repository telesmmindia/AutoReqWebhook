import asyncio

from aiogram.enums import ChatMemberStatus

from models.database import udpate_message_state


async def is_bot_admin(channel_id,bot):
    try:
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=bot.id)
        return chat_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
    except:
        return False

def n(a=0,b=0,c=0,d=0,e=0,f=0):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message(a,b,c,d,e))
    loop.close()

async def send_message(clients=0,forward_from=0,message_id=0,btn=0,usr_count=0,bot=None):
    error_count = 0
    count = 0
    for i in clients:
        if i >0:
            if int(count)<int(usr_count):
                try:
                    print(i)
                    if btn == 0:
                        await bot.copy_message(i,forward_from,message_id)
                    else:
                        await bot.copy_message(i,forward_from,message_id,reply_markup=btn)

                    count+=1
                    #await asyncio.sleep(10)
                except Exception as e:
                    udpate_message_state(i)
                    print(e)
                    error_count += 1
                    pass

    await bot.send_message(forward_from,f'✅📩 Message sent to {count} users\n👥💰 {count} credits deducted')
    await bot.close()