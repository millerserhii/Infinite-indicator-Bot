import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
import markups as nav
from alert import generate_msg
import os


API_TOKEN = os.environ['BOT_API']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply("Hi!\nI'm Crypto Indicator Bot!\nSend me ticker and timeframe \n Example: \n BTC/USDT 15m",
                        reply_markup=nav.main_menu)


@dp.message_handler()
async def send_data(message: types.Message):
    global pair
    if message.text == '📈 Get indicators data':
        await message.answer('Choose pair:', reply_markup=nav.ind_menu)
    elif message.text == 'ℹ️️ Info':
        await message.answer('*Crypto Bot made by Gushbee©*\n'
                             'If you have any questions or propositions - contact _@smillex_',
                             reply_markup=nav.custom_menu, parse_mode="Markdown")
    elif message.text == '⬅️ Main menu':
        await message.answer('Main menu', reply_markup=nav.main_menu)
    elif message.text == 'BTC/USDT':
        pair = 'BTC/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'ETH/USDT':
        pair = 'ETH/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'BNB/USDT':
        pair = 'BNB/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'ADA/USDT':
        pair = 'ADA/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'XRP/USDT':
        pair = 'XRP/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'DOGE/USDT':
        pair = 'DOGE/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'DOT/USDT':
        pair = 'DOT/USDT'
        await message.answer('Choose timeframe:', reply_markup=nav.tf_menu)
    elif message.text == 'Custom pair':
        await message.answer('*Print pair with* _slash (/)_ *and timeframe*\n\n*Example*:\n_LINK/USDT 15m_\n\n'
                             '*Available all pairs from Binance*\n\n'
                             '*Timeframes* - _1m, 5m, 15m, 30m, 1h, 4h, 1d_', parse_mode="Markdown")

    elif message.text == '1m':
        msg = await generate_msg(pair, '1m')
        chat_id = message.from_user.id
        await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
    elif message.text == '5m':
        msg = await generate_msg(pair, '5m')
        chat_id = message.from_user.id
        await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
    elif message.text == '15m':
        msg = await generate_msg(pair, '15m')
        chat_id = message.from_user.id
        await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
    elif message.text == '1h':
        msg = await generate_msg(pair, '1h')
        chat_id = message.from_user.id
        await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
    elif message.text == '4h':
        msg = await generate_msg(pair, '4h')
        chat_id = message.from_user.id
        await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
    elif message.text == '1d':
        msg = await generate_msg(pair, '1d')
        chat_id = message.from_user.id
        await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
    else:
        try:
            pair = message.text.split()[0].upper()
            tf = message.text.split()[1]
            msg = await generate_msg(pair, tf)
            chat_id = message.from_user.id
            await bot.send_photo(chat_id, InputFile('images/img.png'), caption=msg, reply_markup=nav.ind_menu, parse_mode="Markdown")
        except:
            await message.answer('Pair not recognized', reply_markup=nav.ind_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
