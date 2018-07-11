import telebot
from telebot import types
import settings

admin_id = settings.ADMIN_ID
bot = telebot.TeleBot(settings.API_TOKEN)
print(bot.get_me())
# log about bot


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print("start/help")
    bot.send_message(message.chat.id, settings.HELLO_MESSAGE)


@bot.message_handler(content_types=['text', 'document', 'audio', 'photo'])
def handle_everything(message):
    print("message handler")
    bot.send_message(admin_id, settings.NEW_FEEDBACK)
    keyboard = types.InlineKeyboardMarkup()
    callback_button_yes = types.InlineKeyboardButton(settings.YES, callback_data='yes')
    callback_button_no = types.InlineKeyboardButton(settings.NO, callback_data='no')
    keyboard.add(callback_button_yes, callback_button_no)

    bot.send_message(message.chat.id, settings.SURE_TO_FORWARD, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print("callback handler")
    if call.message:
        if call.data == "yes":
            bot.forward_message(admin_id, call.message.chat.id, call.message.message_id - 2)
            # TODO: find another way to forward message (without id-2)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=settings.ACCEPT)

        elif call.data == "no":
            bot.send_message(admin_id, "@" + call.from_user.username + settings.NOT_SURE)
            # TODO: user can be without USERNAME?
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=settings.REJECT)


if __name__ == '__main__':
    bot.polling(none_stop=True,  interval=1)
