import telebot
from telebot import types
import datetime

token = "5941529305:AAGTgNW2NEM67Y8MYHYZM2Z4o_X8kcDWIMg"
max_diary = telebot.TeleBot(token)

keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(types.KeyboardButton("registration".title()),
                   types.KeyboardButton("authorization".title()))

keyboard_inlines = types.InlineKeyboardMarkup()
keyboard_inlines.add(types.InlineKeyboardButton(text="Добавить задачу", callback_data="add"),
                     types.InlineKeyboardButton(text="Просмотреть задачу", callback_data="see"))


@max_diary.message_handler(commands=["start"])
def start(message):
    max_diary.send_message(message.chat.id,
                           "hello, выбирете авторизация если вы зарегестрированы или регистрация если нет",
                           reply_markup=keyboard_start)


@max_diary.callback_query_handler(func=lambda call: call.data in ["add", "see"])
def firs(call):
    if call.data == "add":
        max_diary.register_next_step_handler(max_diary.send_message(call.message.chat.id, "Hi"), file_w)
    elif call.data == "see":
        max_diary.register_next_step_handler(max_diary.send_message(call.message.chat.id, "See"), file_r)


@max_diary.message_handler(content_types=["text"])
def get_bot(message):
    if message.text.lower() == "registration":
        max_diary.register_next_step_handler(max_diary.send_message(message.chat.id, "Введите логин"), registration)
    elif message.text.lower() == "authorization":
        max_diary.register_next_step_handler(
            max_diary.send_message(message.chat.id, "Введите логин"), authorization)


def authorization(message):
    global autho_user
    autho_user = message.text
    max_diary.register_next_step_handler(
        max_diary.send_message(message.chat.id, "Авторизация успешна", reply_markup=keyboard_inlines),
        authorization_text)


def authorization_text(message):
    with open("reg.txt", "r") as file_log:
        login = file_log.readlines()
    if message.text in login:
        max_diary.send_message(message.chat.id, "Авторизация успешна")
    if message.text not in login:
        max_diary.send_message(message.chat.id, "Не верный логин")


def registration(message):
    with open("reg.txt", "a") as f:
        f.write(message.text + "\n")
    max_diary.send_message(message.chat.id, "Логин сохранен")


def file_w(message):
    with open("file.txt", "a") as file_file:
        file_file.write("* " + message.text + '\n')
    max_diary.send_message(message.chat.id, "Задача добавлена")


def file_r(message):
    with open("file.txt", "r", encoding="utf-8") as file:
        send = file.read()
    max_diary.send_message(message.chat.id, send)


max_diary.polling(none_stop=True, interval=0)
