from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery, LabeledPrice, PreCheckoutQuery, ShippingQuery

from data import dp, db, bot
from callback_datas import buy_callback
from loader import PROVIDER_TOKEN
from payment.item import POST_REGULAR_SHIPPING


@dp.inline_handler(text="")
async def show_items(query: InlineQuery):
    results = []
    users = await db.select_users()
    for user in users:
        results.append(
            InlineQueryResultArticle(
                id=str(user[0]),
                title=user[1],
                input_message_content=InputTextMessageContent(
                    message_text=user[1]
                ),
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Купить его?", callback_data=buy_callback.new(item_name=user[1],
                                                                                                price=user[2]))
                    ]
                ])
            )
        )
    await query.answer(results=results, cache_time=300)


@dp.callback_query_handler(buy_callback.filter())
async def sell(call: CallbackQuery, callback_data: dict):
    print(callback_data.get('item_name'))
    await call.answer(cache_time=1)
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=callback_data.get('item_name'),
        description="Очень хороший товар",
        payload="payload",
        provider_token=PROVIDER_TOKEN,
        currency="UZS",
        prices=[
            LabeledPrice(label=callback_data.get('item_name'),
                         amount=callback_data.get("price"))
        ],
        start_parameter="buy",
        is_flexible=True
    )


@dp.shipping_query_handler()
async def shipping_method(query: ShippingQuery):
    await bot.answer_shipping_query(shipping_query_id=query.id,
                                    shipping_options=[POST_REGULAR_SHIPPING],
                                    ok=True)


@dp.pre_checkout_query_handler()
async def check_out(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=query.id,
        ok=True,
    )
    await bot.send_message(query.from_user.id, "Success!")
