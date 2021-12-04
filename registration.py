import sqlite3

"""conn = sqlite3.connect("database.db")


def connect():
    cursor = conn.cursor()
    return cursor




def add(name, surname, patronymic, post, module1=0, module2=0, module3=0):
    list = [(f'{name}', f'{surname}', f'{patronymic}', f'{post}', f'{module1}', f'{module2}', f'{module3}')]
    connect().executemany("INSERT INTO user VALUES (?,?,?,?,?,?,?)", list)
    conn.commit()"""

def sql(name, surname, patronymic, post, module1=0, module2=0, module3=0):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE user
                             (name text, surname text, patronymic text,
                              post text, module1 int, module2 int, module3 int)
                          """)
    except:
        print("таблица уже создана!")

    list = [(f'{name}', f'{surname}', f'{patronymic}', f'{post}', f'{module1}', f'{module2}', f'{module3}')]
    cursor.executemany("INSERT INTO user VALUES (?,?,?,?,?,?,?)", list)
    conn.commit()


def sqlcheck():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    print(cursor.fetchall())