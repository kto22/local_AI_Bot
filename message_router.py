from aiogram import Router #тут импортируем aiogram
from aiogram.types import Message
import data #тут импортируем файлик с функциями для работы с БД
import openai #тут импортим openai api


router = Router()


@router.message()
async def any_message(message: Message, client: openai.Client, client2):    #тут функция для обработки сообщений от пользователя

    table_name = 'u'+str(message.from_user.id)


    if message.text == '#delete_history':   #тут при получении команды #delete_history вызывается функция очистки переписки из БД
        await data.delete_history(table_name)
        return 0

    if message.text == '#compress_history':     #тут при получении команды #compress_history вызывается функция сжатия переписки из БД
        await data.compress_history(table_name, client=client2)
        return 0


    await data.insert_history(table_name, 'user', str(message.text))
    history = await data.get_history(table_name)    #тут формируем список из истории переписки из БД

    completion = client.chat.completions.create(   #тут делаем запрос и получаем ответ от нейронки
        model="local-model",
        messages=history,   #тут передаём переписку
        temperature=0.7,
    )
    print(completion)
    content = completion.choices[0].message.content

    await data.insert_history(table_name, 'assistant', str(content))   #тут добавляем новое сообщение в базу данных

    await message.answer(content)   #тут отправляем ответ пользователю