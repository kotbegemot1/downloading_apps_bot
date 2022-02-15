import json
import os
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hlink, hitalic, hide_link
from get_page_of_app import get_page_of_app_2
from get_url_selenium import get_url_by_selenium

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("bot_token"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(f"Здравстуйте {message.chat.first_name}! Этот бот поможет вам скачать актуальные версии  android приложений")
    
@dp.message_handler(content_types=["text"])
async def do_something(message: types.Message):
    await message.answer(f"Загружаются результаты по запросу '{message.text}'. Ожидайте... ")

    data = get_page_of_app_2(message.text)
    with open(f"JSONs/{message.text}-data.json") as file:
        data = json.load(file)
    for item in data:
        card = f"{hide_link(item.get('app_icon'))}\n" \
            f"{hitalic(item.get('app_name'))} \n" \
            f"{hbold('Категория: ')} {item.get('app_category')}\n" \
            f"{hbold('Автор: ')} {item.get('app_author')}\n" \
            f"{hlink('Скачать', get_url_by_selenium(item.get('app_link')))}\n"
        await message.answer(card)

def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()