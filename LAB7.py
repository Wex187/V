import telebot
from telebot import types
import datetime
import psycopg2
token = "6229680576:AAExkbhjAmv8vRiqvCJZomKr_l3BNeheZDg"
bot = telebot.TeleBot(token)

today_date = datetime.datetime.today()

conn = psycopg2.connect(database='raspisanie',
                        user='postgres',
                        password='12365477Suka',
                        host='localhost',
                        port='5432'
                        )
cursor = conn.cursor()

if int(datetime.datetime.utcnow().isocalendar()[1]) % 2 == 0:
    week = 0
else:
    week = 1


def week_day_func(day_number):
    if day_number == 0:
        return 'Понедельник'
    elif day_number == 1:
        return 'Вторник'
    elif day_number == 2:
        return 'Среда'
    elif day_number == 3:
        return 'Четверг'
    elif day_number == 4:
        return 'Пятница'
    elif day_number == 5:
        return 'Суббота'
    elif day_number == 6:
        return 'Воскресенье'


def day_schedule(day, week_parity):
    response = ""
    if week_parity:
        week_name = 'upper_week'
    else:
        week_name = 'lower_week'

    cursor.execute(f"SELECT {week_name}.room_numb, {week_name}.start_time, teachers.teacher_name, subjects.subject_name "
                   f"FROM {week_name} INNER JOIN subjects "
                   f"on {week_name}.subject = subjects.id_subject INNER JOIN teachers "
                   f"on teachers.teacher_subject = subjects.id_subject "
                   f"WHERE day = '{day}' "
                   f"ORDER BY {week_name}.start_time;")
    schedule = list(cursor.fetchall())

    for i in range(len(schedule)):
        response += f"\n{i+1}. {schedule[i][1]}"
        response += f"\n{schedule[i][3]}"
        if schedule[i][2]:
            response += f"\n{schedule[i][2]}"
        if schedule[i][0]:
            response += f"\n{schedule[i][0]}\n"
        else:
            response += "\n"

    return response



def week_schedule(week_parity):
    response = ""

    for i in range(6):
        week_day = week_day_func(i)
        response += f"{week_day}:{day_schedule(week_day, week_parity)}\n{'-'*66 if i != 5 else ''}\n"
    return response


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("/help")

    bot.send_message(message.chat.id, 'Привет! Это бот с расписанием занятий группы БВТ2203 МТУСИ\n\nЧтобы узнать '
                                      'больше информации нажмите /help', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Понедельник")
    btn2 = types.KeyboardButton("Вторник")
    btn3 = types.KeyboardButton("Среда")
    btn4 = types.KeyboardButton("Четверг")
    btn5 = types.KeyboardButton("Пятница")
    btn6 = types.KeyboardButton("Суббота")
    btn7 = types.KeyboardButton("Расписание на текущую неделю")
    btn8 = types.KeyboardButton("Расписание на следующую неделю")
    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)

    bot.send_message(message.chat.id, 'СПИСОК КОМАНД:'
                                      '\n/help - получить список команд бота'
                                      '\n/current_week - узнать чётность текущей недели'
                                      '\n/today - расписание на сегодня'
                                      '\n/tomorrow - расписание на завтра'
                                      '\n/week - расписание на эту неделю'
                                      '\n/nextweek - расписание на следующую неделю'
                                      '\n/mtuci - узнать больше информации на сайте университета',
                     reply_markup=keyboard)


@bot.message_handler(commands=['current_week'])
def current_week_response(message):
    if week:
        bot.send_message(message.chat.id, "Сейчас нечетная неделя.")
    else:
        bot.send_message(message.chat.id, "Сейчас четная неделя.")


@bot.message_handler(commands=['today'])
def today_response(message):
    week_day = week_day_func(today_date.weekday())
    bot.send_message(message.chat.id, f"{week_day}:{day_schedule(week_day, week)}")


@bot.message_handler(commands=['tomorrow'])
def tomorrow_response(message):
    week_day = week_day_func(today_date.weekday() + 1)
    if week_day == 'Воскресенье':
        bot.send_message(message.chat.id, 'Завтра выходной!')
    else:
        bot.send_message(message.chat.id, f"{week_day}:{day_schedule(week_day, week)}")


@bot.message_handler(commands=['week'])
def week_response(message):
    bot.send_message(message.chat.id, f"Расписание на эту неделю:\n{week_schedule(week)}")


@bot.message_handler(commands=['nextweek'])
def nextweek_response(message):
    bot.send_message(message.chat.id, f"Расписание на следующую неделю:\n{week_schedule(week+1)}")


@bot.message_handler(commands=['mtuci'])
def mtuci_response(message):
    bot.send_message(message.chat.id, "https://mtuci.ru/")


@bot.message_handler(content_types=['text'])
def text_response(message):
    if message.text == 'Понедельник':
        bot.send_message(message.chat.id, f"Понедельник:{day_schedule('Понедельник', week)}")
    elif message.text == 'Вторник':
        bot.send_message(message.chat.id, f"Вторник:{day_schedule('Вторник', week)}")
    elif message.text == 'Среда':
        bot.send_message(message.chat.id, f"Среда:{day_schedule('Среда', week)}")
    elif message.text == 'Четверг':
        bot.send_message(message.chat.id, f"Четверг:{day_schedule('Четверг', week)}")
    elif message.text == 'Пятница':
        bot.send_message(message.chat.id, f"Пятница:{day_schedule('Пятница', week)}")
    elif message.text == 'Суббота':
        bot.send_message(message.chat.id, f"Суббота:{day_schedule('Суббота', week)}")
    elif message.text == 'Расписание на текущую неделю':
        bot.send_message(message.chat.id, f"Расписание на эту неделю:\n{week_schedule(week)}")
    elif message.text == 'Расписание на следующую неделю':
        bot.send_message(message.chat.id, f"Расписание на следующую неделю:\n{week_schedule(week + 1)}")
    else:
        bot.send_message(message.chat.id, 'Упс, что мы пишем ?_?')


bot.polling(none_stop=True, interval=0)
