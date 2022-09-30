import json
import os
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink, hitalic, hide_link

from get_page_of_app import get_page_of_app
from get_url_selenium import get_url_by_selenium

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("bot_token"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(content_types=["text"])
async def do_something(message: types.Message):
    await message.answer(f"Загружаются результаты по запросу '{message.text}'. Ожидайте... ")

    try:
        data = get_page_of_app(message.text)
    except AttributeError:
        await message.answer(f"Некорректный запрос, попробуйте другой")

    with open(f"JSONs/{message.text}-data.json") as file:
        data = json.load(file)

    for item in data:
        card = f'<a href="{item.get("app_icon")}">&#8288;</a>\n' \
            f"{hitalic(item.get('app_name'))} \n" \
            f"{hbold('Категория: ')} {item.get('app_category')}\n" \
            f"{hbold('Автор: ')} {item.get('app_author')}\n" \
            f"{hlink('Скачать', get_url_by_selenium(item.get('app_link')))}\n"
        await message.answer(card)
        
def main():
    executor.start_polling(dp)

if __name__ == "__main__":
    main()