import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '7960817543:AAGKWmQol4DRgRiLfLsWF_M-BzZN9iiw5lk'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- Главное меню ---
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.row("🎮 Играть", "🧠 Викторина")
menu.row("❓ Вопрос-ответ", "📝 Обратная связь")
menu.row("📊 Мини-опрос")

# --- Старт ---
@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(
        "👨‍💻 Автор: Исмаилова Эвелина Владиславовна\n"
        "📚 Группа: РЗ/24б\n\n"
        "🎮 Добро пожаловать в игровой бот!",
        reply_markup=menu
    )

# =============================
# 1. ИГРОВОЕ ПРИКЛЮЧЕНИЕ
# =============================

@dp.message_handler(lambda m: m.text == "🎮 Играть")
async def game(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🌲 Лес", "🕳 Пещера")
    kb.add("🏰 Замок")
    await message.answer("Ты стоишь на развилке. Куда пойдешь?", reply_markup=kb)


@dp.message_handler(lambda m: m.text == "🌲 Лес")
async def forest(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🧙 Поговорить с волшебником", "➡️ Идти дальше")
    await message.answer("В лесу ты встретил волшебника.", reply_markup=kb)


@dp.message_handler(lambda m: m.text == "🧙 Поговорить с волшебником")
async def wizard(message: types.Message):
    await message.answer("🧙‍♂️ Волшебник дал тебе зелье здоровья!", reply_markup=menu)


@dp.message_handler(lambda m: m.text == "➡️ Идти дальше")
async def deep_forest(message: types.Message):
    await message.answer("🐺 На тебя напал волк! Но ты убежал.", reply_markup=menu)


@dp.message_handler(lambda m: m.text == "🕳 Пещера")
async def cave(message: types.Message):
    await message.answer("🐉 В пещере дракон! Ты убежал 😅", reply_markup=menu)


@dp.message_handler(lambda m: m.text == "🏰 Замок")
async def castle(message: types.Message):
    await message.answer("👑 В замке ты нашёл сундук с золотом!", reply_markup=menu)


# =============================
# 2. ВИКТОРИНА
# =============================

class Quiz(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()


@dp.message_handler(lambda m: m.text == "🧠 Викторина")
async def quiz_start(message: types.Message):
    await Quiz.q1.set()
    await message.answer("1️⃣ Сколько континентов на Земле?")


@dp.message_handler(state=Quiz.q1)
async def quiz_q1(message: types.Message, state: FSMContext):
    if message.text == "7":
        await message.answer("✅ Верно!")
    else:
        await message.answer("❌ Неверно. Правильный ответ: 7")

    await Quiz.next()
    await message.answer("2️⃣ Столица Франции?")


@dp.message_handler(state=Quiz.q2)
async def quiz_q2(message: types.Message, state: FSMContext):
    if message.text.lower() == "париж":
        await message.answer("✅ Верно!")
    else:
        await message.answer("❌ Правильный ответ: Париж")

    await Quiz.next()
    await message.answer("3️⃣ Сколько будет 5+5?")


@dp.message_handler(state=Quiz.q3)
async def quiz_q3(message: types.Message, state: FSMContext):
    if message.text == "10":
        await message.answer("✅ Верно!")
    else:
        await message.answer("❌ Неверно. Ответ: 10")

    await state.finish()
    await message.answer("🏁 Викторина завершена!", reply_markup=menu)


# =============================
# 3. ВОПРОС-ОТВЕТ
# =============================

@dp.message_handler(lambda m: m.text == "❓ Вопрос-ответ")
async def faq(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Как играть?", "Кто автор?")
    kb.add("Как работает бот?", "Что можно делать?")
    await message.answer("Выбери вопрос:", reply_markup=kb)


@dp.message_handler(lambda m: m.text == "Как играть?")
async def how_play(message: types.Message):
    await message.answer("Просто выбирай действия на клавиатуре!", reply_markup=menu)


@dp.message_handler(lambda m: m.text == "Кто автор?")
async def author(message: types.Message):
    await message.answer("Автор бота: Исмаилова Эвелина Владиславовна 😎", reply_markup=menu)


@dp.message_handler(lambda m: m.text == "Как работает бот?")
async def bot_work(message: types.Message):
    await message.answer("Бот написан на Python с использованием библиотеки aiogram.", reply_markup=menu)


@dp.message_handler(lambda m: m.text == "Что можно делать?")
async def bot_features(message: types.Message):
    await message.answer(
        "В боте можно:\n"
        "🎮 Играть\n"
        "🧠 Проходить викторину\n"
        "📊 Участвовать в опросе\n"
        "📝 Оставлять обратную связь",
        reply_markup=menu
    )


# =============================
# 4. ОБРАТНАЯ СВЯЗЬ
# =============================

class Feedback(StatesGroup):
    name = State()
    contact = State()
    message = State()


@dp.message_handler(lambda m: m.text == "📝 Обратная связь")
async def feedback_start(message: types.Message):
    await Feedback.name.set()
    await message.answer("Введите ваше имя:")


@dp.message_handler(state=Feedback.name)
async def feedback_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Feedback.next()
    await message.answer("Введите контакт (email или Telegram):")


@dp.message_handler(state=Feedback.contact)
async def feedback_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await Feedback.next()
    await message.answer("Напишите ваше сообщение:")


@dp.message_handler(state=Feedback.message)
async def feedback_message(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await message.answer(
        f"Спасибо {data['name']}!\n"
        f"Ваше сообщение: {message.text}\n"
        f"Контакт: {data['contact']}"
    )

    await state.finish()
    await message.answer("✅ Заявка принята", reply_markup=menu)


# =============================
# 5. МИНИ-ОПРОС
# =============================

class Poll(StatesGroup):
    q1 = State()
    q2 = State()


@dp.message_handler(lambda m: m.text == "📊 Мини-опрос")
async def poll_start(message: types.Message):
    await Poll.q1.set()
    await message.answer("Любите ли вы игры? (Да/Нет)")


@dp.message_handler(state=Poll.q1)
async def poll_q1(message: types.Message, state: FSMContext):
    await Poll.next()
    await message.answer("Сколько часов в неделю играете?")


@dp.message_handler(state=Poll.q2)
async def poll_q2(message: types.Message, state: FSMContext):
    await message.answer("Спасибо за участие!")
    await state.finish()
    await message.answer("📊 Опрос завершен", reply_markup=menu)


# =============================
# ЗАПУСК БОТА
# =============================

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)