from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

help_keyboard = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton("referal_link", callback_data="referal_link"),
                                             InlineKeyboardButton("bonuses", callback_data="bonus")
                                         ]
                                     ]
                                     )
