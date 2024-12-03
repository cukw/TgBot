import os
import logging
from aiogram import Bot,Dispatcher,types
import asyncio
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.storage.memory import MemoryStorage

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')

if(os.path.exists(dotenv_path)):
    load_dotenv(dotenv_path)
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher(storage=MemoryStorage())

class SendMessageState(StatesGroup):
    wait_recipient = State()
    wait_message = State()
 
@dp.message(Command("start"))
async def handle_message(message: Message):
    print(f"user {message.from_user.username} activated bot")
    await message.answer("Привет, я твой личный почтовый ящик, буду принимать все анонимные сообщения, что тебе придут")

@dp.message(Command("help"))
async def handle_message_help(message: Message):
    await message.answer("Вот все команды.\n/start - начало работ\n/send - отправить сообщение пользователю")

@dp.message(Command("send"))
async def send_message(message: Message,state: FSMContext):
    await message.answer("Введите ник пользователя с добавление @")
    await state.set_state(SendMessageState.wait_recipient)

@dp.message(SendMessageState.wait_recipient)
async def get_recipient(message: Message, state: FSMContext):
    recipient = message.text.strip()
    if not recipient.startswith("@"):
        await message.answer("Ник пользователя должен начинаться с @")
        return
    await state.update_data(recipient=recipient)
    await message.answer(f"Введите сообщение, которое хотите отправить пользователю {recipient}")
    await state.set_state(SendMessageState.wait_message)

@dp.message(SendMessageState.wait_message)
async def get_message_to_user(message: Message, state: FSMContext):
    user_data = await state.get_data()
    recipient = user_data.get("recipient")
    message = message.text.strip()
    try:
        await bot.send_message(chat_id=recipient,text=message)
        await message.answer("Сообщение успешно доставлено")
        print(f"user {message.from_user.username} send message to {recipient}")
    except Exception as ex:
        await message.answer("Произошла ошибка, попробуйте снова")
        print(f"Error {ex}")
    finally:
        state.clear()


async def main():
    try:
        print("Bot activated")
        await dp.start_polling(bot)
    except Exception as ex:
        print(f"Error {ex}")

if __name__ =='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shutdown")