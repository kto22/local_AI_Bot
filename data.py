import sqlite3   #тут импортируем библиотеку для работы с БД


connection = sqlite3.connect('database.db')   #тут подключаемся к БД
cursor = connection.cursor()
print("connected to database successfully")


async def insert_history(table_name, role, content):   #тут функция для добавления сообщений в БД
    cursor.execute(f'INSERT INTO {table_name} (role, content) VALUES (?,?)', (role, content))
    connection.commit()
    print('history inserted successfully')


async def get_history(table_name):   #тут функция для получения списка истории переписки из БД
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
        role TEXT,
        content TEXT
        )
        ''')
    connection.commit()
    cursor.execute(f'SELECT * FROM {table_name}')
    result = cursor.fetchall()
    history = [
        {
            "role": "system",
            "content": "You are Konata Izumi from Lucky Star 2007."
        }
    ]
    for item in result:
        history.append({"role": str(item[0]), "content": str(item[1])})
    print(history)
    print('history fetched successfully')
    return history


async def delete_history(table_name):              #тут функция для удаления переписки
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    connection.commit()
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
            role TEXT,
            content TEXT
            )
            ''')
    connection.commit()
    print('history deleted successfully')


async def compress_history(table_name, client):            #тут функция для сжатия ответов нейросети с помощью другой нейросети
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
            role TEXT,
            content TEXT
            )
            ''')
    connection.commit()
    cursor.execute(f'SELECT * FROM {table_name}')
    result = cursor.fetchall()

    for i in range(1, len(result), 1):
        row = result[i]
        if str(row[0]) == 'assistant':
            prompt = [
                {
                    "role": "system",
                    "content": "You have to shorten the text you receive from user."
                },
                {
                    "role": "user",
                    "content": str(row[1]).replace('"', '').replace("'", "")
                }
            ]
            completion2 = client.chat.completions.create(
                model="local-model",
                messages=prompt,
                temperature=0.7,
            )
            new_line = completion2.choices[0].message.content.replace('"', '').replace("'", "")
            print(new_line)
            cursor.execute(f'UPDATE {table_name} SET content = ? WHERE content = ?', (new_line, str(row[1])))
            connection.commit()
