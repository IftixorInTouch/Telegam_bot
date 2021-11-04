from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from data import dp, bot, db
from re import compile


@dp.message_handler(CommandStart(deep_link=compile(r"\d\d\d\d\d\d\d\d\d")))
async def with_deeplink(message: Message):
    deep_link_args = int(message.get_args())
    username = await db.select_user(message.get_args())
    referer = username[0][1]
    if deep_link_args == message.from_user.id:
        await message.answer("<b>Приводить самого себя нельзя!</b>")
    else:
        if not await db.select_user(message.from_user.id):
            await db.add_parent(
                username=message.from_user.username,
                user_id=message.from_user.id,
                parent_name=referer,
                parent_id=deep_link_args,
                referals=1,
                bonus=1
            )
            if not await db.select_referer(parent_id=deep_link_args):
                user = await db.select_referer(deep_link_args)
                print(user)
                print(deep_link_args)
                await db.add_referer(parent_id=deep_link_args)
                print("were added")
            await db.add_bonus(parent_id=deep_link_args)
            await message.answer(f"<b>Вас привел <a href='https://t.me/{referer}'>{referer}</a></b>")
            await message.answer("<b>Ты был занесен в базу</b>")
        else:
            await message.answer("<b>you are already in base</b>")


@dp.message_handler(CommandStart(deep_link=None))
async def refferal_system(message: Message):
    botname = await bot.get_me()
    name = botname.username
    user_id = message.from_user.id
    refferal_link = f"https://t.me/{name}?start={user_id}"
    await message.answer(f"<b>Приветствую вас в магазине!\n"
                         f"Вот ваша реферальная ссылка\n{refferal_link}\n"
                         f"За каждого приведенного вами человека вам засчитываются баллы.</b>\n")
    if not await db.select_user(message.from_user.id):
        await db.add_user(username=message.from_user.username, user_id=user_id)
        await message.answer("<b>You were added into base</b>")
    else:
        await message.answer("<b>You are already in base</b>")
