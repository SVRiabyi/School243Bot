import MySQLdb
from datetime import datetime
import auth_data

# В даному файлі зібрані функції, що формують запити до БД і повертають сформований результат


def sql_present():  # Функція для запиту розкладу занять на поточний день

    # Приєднуємось до бази даних
    con = MySQLdb.connect(auth_data.sql_server, auth_data.sql_user, auth_data.sql_pass, auth_data.sql_dbname)
    cursor = con.cursor()
    # Задаємо змінні для роботи з днями тижня і поточними часовими даними
    day = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    now = datetime.now()
    present_day = datetime.weekday(now)
    # Виконуємо запит до БД записуємо результат в змінну rows
    query1 = f'''SELECT lesson_number, time_start, time_stop, subject
            FROM schedule
            WHERE weekday="{day[present_day]}"
            ORDER BY lesson_number ASC;'''
    cursor.execute(query1)
    rows = cursor.fetchall()

    # Задаємо порожню строку, в яку будемо записувати відповідь
    message = ''
    # Виключаємо ймовірність того, що сьогодні вихідний день
    if present_day == 5 or present_day == 6:
        message = message + "Сьогодні вихідний день. Уроків немає"
    #     Якщо умова вихідного дня не виконалась, то формуємо відповідь
    else:
        for row in rows:
            message = f'''{message}
{row[0]}. <b>{row[3]}</b> <i>({row[1]}-{row[2]})</i>'''

    # break the connection
    con.close()

    return message


def sql_workday(workday):  # Функція для запиту розкладу занять на будь-який робочий день. Назву задасть юзер.

    # Приєднуємось до бази даних
    con = MySQLdb.connect(auth_data.sql_server, auth_data.sql_user, auth_data.sql_pass, auth_data.sql_dbname)
    cursor = con.cursor()
    # Створюємо кортеж для запитів дня тижня в БД - назви відповідають назвам в БД
    day = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    # В залежності від введеного юзером дня тижня присвоюємо змінній whatever_day порядковий номер, що буде відповідати
    # індексу кортежа day, елементи якого (дні тижня) використовуємо в запиті до БД нижче.
    if workday == 'Понеділок':
        whatever_day = 0
    elif workday == 'Вівторок':
        whatever_day = 1
    elif workday == 'Ceреда':
        whatever_day = 2
    elif workday == 'Четвер':
        whatever_day = 3
    elif workday == "П'ятниця":
        whatever_day = 4
    elif workday == "Субота":
        whatever_day = 5
    elif workday == "Неділя":
        whatever_day = 6

    # Виконуємо запит до БД
    query1 = f'''SELECT lesson_number, time_start, time_stop, subject
                FROM schedule
                WHERE weekday="{day[whatever_day]}"
                ORDER BY lesson_number ASC;'''
    cursor.execute(query1)
    # Отримали кортеж рядка БД, де кожен елемент теж є кортежем
    rows = cursor.fetchall()

    # Задаємо порожню строку, в яку будемо записувати відповідь
    message = ''
    # Виключаємо ймовірність того, що сьогодні вихідний день
    if whatever_day == 5 or whatever_day == 6:
        message += "Сьогодні вихідний день. Уроків немає"
    else:
        # Якщо умова вихідного дня не виконалась, то формуємо відповідь
        for row in rows:
            message = f'''{message}
{row[0]}. <b>{row[3]}</b> <i>({row[1]}-{row[2]})</i>'''
    # Отримали кортеж, елементами якого я строки, форматовані в HTML режимі
    # break the connection
    con.close()
    # Повертаємо кортеж зі списком уроків
    return message


def current_lesson():  # Функція, що тягне з БД інформацію щодо поточного уроку
    # приєднуємося до бази даних класу
    con = MySQLdb.connect(auth_data.sql_server, auth_data.sql_user, auth_data.sql_pass, auth_data.sql_dbname)
    cursor = con.cursor()

    # Задаємо змінні для звернення до дати або часу
    day = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    now = datetime.now()
    present_day = datetime.weekday(now)

    # Виконуємо запит до БД
    query2 = f'''SELECT lessons.subject, lessons.first_name, lessons.patronymic, lessons.last_name, 
    lessons.identificator, lessons.pass, lessons.url, lessons.notes
                FROM `schedule` 
                RIGHT JOIN lessons ON schedule.lessons_id=lessons.id 
                WHERE weekday='{day[present_day]}' AND time_start<=CURRENT_TIME AND time_stop>=CURRENT_TIME;'''
    cursor.execute(query2)
    # отримали кортеж, кожен елемент якого це строка з інформацією про урок
    rows = cursor.fetchall()

    # break the connection
    con.close()
    # Повертаємо кортеж з інформацією про урок
    return rows


def end_lesson():  # Запит для визначення часу закінчення уроку
    # приєднуємося до бази даних класу
    con = MySQLdb.connect(auth_data.sql_server, auth_data.sql_user, auth_data.sql_pass, auth_data.sql_dbname)
    cursor = con.cursor()

    # Задаємо змінні для звернення до дати або часу
    day = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    now = datetime.now()
    present_day = datetime.weekday(now)

    # Виконуємо запит до БД
    query3 = f'''SELECT MAX(time_stop) 
FROM `schedule` 
WHERE weekday = '{day[present_day]}' AND time_stop>CURRENT_TIME;'''

    cursor.execute(query3)
    # Отримуємо кортеж з одним елементом, який містить час закінчення останнього уроку поточного дня
    # Якщо уроки вже закінчились, то значення в кортежі буде NULL
    rows = cursor.fetchall()

    # break the connection
    con.close()
    # повертаємо кортеж зі значенням часу закінчення уроку або значення NULL
    return rows


def any_lesson(subject):  # Функція, що тягне інформацію про урок, назва якого заходить як змінна subject
    # приєднуємося до бази даних класу
    con = MySQLdb.connect(auth_data.sql_server, auth_data.sql_user, auth_data.sql_pass, auth_data.sql_dbname)
    cursor = con.cursor()

    # Виконуємо запит до БД
    query4 = f'''SELECT subject, first_name, patronymic, last_name, identificator, pass, url, notes 
                FROM lessons  
                WHERE subject='{subject}';'''
    cursor.execute(query4)
    # отримали кортеж, кожен елемент якого це строка з інформацією про урок
    rows = cursor.fetchall()

    # break the connection
    con.close()
    # Повертаємо кортеж з інформацією про урок
    return rows


def list_of_subjects():  # Функція, що тягне список уроків з БД
    # приєднуємося до бази даних класу
    con = MySQLdb.connect(auth_data.sql_server, auth_data.sql_user, auth_data.sql_pass, auth_data.sql_dbname)
    cursor = con.cursor()
    # задаємо запит на список предметів
    query5 = '''SELECT subject 
                FROM lessons;'''
    cursor.execute(query5)
    # Отримали кортеж, де елемент це теж кортеж, у якого кожен урок це елемент з індексом 0
    rows = cursor.fetchall()
    # Щоб створити список з назвами уроків, створимо спочатку порожній список
    list_rows = []
    # За допомогою перебору елементів кортежу rows витягнемо кортежі col. Елементи кортежу col з індексом 0 запишемо
    # в список list_row. Записуємо всі елементи в lowercase - це знадобиться для можливості вводу даних в різних
    # регістрах
    for col in rows:
        list_elem = col[0]
        list_rows.append(list_elem.lower())

    # break the connection
    con.close()
    # Повертаємо список уроків
    return list_rows
