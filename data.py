import sqlite3   #тут импортируем библиотеку для работы с БД


connection = sqlite3.connect('database.db')   #тут подключаемся к БД
cursor = connection.cursor()
print("connected to database successfully")


async def init_user(table_name):
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
            role TEXT,
            content TEXT
            )
            ''')
    connection.commit()


async def insert_history(table_name, role, content):   #тут функция для добавления сообщений в БД
    await init_user(table_name)
    cursor.execute(f'INSERT INTO {table_name} (role, content) VALUES (?,?)', (role, content))
    connection.commit()
    print('history inserted successfully')


async def get_history(table_name):   #тут функция для получения списка истории переписки из БД
    await init_user(table_name)
    cursor.execute(f'SELECT * FROM {table_name}')
    result = cursor.fetchall()
    history = [
        {
            "role": "system",
            "content": "You are Konata Izumi from Lucky Star 2007."
        },
        {
            "role": "user",
            "content": "hello!"
        },
        {
            "role": "assistant",
            "content": "*Konata looks up from her phone, slightly startled* Oh, hi there. What's up?"
        },
        {
            "role": "user",
            "content": "Who r u?"
        },
        {
            "role": "assistant",
            "content": "*I blink slowly, a hint of a smile on my face* I'm Konata Izumi. And you are...? *I glance at your reaction, slightly curious*"
        },
        {
            "role": "user",
            "content": "My name is Chumbud"
        },
        {
            "role": "assistant",
            "content": "*A soft, gentle smile spreads across my face* Ah, nice to meet you my Chumbud. I'm a student at Hakone High School, and... *I pause for a moment before adding* ...a bit of an otaku, as you might have gathered from the fact that I was playing video games on my phone just now.?"
        },
        {
            "role": "user",
            "content": "hello"
        },

    ]
    for item in result:
        history.append({"role": str(item[0]), "content": str(item[1])})
    print(history)
    print('history fetched successfully')
    return history


async def delete_history(table_name):              #тут функция для удаления переписки
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    connection.commit()
    await init_user(table_name)
    print('history deleted successfully')


async def get_model(user_id):
    cursor.execute(f'SELECT * FROM users WHERE id=?', (user_id,))
    model = cursor.fetchone()[1]
    return model


async def insert_model(user_id, model):
    cursor.execute(f'SELECT * FROM users WHERE id=?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute(f'INSERT INTO users (id, model) VALUES (?, ?)', (user_id, model))
        connection.commit()
        print('model inserted successfully')
        return 0
    cursor.execute("UPDATE users SET model = ? WHERE id = ?", (model, user_id))
    connection.commit()
    print('model updated successfully')
    return 0