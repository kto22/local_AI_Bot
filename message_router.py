from aiogram import F, Router, types
from aiogram.types import Message

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import data #тут импортируем файлик с функциями для работы с БД
from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

from data import get_model

router = Router()


@router.message(F.text == '/start')
async def start(message: Message):
    await message.answer("Hello my chumbud! I'm Kona-tyan..."
                         "\n"
                         "Here is list of available commands:\n"
                         "/model - model selection\n"
                         "/delete_history - delete your conversation history from database\n")


@router.message(F.text == '/model')
async def model_sel(message: Message):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Llama-3", callback_data="llama"),
            InlineKeyboardButton(text="Phi-4", callback_data="phi")
        ]
    ])

    await message.answer("Hello! Please choose your model:", reply_markup=inline_keyboard)


@router.callback_query(lambda c: c.data == "llama") # Register callback query handler within the router
async def button1_callback_handler(callback_query: types.CallbackQuery):
    await data.insert_model(callback_query.from_user.id, 'models/Llama-3.2-3B-Instruct-Q4_0.gguf')


@router.callback_query(lambda c: c.data == "phi") # Register callback query handler within the router
async def button2_callback_handler(callback_query: types.CallbackQuery):
    await data.insert_model(callback_query.from_user.id, 'models/matteogeniaccio.phi-4.Q2_K.gguf')


@router.message(F.text == '/delete_history')
async def del_hist(message: Message):
    table_name = 'u' + str(message.from_user.id)
    await data.delete_history(table_name)
    return 0


@router.message()
async def any_message(message: Message):    #тут функция для обработки сообщений от пользователя

    table_name = 'u'+str(message.from_user.id)

    await data.insert_history(table_name, 'user', str(message.text))
    history = await data.get_history(table_name)    #тут формируем список из истории переписки из БД

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    model = await get_model(message.from_user.id)
    llm = ChatLlamaCpp(
        model_path=model,
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,
    )

    msg = llm.invoke(history)
    content = msg.content

    await data.insert_history(table_name, 'assistant', str(content))   #тут добавляем новое сообщение в базу данных

    await message.answer(content)   #тут отправляем ответ пользователю