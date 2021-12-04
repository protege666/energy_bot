import sqlite3

"""conn = sqlite3.connect("database.db")


def connect():
    cursor = conn.cursor()
    return cursor




def add(name, surname, patronymic, post, module1=0, module2=0, module3=0):
    list = [(f'{name}', f'{surname}', f'{patronymic}', f'{post}', f'{module1}', f'{module2}', f'{module3}')]
    connect().executemany("INSERT INTO user VALUES (?,?,?,?,?,?,?)", list)
    conn.commit()"""

def sql(telegram_id, surname, name, patronymic, post, module1=0, module2=0, module3=0, module4=0, module5=0, module6=0, module7=0):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE users
                             (telegram_id text ,surname text, name text, patronymic text,
                              post text, module1 int, module2 int, module3 int, module4 int, module5 int, module6 int, module7 int)
                          """)
    except:
        print("таблица уже создана!")

    list = [(f'{telegram_id}', f'{surname}', f'{name}', f'{patronymic}', f'{post}', f'{module1}', f'{module2}', f'{module3}', f'{module4}', f'{module5}', f'{module6}', f'{module7}')]
    cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", list)
    conn.commit()


def sqlcheck():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    print(cursor.fetchall())