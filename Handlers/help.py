from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from data import bot, dp, db
from Keyboards.Inline_keyboard.help import help_keyboard


@dp.message_handler(Command("help"))
async def help(message: Message):
    await message.answer("<b>Здесь вы можете узнать вашу реферальную ссылку и ваши бонусы</b>",
                         reply_markup=help_keyboard)


@dp.callback_query_handler(text="referal_link")
async def send_link(call: CallbackQuery):
    await call.answer(cache_time=0)
    user_id = call.from_user.id
    bot_info = await bot.get_me()
    name = bot_info.username
    referal_link = f"https://t.me/{name}?start={user_id}"
    await call.message.answer(text=f"<b>Ваша реферальная ссылка:\n"
                                   f"{referal_link}</b>")


@dp.callback_query_handler(text="bonus")
async def show_bonus(call: CallbackQuery):
    await call.answer(cache_time=0)
    quantity = await db.select_bonus(call.from_user.id)
    await call.message.answer(text=f"<b>You have <i>{quantity}</i> bonuses</b>")
