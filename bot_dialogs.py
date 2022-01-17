import DB_log
import bot_commands
from data_checks import is_float, check_date
from datetime import datetime, date
from telebot_calendar import Calendar, CallbackData
from telebot.types import Message
from loader import bot, query_headers, key


calendar = Calendar()
calendar_callback = CallbackData("name", "action", "year", "month", "day")


def get_ch_in(message):
    now = date.today()
    bot.send_message(message.from_user.id,
                     'Select check-in date',
                     reply_markup=calendar.create_calendar(
                         name='ch_in_calendar',
                         year=now.year,
                         month=now.month
                        )
                     )
    if not isinstance(message, Message):
        message = message.message
    bot.register_next_step_handler(message, get_tapped_ch_in)


def get_ch_out(message):
    now = datetime.strptime(query_headers[message.from_user.id].ch_in, '%Y-%m-%d')
    bot.send_message(message.from_user.id,
                     'Select check-out date',
                     reply_markup=calendar.create_calendar(
                         name='ch_out_calendar',
                         year=now.year,
                         month=now.month
                        )
                     )
    if not isinstance(message, Message):
        message = message.message
    bot.register_next_step_handler(message, get_tapped_ch_out)


def get_tapped_ch_in(message):
    bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1, reply_markup='')
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    if check_date(message.text) is not None:
        delta = datetime.strptime(message.text, '%Y-%m-%d') - datetime.now()
        if delta.days < 0:
            bot.send_message(message.from_user.id, 'Date must be more then current date!')
            get_ch_in(message)
        else:
            query_headers[message.from_user.id].ch_in = message.text
            bot.send_message(message.from_user.id, 'Successfully')
            get_ch_out(message)
    else:
        bot.send_message(message.from_user.id, 'Incorrect Data type!')
        get_ch_in(message)


def get_tapped_ch_out(message):
    bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1, reply_markup='')
    bot.clear_step_handler_by_chat_id(message.from_user.id)
    if check_date(message.text) is not None:
        delta = datetime.strptime(message.text, '%Y-%m-%d') - datetime.strptime(query_headers[message.from_user.id].ch_in, '%Y-%m-%d')
        if delta.days < 0:
            bot.send_message(message.from_user.id, 'Check-out date must be more then check-in date!')
            get_ch_out(message)
        else:
            query_headers[message.from_user.id].ch_out = message.text
            bot.send_message(message.from_user.id, 'Check-out date successfully')
            bot.send_message(message.from_user.id, 'Enter the City')
            bot.register_next_step_handler(message, get_city)
    else:
        bot.send_message(message.from_user.id, 'Incorrect Data type!')
        get_ch_out(message)


def get_city(message):
    query_headers[message.from_user.id].city = message.text
    if query_headers[message.from_user.id].command == 'bestdeal':
        bot.send_message(message.from_user.id, 'Enter minimum hotel`s price')
        bot.register_next_step_handler(message, get_min_price)
    else:
        bot.send_message(message.from_user.id, 'Enter maximum hotels count (max 25)')
        bot.register_next_step_handler(message, get_hotels_count)


def get_min_price(message):
    if not is_float(message.text):
        bot.send_message(message.from_user.id, 'It must be number!')
        bot.register_next_step_handler(message, get_min_price)
    if float(message.text) <= 0:
        bot.send_message(message.from_user.id, 'A number must be more than 0!')
        bot.register_next_step_handler(message, get_min_price)
    else:
        query_headers[message.from_user.id].min_price = float(message.text)
        bot.send_message(message.from_user.id, 'Enter maximum hotel`s price')
        bot.register_next_step_handler(message, get_max_price)


def get_max_price(message):
    if not is_float(message.text):
        bot.send_message(message.from_user.id, 'It must be number!')
        bot.register_next_step_handler(message, get_max_price)
    if query_headers[message.from_user.id].min_price > float(message.text):
        bot.send_message(message.from_user.id, 'A number must be more minimum price!')
        bot.register_next_step_handler(message, get_max_price)
    else:
        query_headers[message.from_user.id].max_price = float(message.text)
        bot.send_message(message.from_user.id, 'Enter minimum distance from city center')
        bot.register_next_step_handler(message, get_min_distance)


def get_min_distance(message):
    if not is_float(message.text):
        bot.send_message(message.from_user.id, 'It must be number!')
        bot.register_next_step_handler(message, get_min_distance)
    if float(message.text) <= 0:
        bot.send_message(message.from_user.id, 'A number must be more 0!')
        bot.register_next_step_handler(message, get_min_distance)
    else:
        query_headers[message.from_user.id].min_dist = float(message.text)
        bot.send_message(message.from_user.id, 'Enter maximum distance from city center')
        bot.register_next_step_handler(message, get_max_distance)


def get_max_distance(message):
    if not is_float(message.text):
        bot.send_message(message.from_user.id, 'It must be number!')
        bot.register_next_step_handler(message, get_max_distance)
    if query_headers[message.from_user.id].min_dist > float(message.text):
        bot.send_message(message.from_user.id, 'A number must be more minimum price!')
        bot.register_next_step_handler(message, get_max_distance)
    else:
        query_headers[message.from_user.id].max_dist = float(message.text)
        bot.send_message(message.from_user.id, 'Enter maximum hotels count (max 25)')
        bot.register_next_step_handler(message, get_hotels_count)


def get_hotels_count(message):
    if not str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'An integer number required!')
        bot.register_next_step_handler(message, get_hotels_count)
    elif int(message.text) > 25 or int(message.text) < 1:
        bot.send_message(message.from_user.id, 'An integer number must be more than 0 and less then 26!')
        bot.register_next_step_handler(message, get_hotels_count)
    else:
        query_headers[message.from_user.id].hotels_count = int(message.text)
        bot.send_message(message.from_user.id, 'Load hotel`s photos?')
        bot.register_next_step_handler(message, need_photo)


def need_photo(message):
    if message.text in ['yes', 'Yes', 'Y', 'y']:
        query_headers[message.from_user.id].need_photo = True
        bot.send_message(message.from_user.id, 'How many photos load for each hotel?')
        bot.register_next_step_handler(message, get_photo_count)
    else:
        query_headers[message.from_user.id].need_photo = False
        bot.send_message(message.from_user.id, 'OK! Please wait! I`m looking for hotels!')

        # make result dictionary
        if query_headers[message.from_user.id].command == 'lowprice':
            res = bot_commands.low_price(city=query_headers[message.from_user.id].city, api_key=key,
                                         ch_in=query_headers[message.from_user.id].ch_in,
                                         ch_out=query_headers[message.from_user.id].ch_out,
                                         count=query_headers[message.from_user.id].hotels_count, photos=0)
        elif query_headers[message.from_user.id].command == 'highprice':
            res = bot_commands.high_price(city=query_headers[message.from_user.id].city, api_key=key,
                                          ch_in=query_headers[message.from_user.id].ch_in,
                                          ch_out=query_headers[message.from_user.id].ch_out,
                                          count=query_headers[message.from_user.id].hotels_count, photos=0)
        elif query_headers[message.from_user.id].command == 'bestdeal':
            res = bot_commands.best_deal(city=query_headers[message.from_user.id].city, api_key=key,
                                         ch_in=query_headers[message.from_user.id].ch_in,
                                         ch_out=query_headers[message.from_user.id].ch_out,
                                         min_price=query_headers[message.from_user.id].min_price,
                                         max_price=query_headers[message.from_user.id].max_price,
                                         min_dist=query_headers[message.from_user.id].min_dist,
                                         max_dist=query_headers[message.from_user.id].max_dist,
                                         count=query_headers[message.from_user.id].hotels_count, photos=0)
            res = dict(sorted(res.items(), key=lambda x: x[1]['price']))
        if res is not None:
            hotels_list = ''
            if len(res) == 0:
                bot.send_message(message.from_user.id, 'No hotels was found!!!')
            i_num = 0
            for odr_num in res:
                i_num += 1
                hotel_url = 'https://ru.hotels.com/ho{id}/?q-check-in={ch_in}&q-check-out={ch_out}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&f-hotel-id={id}'.format(
                    id=res[odr_num]['id'], ch_in=query_headers[message.from_user.id].ch_in,
                    ch_out=query_headers[message.from_user.id].ch_out
                )
                mess = '{num}:\n    Hotel name: {name}\n    Address: {address}\n    Distance from city center: {dist}' \
                       '\n    Price (average for 1 night): ${price}' \
                       '\n    Booking page: {url}'.format(
                    num=i_num, name=res[odr_num]['name'], address=res[odr_num]['address'], dist=res[odr_num]['dist'],
                    price=res[odr_num]['price'], url=hotel_url
                )
                hotels_list += res[odr_num]['name'] + ';' + str(res[odr_num]['id']) + ';'
                bot.send_message(message.from_user.id, mess)
            logged = DB_log.write_req(req_id=query_headers[message.from_user.id].command_id,
                                      in_user_id=query_headers[message.from_user.id].user_id,
                                      req_time=query_headers[message.from_user.id].command_date,
                                      in_command=query_headers[message.from_user.id].command,
                                      in_city=query_headers[message.from_user.id].city,
                                      in_hotels=hotels_list)
            if not logged:
                bot.send_message(message.from_user.id, 'Something wrong with the DataBase! '
                                                       'History of request was not saved!')
        else:
            bot.send_message(message.from_user.id, 'Sorry! An connection error was registered! Try again later!')


def get_photo_count(message):
    if not str(message.text).isdigit():
        bot.send_message(message.from_user.id, 'An integer number required!')
        bot.register_next_step_handler(message, get_photo_count)
    elif int(message.text) > 10 or int(message.text) < 1:
        bot.send_message(message.from_user.id, 'An integer number must be more than 0 and less then 11!')
        bot.register_next_step_handler(message, get_photo_count)
    else:
        query_headers[message.from_user.id].photo_count = int(message.text)
        bot.send_message(message.from_user.id, 'OK! Please wait! I`m looking for hotels!')

        # make result dictionary
        if query_headers[message.from_user.id].command == 'lowprice':
            res = bot_commands.low_price(city=query_headers[message.from_user.id].city, api_key=key,
                                         ch_in=query_headers[message.from_user.id].ch_in,
                                         ch_out=query_headers[message.from_user.id].ch_out,
                                         count=query_headers[message.from_user.id].hotels_count,
                                         photos=query_headers[message.from_user.id].photo_count)
        elif query_headers[message.from_user.id].command == 'highprice':
            res = bot_commands.high_price(city=query_headers[message.from_user.id].city, api_key=key,
                                          ch_in=query_headers[message.from_user.id].ch_in,
                                          ch_out=query_headers[message.from_user.id].ch_out,
                                          count=query_headers[message.from_user.id].hotels_count,
                                          photos=query_headers[message.from_user.id].photo_count)
        elif query_headers[message.from_user.id].command == 'bestdeal':
            res = bot_commands.best_deal(city=query_headers[message.from_user.id].city, api_key=key,
                                         ch_in=query_headers[message.from_user.id].ch_in,
                                         ch_out=query_headers[message.from_user.id].ch_out,
                                         min_price=query_headers[message.from_user.id].min_price,
                                         max_price=query_headers[message.from_user.id].max_price,
                                         min_dist=query_headers[message.from_user.id].min_dist,
                                         max_dist=query_headers[message.from_user.id].max_dist,
                                         count=query_headers[message.from_user.id].hotels_count,
                                         photos=query_headers[message.from_user.id].photo_count)
            res = dict(sorted(res.items(), key=lambda x: x[1]['price']))
        if res is not None:
            if len(res) == 0:
                bot.send_message(message.from_user.id, 'No hotels was found!!!')
            hotels_list = ''
            i_num = 0
            for odr_num in res:
                i_num += 1
                hotel_url = 'https://ru.hotels.com/ho{id}/?q-check-in={ch_in}&q-check-out={ch_out}&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&f-hotel-id={id}'.format(
                    id=res[odr_num]['id'], ch_in=query_headers[message.from_user.id].ch_in,
                    ch_out=query_headers[message.from_user.id].ch_out
                )
                mess = '{num}:\n    Hotel name: {name}\n    Address: {address}\n    Distance from city center: {dist}' \
                       '\n    Price (average for 1 night): ${price}' \
                       '\n    Booking page: {url}'.format(
                    num=i_num, name=res[odr_num]['name'], address=res[odr_num]['address'], dist=res[odr_num]['dist'],
                    price=res[odr_num]['price'], url=hotel_url
                )
                hotels_list += res[odr_num]['name'] + ';' + str(res[odr_num]['id']) + ';'
                bot.send_message(message.from_user.id, mess)
                for url in res[odr_num]['photos_url']:
                    bot.send_message(message.from_user.id, url)
            logged = DB_log.write_req(req_id=query_headers[message.from_user.id].command_id,
                                      in_user_id=query_headers[message.from_user.id].user_id,
                                      req_time=query_headers[message.from_user.id].command_date,
                                      in_command=query_headers[message.from_user.id].command,
                                      in_city=query_headers[message.from_user.id].city,
                                      in_hotels=hotels_list)
            if not logged:
                bot.send_message(message.from_user.id, 'Something wrong with the DataBase! '
                                                       'History of request was not saved!')
        else:
            bot.send_message(message.from_user.id, 'Sorry! An connection error was registered! Try again later!')
