import time

import telebot
from telebot import types
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
import datetime

token = "5961017567:AAGU_qJ5WNI1sDaH7BlADwEbPDg806HXqcg"

max_diary = telebot.TeleBot(token)
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.datetime.now()
keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(types.KeyboardButton("registration".title()),
                   types.KeyboardButton("authorization".title()))

keyboard_inlines = types.InlineKeyboardMarkup()
keyboard_inlines.add(types.InlineKeyboardButton(text="Добавить задачу", callback_data="add"),
                     types.InlineKeyboardButton(text="Cмотреть задачу", callback_data="see"),
                     types.InlineKeyboardButton(text="Удалить задачу", callback_data="del"))

time_in = time.time()


@max_diary.message_handler(commands=['start'])
def start(message):
    max_diary.send_message(message.chat.id,
                           f"Добро пожаловать,  {message.from_user.first_name}!\nПожалуйста пройдите регистрацию"
                           f" если вы не зарегестрированный пользователь\n"
                           f"или авторезируйтесь если вы есть в системе !",
                           reply_markup=keyboard_start)


@max_diary.message_handler(content_types=["text"])
def get_bot(message):
    if message.text.lower() == "registration":
        max_diary.register_next_step_handler(max_diary.send_message(message.chat.id, "Введите логин"), registration)
    elif message.text.lower() == "authorization":
        max_diary.register_next_step_handler(
            max_diary.send_message(message.chat.id, "Введите логин"), authorization)


@max_diary.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1.sep)
    global date
    date = calendar.calendar_query_handler(bot=max_diary, call=call, name=name, action=action, year=year, month=month,
                                           day=day)

    if action == 'DAY':
        max_diary.register_next_step_handler(max_diary.send_message(chat_id=call.from_user.id,
                                                                    text=f'Вы выбрали {date.strftime("%d.%m.%Y")},'
                                                                         f' теперь напишите задачу',
                                                                    ), file_w)

    elif action == 'CANCEL':
        max_diary.send_message(chat_id=call.from_user.id, text='Отмена', reply_markup=types.ReplyKeyboardRemove())


@max_diary.callback_query_handler(func=lambda call: True)
def firs(call):
    with open("reg.txt", "r") as file_log:
        login = file_log.read().split('\n')
        print(login)
        for el in range(len(login) - 1):
            print(login[el].split()[1])
            if (time_in - float(login[el].split()[1])) < 86400:
                print("1")
                with open("file.txt", "r") as file_first:
                    file_1 = file_first.readlines()
                print("1")
                if call.data == "add":
                    print("1")
                    max_diary.send_message(call.message.chat.id, "Выбирете дату",
                                           reply_markup=calendar.create_calendar(
                                               name=calendar_1.prefix,
                                               year=now.year,
                                               month=now.month))
                    break
                elif call.data == "see":
                    # with open("file.txt", "r") as file1:
                    #     send = file1.read()
                    #     max_diary.send_message(call.message.chat.id, send)
                    inlines_1 = types.InlineKeyboardMarkup()
                    inlines_1.add(types.InlineKeyboardButton(text="Посмотреть все", callback_data="all"),
                                  (types.InlineKeyboardButton(text="Выбрать по дате", callback_data="date")))
                    max_diary.send_message(call.message.chat.id, "Выберете что вам показать", reply_markup=inlines_1)
                elif call.data == "all":
                    with open("file.txt", "r") as file4:
                        send = file4.read()
                    max_diary.send_message(call.message.chat.id, send)
                elif call.data == "date":
                    inlines = types.InlineKeyboardMarkup()
                    with open("file.txt", "r") as f:
                        date_file = f.readlines()
                        for g in date_file:
                            inlines.add(
                                types.InlineKeyboardButton(text=g.split(" ")[len(g.split(" ")) - 2], callback_data=g))
                        max_diary.send_message(call.message.chat.id, "Даты задач", reply_markup=inlines)
                elif call.data == "del":
                    inlines = types.InlineKeyboardMarkup()
                    with open("file.txt", "r") as file_del:
                        file_for_del = file_del.readlines()
                        for j in file_for_del:
                            inlines.add(types.InlineKeyboardButton(text=j, callback_data=j))

                        max_diary.send_message(call.message.chat.id, f"Нажмите на задачу чтобы удалить ее",
                                               reply_markup=inlines)
                elif call.data in file_1:
                    file_1.remove(call.data)
                    with open("file.txt", "w") as file_2:
                        file_2.write("".join(file_1).strip())
                    max_diary.send_message(call.message.chat.id, "Выбранные данные удалены")
            else:
                max_diary.send_message(call.message.chat.id,
                                       "Время авторицации вышло, пожалуйста авторезируйтесь снова",
                                       reply_markup=keyboard_start)


def file_w(message):
    with open("file.txt", "a+") as file_file:
        file_file.write(f"{message.text} {date}\n")
    max_diary.send_message(message.chat.id, "Задача добавлена")


def authorization(message):
    with open("reg.txt", "r") as file_log:
        login = file_log.read()
    if message.text.split(' ')[0] in login:
        print("L")
        max_diary.send_message(message.chat.id, "Авторизация успешна", reply_markup=keyboard_inlines)
    else:
        max_diary.send_message(message.chat.id, "Не верный логин")


def registration(message):
    name = message.text
    date_in = time.time()
    with open("reg.txt", "w") as f:
        f.write(f"{name} {date_in} \n")
    max_diary.send_message(message.chat.id, "Логин сохранен")


max_diary.polling(none_stop=True, interval=0)
