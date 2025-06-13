import logging
import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def welcome(message: types.Message):
    await message.reply("Привет! Я GPT-бот с поддержкой изображений (в будущем) и текста. Напиши что-то!")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def photo_handler(message: types.Message):
    await message.reply("Фото получено! Пока GPT не умеет его читать напрямую, но скоро добавим.")

@dp.message_handler()
async def handle_text(message: types.Message):
    user_input = message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Ошибка: {e}"
    await message.reply(reply)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
