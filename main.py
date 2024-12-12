from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import asyncio
import os

# Токен вашего бота
TOKEN = os.getenv("7726976750:AAFkjAckKE-kRTtOpdcFkn1BfLyWAfRWRmI")

# Инициализация бота и диспетчера
bot = Bot(token=7726976750:AAFkjAckKE-kRTtOpdcFkn1BfLyWAfRWRmI)
dp = Dispatcher()

# Глобальные переменные для квиза
current_question_index = 0
score = 0

# Функция для создания клавиатуры с вариантами ответов
def create_answer_keyboard(correct_answer, wrong_answers):
    buttons = [KeyboardButton(text=correct_answer)] + [KeyboardButton(text=ans) for ans in wrong_answers]
    return ReplyKeyboardMarkup(keyboard=[[btn] for btn in buttons], resize_keyboard=True)

# Хэндлер для команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global current_question_index, score
    current_question_index = 0
    score = 0
    await message.answer("Добро пожаловать в квиз 'Questigo'! Нажмите /quiz, чтобы начать.")

# Хэндлер для команды /quiz
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    global current_question_index
    if current_question_index >= len(df):
        await message.answer("Квиз завершен. Нажмите /start, чтобы начать заново.")
        return
    question = df.iloc[current_question_index]['question']
    correct_answer = df.iloc[current_question_index]['correct_answer']
    wrong_answers = df.iloc[current_question_index]['wrong_answers']
    keyboard = create_answer_keyboard(correct_answer, wrong_answers)
    await message.answer(question, reply_markup=keyboard)

# Хэндлер для ответов пользователя
@dp.message()
async def handle_answer(message: types.Message):
    global current_question_index, score
    user_answer = message.text
    correct_answer = df.iloc[current_question_index]['correct_answer']
    if user_answer == correct_answer:
        score += 1
        await message.answer(f"Правильно! Ваш счет: {score}")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {correct_answer}. Ваш счет: {score}")
    current_question_index += 1
    await cmd_quiz(message)

# Хэндлер для команды /stats
@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    global score
    await message.answer(f"Ваш текущий счет: {score}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
