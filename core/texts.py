
#--------------------------ALL LINKS-------------

TUTORIAL_CHANNEL_LINK="@ChannelGuruBot_Tutorials"
ALL_REQUEST_ACCEPT_DICT={"Add Channel":"https://t.me/ChannelGuruBot_Tutorials/4",
                         "My Channel":"https://t.me/ChannelGuruBot_Tutorials/5",
                         "Broadcast Message":"https://t.me/ChannelGuruBot_Tutorials/6"}
CREATE_BOT_DICT={"Create Bot Tutorial":"https://t.me/ChannelGuruBot_Tutorials/7",}
ADD_BUTTON_DICT={"Create Post With Button":"https://t.me/ChannelGuruBot_Tutorials/9","Use Saved Buttons Tutorial":"https://t.me/ChannelGuruBot_Tutorials/10"}
INLINE_MODE_DICT={"Inline Mode Tutorial":"https://t.me/ChannelGuruBot_Tutorials/8"}
BOT_WELCOME_DICT={"Set Bot's Welcome Message":"https://t.me/ChannelGuruBot_Tutorials/11"}
#--------------------------ALL LINKS-------------
DONT_KNOW_HOW_TO = """
<i>Don't know how to use this feature? ❓
Watch the video tutorial here 🎥👇</i>
"""

CHOOSE = "🔘 <b>Choose:</b>"
BOT_NOT_ADMIN = 'The Bot is not an Admin in your Channel ☹ Named\n<b>{}</b>\nMake sure the Bot is Admin and Resend the Post Here!'
FRWD_POST_FRM_CHNL_ONLY = '🔄 Please forward a message from your channel only'
GRT_SET_2_DEF = 'Greeting Message Set to:\n`Hey {username},\nYour Request is Accepted By Channel Guru Bot 🛐! \n\nTo Know My Features Send /start or /help!`'
GRT_MSG_DEFAULT = 'Hey <b>{}</b>,\nYour Request is Accepted By Channel Guru Bot 🛐! \n\nTo Know My Features Send /start or /help!'
FORWARD_YOUR_POST = "🔄 Forward a post from your channel"
CHANNEL_INSERTED = "Channel Data Inserted Successfully ✅📊"
BROADCAST_SUMMARY = """📊 <b>Broadcast Summary</b>
✅📩 Message sent to <b>{}</b> users
❌ Error Count: <b>{}</b>

<i>Send /start to see bot buttons!</i>
"""

DEFAULT_ACCEPTTED_TXT = '''👋 Hey <b>{}</b>,

🎉 Your request to join the channel <b>{}</b> has been accepted!  
To explore my features, send <code>/start</code> or <code>/help</code>.

<i>🤖 This bot is powered by @ChannelGuru_Bot ❤️</i>
'''

ENABLE_INLINE_MODE = (
    "⚙️ <b>Please enable Inline Mode on your bot!</b>\n\n"
    "📺 <i>For any help, watch the tutorial below!</i>"
)
FWD_POST_FR_BTN = "👉 Forward the post where you want to attach buttons, or\n💬 Send any message or picture!"
HOW_2_USE_POST_MKR = '''Hey there! Just a quick heads up:
• The prompt with the ➕ button is where you can <i>add options for your post</i>
• <b>"Get Post"</b> button creates the post with the buttons. 

That's it! Let me know if you have any questions. 
@ChannelGuru_Support'''
LNK_FRMT = '''🔗 Enter Link or Username For the Button!
Accepted Formats are - 👉"@[YourUsername]"
👉 https://[YOUR LINK]'''
INCRT_BTN_URL = '🚫🔗 The button URL is incorrect'
WHT_IS_GRT_MSG = "💬 <b>Select your greeting message</b>\nSend a Greeting Message for your Users or use the default Greeting Message👋🏼😊\nWarning: Do not delete the custom message from chat"
CHNL_ALRDY_ADDED = "📢 Channel already connected 👍\n🔄 Try another channel"
BOT_ADDED_WEBHOOK = "🚀 <b>@{}</b> is LIVE and has started successfully! 🎉 \nPlease start your bot and follow the steps to get started. 💡"
ERROR_MESSAGE_BOT_WEBHOOK = "⚠️ <b>Error Adding Bot</b>. Please contact the admin. 🛠️\n<i>ERROR:</i> {}"
BOT_ALREADY_AUTOVIEWS = '⚠️ This bot is already being used. Please use a different bot or remove this one.'
BOT_ALREADY_EXISTS = "⚠️ This bot already exists. Enter another token or send /start."
ENTER_A_VALID_TOKEN = "<b>Please enter a valid bot token:</b>"

HELP_TEXT = '''Channel Guru Bot 🛐🚀 - Your Ultimate Channel Management Assistant!

👉 Accept join requests and send personalized greeting messages 💌.
👉 Store subscriber details for easy access, even after they leave your channel 😉.
👉 Create eye-catching buttons for your posts to boost engagement 😍.

💡 Open to suggestions! New features coming soon 🔜🎥.'''

START_TEXT = '''Welcome To Channel Guru Bot! 🛐🫂!
Just Make Me Admin In Your Channel 🫡 & I Will Accept All Your Channel Requests!

To Know My Features Click 👉  /help !'''

def bot_details_text(bot_name, bot_token):
    return f"""
🤖 <b>Bot Username:</b> @{bot_name}
🔑 <b>Bot Token:</b> {bot_token}
✏️ Choose an option to edit.\n"""

CONFIRMATION_REMOVE_BOT = "❓ <b>Are you sure</b> you want to remove this bot? 🤖"
BOT_DELETED = "🗑️✅ The Bot has been deleted successfully."
NOT_ENOUGH_PEOPLE = "You Don't Have Anyone To Broadcast!"
ERROR_IN_ADDING_CHANNEL = 'There was some error in adding the channel. Please contact admin or retry'

SEND_GREETING_MESSAGE = '''👋 <b>Send your Greeting Message</b>\n

<i>📝 Note: This message will be sent to your user when a request is accepted by the bot.</i>\n
⚠️ <b>Warning:</b> Do not delete this custom message from the chat.'''
CONFIRM_SET_MESSAGE = "❓ Are you sure you want to set this message?"
CANCELLED = "❌ Cancelled"
UNKNOWN_CHOICE = "⚠️ Unknown Choice"
BROADCAST_MESSAGE_PROMPT = "📤 For how many users do you want to broadcast the message?"
SELECT_CHANNEL_PROMPT = "📱 Select a channel to get the user count"
USER_COUNT_MESSAGE = "👥 You have {} users in this channel"
SEND_TO_USERS_PROMPT = "📤 Send message to how many users?"
SEND_MESSAGE_PROMPT = "✉️ Send a message you want to broadcast!"

ENTER_NUMBER_ONLY = "🔢 Please enter a number only."
USER_COUNT_BROADCAST = "👥 You have {} users in this channel\n\n🔢 Enter the number of users you want to broadcast:"

CONFIRM_RUN_MESSAGE = "❓ Are you sure you want to run this message?"
TOTAL_USERS_MESSAGE = "👥 You have a total of {} users!"
NO_USERS_MESSAGE = '🚫👥 You don\'t have any users'
YOUR_CHANNELS = "📡📈 Your Channels"
CHANNEL_DETAILS = """📢 <b>Channel Name</b>: {}
🔑 <b>Channel ID</b>: {}"""
EDIT_OPTIONS = "✏️ Edit Options"
NO_POST_CREATED = "❌ No post created"
BROADCAST_USER_COUNT = "<i>👥 You have <b>{}</b> users in this channel</i>\n\n🔢 Enter the number of users you want to broadcast your message:"
GREETING_MESSAGE_CHANNEL = "🎉 Your Greeting Message for this Channel is 👇"
SEND_NEW_WELCOME_MSG = "🌟 Send a new welcome message"
CONFIRM_WELCOME_MSG = "🤔 Are you sure you want to set this message as the welcome message?"
UPDATED_WELCOME_TEXT = "✅ Welcome text updated successfully!"

CONFIRM_REMOVE_CHANNEL = "❓ Are you sure you want to remove this channel?"
CHANNEL_REMOVED_SUCCESS = "✅ Channel removed successfully"
SEND_BROADCAST_MESSAGE = "🔚 Send your message or post for broadcast"
SENDING_MESSAGE_TO_USERS = "<b>📢 Broadcast has been started</b>.\n<i>You will receive a broadcast summary once it's completed.</i>"
SEND_NEW_POST = "📝 Send New Post"
GREET_MESSAGE_STORED = "🎉 Greet message stored 📥"
CONFIRM_SET_GREETING_MESSAGE = "❓ Are you sure you want to set this message as your greet message?"
GREET_MESSAGE_UPDATED = "🎉 Greet message updated successfully ✅📊"
ENTER_BOT_TOKEN = "🔑 Enter Your Bot Token:"
YOUR_BOTS = "🤖 Your bots are"
CANNOT_EDIT_STICKERS = "❌ Cannot edit stickers\n🔄 Try something else"
YOUR_POST = "Click on the + button to add buttons! \n📄 Your post is"
SEND_TEXT_FOR_BUTTON = "🔤 Send text for button"
NO_BUTTONS_ADDED = "❌ No buttons added"
ENTER_TEXT_ONLY = "🔤 Enter text only"
BUTTON_SAVED = "✅ Button saved"
MAX_BUTTONS_LIMIT = "🛑🤚 You can only add 5 buttons"
CHANNEL_USER_COUNT = "👥 You have {} users in this channel"
ENTER_A_NAME_FOR_BUTTON_SET = 'Enter a name for button set'
BUTTON_INSERTED = "✅ Button Inserted"
SHARE_POST = '''
You can share the post anywhere using this command, make sure the bot is admin in the channel:  
🔑 @{} share {}  

📲 Tap the buttons to share!'''

UR_BTN = "🟢 Your buttons are"
UR_BTN_IS = '🔘 Your button is'
SND_POST_FR_BTN_ADD = '📤 Send a post to attach these buttons'
SELECT_CHANNELS = "📡 Select channels to send the message"
MSG_SNT_TO_CHANNEL = "✅ Message sent to the selected channel"
MSG_SNT_TO_CHANNEL_ALL = "✅ Message sent to all channels"
ADD_CHANNEL = "📢 <b>Click on the button below to add a channel.</b> ⬇️"
CHANNEL_SAVED = "✅ <b>Channel saved successfully!</b> 🎉"