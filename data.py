import sqlite3


connection = sqlite3.connect('database.db')
cursor = connection.cursor()
connection2 = sqlite3.connect('database.db')
print("connected to database successfully")
cursor2 = connection2.cursor()


async def insert_history(table_name, role, content):
    cursor.execute(f'INSERT INTO {table_name} (role, content) VALUES (?,?)', (role, content))
    connection.commit()
    print('history inserted successfully')


async def get_history(table_name):
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
    print('history fetched successfully')
    return history


async def delete_history(table_name):
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    connection.commit()
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
            role TEXT,
            content TEXT
            )
            ''')
    connection.commit()
    await insert_history(table_name, "system", "You are Konata Izumi from Lucky Star 2007.")
    print('history deleted successfully')


async def compress_history(table_name, client):
    cursor2.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
            role TEXT,
            content TEXT
            )
            ''')
    connection2.commit()
    cursor2.execute(f'SELECT * FROM {table_name}')
    result = cursor2.fetchall()

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
            cursor2.execute(f'UPDATE {table_name} SET content = ? WHERE content = ?', (new_line, str(row[1])))
            connection2.commit()
