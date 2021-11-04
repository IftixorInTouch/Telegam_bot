from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data import dp, db


@dp.message_handler(Command("add"))
async def add_item(message: Message, state: FSMContext):
    await message.answer("Пришлите мне user_id")

    await state.set_state("user_id")


@dp.message_handler(state="user_id")
async def user_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        await state.update_data(user_id=user_id)
        await message.answer("Пришлите юзернаме")
    except ValueError:
        await message.answer("Должно быть число\nПроделайте все заново")
        await state.finish()
        return

    await state.set_state("username")


@dp.message_handler(state="username")
async def username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Thanks")
    data = await state.get_data()
    await db.add_user(data['username'], data['user_id'])
    await state.reset_data()
    await state.finish()


@dp.message_handler(Command('delete'))
async def delete_item(message: Message, state: FSMContext):
    users = await db.select_users()
    for user in users:
        user = dict(user)
        print(user)
        await message.answer(f"{user}")

    await message.answer("kogo udalyaem")
    await state.set_state("delete")


@dp.message_handler(state="delete")
async def delete(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        await db.drop_user(user_id)
        await message.answer("Deleted")
    except ValueError:
        await message.answer("Должно быть число\nПроделайте все заново")
        await state.finish()
        return
    await state.finish()
