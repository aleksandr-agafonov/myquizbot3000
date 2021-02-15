from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import Questions_States
import random

token = '1195846837:AAEt-7JhiX0XM7VgEDHavtycxyJCTPjJCZM'

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())
error_replies_list = ['ты дурачек, только циферки',
                      'ну ты ваще непрошибаемый...',
                      'Ты знаешь что такое \'циферки\', дурачек?',
                      'Славка - глупышка']

count = 0

# задаем первый вопрос
@dp.message_handler(commands=['start'])
async def question_one(message: types.Message):
    start_quiz_message = 'Привет! Давай пройдем тест!\nПервый вопрос: сколько будет 2 + 2 ?'
    start_quiz = await message.answer(start_quiz_message)
    await Questions_States.q1.set()


# получаем ответ на вопрос один и задаем вопрос два
@dp.message_handler(state=Questions_States.q1)
async def quests_two(message: types.Message, state:FSMContext):
    global count
    q1_answer = message.text
    try:
        if int(q1_answer) == 4:
            count += 1
            await bot.send_message(message.from_user.id, 'Ответ верный!\nВы получаете 1 бал!')
            await Questions_States.q2.set()
            await bot.send_message(message.from_user.id, 'Сколько будет 10 + 1 ?')
            return count
        elif int(q1_answer) != 4:
            await bot.send_message(message.from_user.id, 'Ответ неверный!')
            await Questions_States.q2.set()
            await bot.send_message(message.from_user.id, 'Сколько будет 10 + 1 ?')
            return count
    except ValueError:
        await bot.send_message(message.from_user.id, random.choice(error_replies_list))



# получаем ответ на вопрос два и задаем вопрос три
@dp.message_handler(state=Questions_States.q2)
async def question_three(message: types.Message, state:FSMContext):
    global count
    q2_answer = message.text
    try:
        if int(q2_answer) == 11:
            count += 1
            await bot.send_message(message.from_user.id, 'Ответ верный!\nВы получаете 1 бал!')
            await Questions_States.q3.set()
            await bot.send_message(message.from_user.id, 'Сколько будет 9 + 12 ?')
            return count
        elif int(q2_answer) != 11:
            await bot.send_message(message.from_user.id, 'Ответ неверный!')
            await Questions_States.q3.set()
            await bot.send_message(message.from_user.id, 'Сколько будет 9 + 12 ?')
            return count

    except ValueError:
        await bot.send_message(message.from_user.id, random.choice(error_replies_list))


# получаем ответ на вопрос три и выдаем результат
@dp.message_handler(state=Questions_States.q3)
async def final(message: types.Message, state:FSMContext):
    global count
    q3_answer = message.text
    try:
        if int(q3_answer) == 21:
            count += 1
            await bot.send_message(message.from_user.id, 'Ответ верный!\nВы получаете 1 бал!')
            await bot.send_message(message.from_user.id, f'Вы закончили тест!\nВаш счет: {count}'.format())
            await bot.send_message(message.from_user.id, 'Введите /start что бы снова начать тест')
            await state.reset_state()
            count = 0
        elif int(q3_answer) != 21:
            await bot.send_message(message.from_user.id, 'Ответ неверный!')
            await bot.send_message(message.from_user.id, f'Вы закончили тест!\nВаш счет: {count}'.format())
            await bot.send_message(message.from_user.id, 'Введите /start что бы снова начать тест')
            await state.reset_state()
            count = 0

    except ValueError:
        await bot.send_message(message.from_user.id, random.choice(error_replies_list))

# еее работает!
executor.start_polling(dp)