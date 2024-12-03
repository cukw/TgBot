import os
import logging
from aiogram import Bot,Dispatcher
import asyncio
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'.env')

if(os.path.exists(dotenv_path)):
    load_dotenv(dotenv_path)
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

async def main():   
    try:
        logging.info("Bot activated")
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"Error {ex}")

if __name__ =='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bpt shutdown")