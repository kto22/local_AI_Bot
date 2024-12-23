from aiogram import Router
from aiogram.types import Message
import data
import openai


router = Router()


@router.message()
async def any_message(message: Message, client: openai.Client, client2):

    table_name = 'u'+str(message.from_user.id)

    history = await data.get_history(table_name)

    if message.text == '#delete_history':
        await data.delete_history(table_name)
        return 0

    if message.text == '#compress_history':
        await data.compress_history(table_name, client=client2)
        return 0

    await data.insert_history(table_name, 'user', str(message.text))

    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.7,
    )
    print(completion)
    content = completion.choices[0].message.content

    await data.insert_history(table_name, 'assistant', str(content))

    await message.answer(content)