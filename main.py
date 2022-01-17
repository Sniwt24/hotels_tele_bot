import hendlers
from datetime import datetime
import bot_dialogs
from loader import bot, query_headers
from telebot.types import ReplyKeyboardRemove, CallbackQuery
from bot_dialogs import calendar, calendar_callback


@bot.callback_query_handler(func=lambda call: call.data.startswith('ch_in_calendar'))
def callback_inline(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    sel_date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        delta = sel_date - datetime.now()
        if delta.days < 0:
            bot.send_message(call.from_user.id, 'Selected date must be more then today!',
                             reply_markup=ReplyKeyboardRemove())
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot_dialogs.get_ch_in(call)
        else:
            bot.send_message(call.from_user.id, f"Check-in date chosen: {sel_date.strftime('%Y-%m-%d')}",
                             reply_markup=ReplyKeyboardRemove())
            query_headers[call.from_user.id].ch_in = sel_date.strftime('%Y-%m-%d')
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot_dialogs.get_ch_out(call)
    elif action == "CANCEL":
        bot.clear_step_handler_by_chat_id(call.from_user.id)
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('ch_out_calendar'))
def callback_inline(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    sel_date = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )
    if action == "DAY":
        delta = sel_date - datetime.strptime(query_headers[call.from_user.id].ch_in, '%Y-%m-%d')
        if delta.days < 0:
            bot.send_message(call.from_user.id, 'Selected date must be more then check-in date!',
                             reply_markup=ReplyKeyboardRemove())
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot_dialogs.get_ch_out(call)
        else:
            bot.send_message(call.from_user.id, f"Check-out date chosen: {sel_date.strftime('%Y-%m-%d')}",
                             reply_markup=ReplyKeyboardRemove())
            query_headers[call.from_user.id].ch_out = sel_date.strftime('%Y-%m-%d')
            bot.send_message(call.from_user.id, 'Enter the City')
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.register_next_step_handler(call.message, bot_dialogs.get_city)
    elif action == "CANCEL":
        bot.clear_step_handler_by_chat_id(call.from_user.id)
        bot.send_message(
            chat_id=call.from_user.id,
            text="Cancellation",
            reply_markup=ReplyKeyboardRemove(),
        )


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, 'Hello I`m HelperForFindBot (you can find me as Hotels_finder_bot in telegram),'
                          ' and I can help you to find the best hotel!'
                          'Ok! I have this commands:'
                          '\n/hello: My greetings for you!'
                          '\n/lowprice: find hotel with the lowest price'
                          '\n/highprice: find hotel with the highest price'
                          '\n/bestdeal: find best hotels by price and destination'
                          '\n/history: history of hotels search'
                          '\n/help: view my commands')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Ok! I have this commands:'
                          '\n/hello: My greetings for you!'
                          '\n/lowprice: find hotel with the lowest price'
                          '\n/highprice: find hotel with the highest price'
                          '\n/bestdeal: find best hotels by price and destination'
                          '\n/history: history of hotels search'
                          '\n/help: view my commands')


@bot.message_handler(regexp=r"Hello")
def send_hello(message):
    send_hello(message)


@bot.message_handler(commands=['hello', 'hello-world'])
def send_hello(message):
    bot.reply_to(message, 'Hello I`m HelperForFindBot (you can find me as Hotels_finder_bot in telegram),'
                          ' and I can help you to find the best hotel!')


@bot.message_handler(commands=['lowprice'])
def send_lowprice(message):
    query_headers[message.from_user.id] = hendlers.Headers()
    query_headers[message.from_user.id].command = 'lowprice'
    query_headers[message.from_user.id].command_date = datetime.today()
    command_id = int(str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + \
                     str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + \
                     str(datetime.today().microsecond))
    query_headers[message.from_user.id].command_id = command_id
    query_headers[message.from_user.id].user_id = message.from_user.id
    bot_dialogs.get_ch_in(message)


@bot.message_handler(commands=['highprice'])
def send_highprice(message):
    query_headers[message.from_user.id] = hendlers.Headers()
    query_headers[message.from_user.id].command = 'highprice'
    query_headers[message.from_user.id].command_date = datetime.today()
    command_id = int(str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + \
                     str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + \
                     str(datetime.today().microsecond))
    query_headers[message.from_user.id].command_id = command_id
    query_headers[message.from_user.id].user_id = message.from_user.id
    bot_dialogs.get_ch_in(message)


@bot.message_handler(commands=['bestdeal'])
def send_bestdeal(message):
    query_headers[message.from_user.id] = hendlers.Headers()
    query_headers[message.from_user.id].command = 'bestdeal'
    query_headers[message.from_user.id].command_date = datetime.today()
    command_id = int(str(datetime.today().year) + str(datetime.today().month) + str(datetime.today().day) + \
                     str(datetime.today().hour) + str(datetime.today().minute) + str(datetime.today().second) + \
                     str(datetime.today().microsecond))
    query_headers[message.from_user.id].command_id = command_id
    query_headers[message.from_user.id].user_id = message.from_user.id
    bot_dialogs.get_ch_in(message)


@bot.message_handler(commands=['history'])
def send_death_count(message):
    bot.reply_to(message, 'Here will be command "history"')


if __name__ == '__main__':
    bot.infinity_polling()
