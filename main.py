import telebot
from datetime import datetime
from telebot import types
import emoji
from sql8b import sql_present, sql_workday, list_of_subjects
from sql8b import current_lesson, end_lesson, any_lesson
from auth_data import token

# Записуємо в змінні назви днів тижня, поточний день тижня та час.
day = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
day_ukr = ('Понеділок', 'Вівторок', 'Середу', 'Четвер', "П'ятницю", 'Суботу', 'Неділю')
now = datetime.now()
present_day = datetime.weekday(now)
present_date = datetime.date(now)
present_time = datetime.time(now).strftime('%H:%M')

# Отримуємо токен бота
bot = telebot.TeleBot(token)


# Опрацьовуємо команду /start
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'''{emoji.emojize('	:waving_hand:', language="en")} Привіт, <b>{message.from_user.first_name}\n
{message.from_user.last_name}</b>,
Я шкільний бот 8Б класу, ЗЗСО №243, що в м. Києві.
Я твій помічник, і знаю розклад уроків на кожен день та 
володію додатковою інформацією про кожен урок. 
Для отримання необхідної інформації скористайся кнопками знизу екрану.
Ви завжди можете ввести коману <b>Зараз</b>, щоб отримати інформацію щодо поточного уроку.
Для продовження, натисніть кнопку "Продовжити" знизу екрану'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('Продовжити'))
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url='http://google.com'))
    bot.send_message(message.chat.id, 'В йо Гуглити!', reply_markup=markup)


# Опрацьовуємо текстові повідомлення від користувача
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    # Пропонуємо користувачеві два варіанта розкладу: на сьогодні або інший день тижня
    if message.text == 'Продовжити':
        lessons_button = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        today = types.KeyboardButton(text='Розклад на сьогодні')
        enyday = types.KeyboardButton(text='Розклад іншого дня')
        lessons_button.add(today, enyday)
        bot.send_message(message.chat.id, text="Оберіть розклад уроків, який Вас цікавить", reply_markup=lessons_button)

    # Якщо користувач хоче дізнатися розклад на сьогодні
    elif message.text == 'Розклад на сьогодні':
        mess = f'''Сьогодні розклад на {day_ukr[present_day]}:
{sql_present()}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    # Якщо користувач хоче дізнатися розклад іншого дня
    elif message.text == 'Розклад іншого дня':
        lessons_button = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
        monday = types.KeyboardButton(text='Понеділок')
        tuesday = types.KeyboardButton(text='Вівторок')
        wednesday = types.KeyboardButton(text='Ceреда')
        thursday = types.KeyboardButton(text='Четвер')
        friday = types.KeyboardButton(text="П'ятниця")
        lessons_button.add(monday, tuesday, wednesday, thursday, friday)
        bot.send_message(message.chat.id, text="Оберіть день, який Вас цікавить", reply_markup=lessons_button)

    elif message.text == 'Понеділок':
        mess = f'''Розклад на {day_ukr[0]}:
{sql_workday('Понеділок')}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == 'Вівторок':
        mess = f'''Розклад на {day_ukr[1]}:
{sql_workday('Вівторок')}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == 'Ceреда':
        mess = f'''Розклад на {day_ukr[2]}:
{sql_workday('Ceреда')}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == 'Четвер':
        mess = f'''Розклад на {day_ukr[3]}:
{sql_workday('Четвер')}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == "П'ятниця":
        mess = f'''Розклад на {day_ukr[4]}:
{sql_workday("П'ятниця")}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == "Субота":
        mess = f'''Розклад на {day_ukr[5]}:
{sql_workday("Субота")}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == "Неділя":
        mess = f'''Розклад на {day_ukr[6]}:
{sql_workday("Неділя")}

Деталі - наберіть назву предмета в чат'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    elif message.text == "Зараз" or message.text == 'зараз':

        # Зробимо з отриманого на запит до БД кортежу список
        # це необхідно, щоб можна було змінювати значення типу NONE
        rows = list(current_lesson())
        end_lessons = list(end_lesson())

        # Запишемо отриманий список в строку, для виявлення пустого кортежу на запит до БД
        # це знадобиться для виявлення перерви між уроками
        check_mess = ''
        for i in range(len(rows)):
            check_mess += f'{rows[i]}'

        # Цей кортеж має повертати значення None, для визначення закінчення навчального дня
        check_mess1 = end_lessons[0]

        # перевірка, чи сьогодні вихідний день
        if present_day == 5 or present_day == 6:
            mess = f'Cьогодні вихідний день, уроків немає!'

        # Перевіряємо чи закінчились уроки в школі сьогодні
        elif check_mess1[0] is None:
            mess = f'Станом на сьогодні більше уроків немає!'

        # Якщо кортеж на запит був порожній, то повідомляємо, що зараз перерва
        elif check_mess == '':
            mess = f'Зараз в школі перерва!'

        # Видаємо інформацію про поточний урок
        elif check_mess != '':
            # Спочатку визначимо чи не було значень типу NONE та замінюємо його на пусту строку
            for i in range(len(rows)):
                if rows[i] is None:
                    rows[i] = ''
            # Форматуємо отримані дані у приємну відповідь
            for row in rows:
                mess = f'''Поточний урок <b>{row[0]}</b>:
Вчитель(ка): <b>{row[1]} {row[2]} {row[3]}</b>
Ідентифікатор: <b>{row[4]}</b>
Пароль доступу: <b>{row[5]}</b>
Посилання на сайт: <u>{row[6]}</u>

Додаткова інформація: {row[7]}'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    # Видаємо інфу про будь-який предмет, якщо юзер ввів назву предмету. Регістр тексту будь-який.
    elif message.text.lower() in list_of_subjects():
        rows = list(any_lesson(message.text))

        for row in rows:
            mess = f'''Інформація щодо предмету <b>{row[0]}</b>:
Вчитель(ка): <b>{row[1]} {row[2]} {row[3]}</b>
Ідентифікатор: <b>{row[4]}</b>
Пароль доступу: <b>{row[5]}</b>
Посилання на сайт: <u>{row[6]}</u>


Додаткова інформація: {row[7]}'''
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)

    # Якщо введено команда не коректно введена або взагалі не команда
    else:
        mess = '''Дана команда мені не відома, але Ви можете спробувати наступні команди:
        <b>Зараз</b> - інформація щодо поточного уроку,
        <b>/website</b> - перенаправить вас на пошукову сторінку <u>Google</u> 
        або введіть назву предмету, інформація про який Вас цікавить, наприклад, <b>Алгебра</b> або 
        <b>Українська мова</b>.'''

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add(types.KeyboardButton('Продовжити'))
        bot.send_message(message.chat.id, text=mess, parse_mode='html', reply_markup=markup)


# Якщо вставлена фотка то бот прокоментує
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау, класна фотка!')


# Якщо вставлене відео то бот прокоментує
@bot.message_handler(content_types=['video'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Норм відос!')


bot.polling(none_stop=True)
