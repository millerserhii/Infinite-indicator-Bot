from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btn_main = KeyboardButton('⬅️ Main menu')

# --- Main Menu ---
btn_get_ind = KeyboardButton('📈 Get indicators data')
btn_info = KeyboardButton('ℹ️️ Info')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_get_ind, btn_info)


# --- Indicator Menu ---
btn_btc = KeyboardButton('BTC/USDT')
btn_eth = KeyboardButton('ETH/USDT')
btn_bnb = KeyboardButton('BNB/USDT')
btn_ada = KeyboardButton('ADA/USDT')
btn_xrp = KeyboardButton('XRP/USDT')
btn_doge = KeyboardButton('DOGE/USDT')
btn_dot = KeyboardButton('DOT/USDT')
btn_custom = KeyboardButton('Custom pair')
ind_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_btc, btn_eth, btn_bnb, btn_ada, btn_xrp,
                                                         btn_doge, btn_dot, btn_custom, btn_main)

# -----Timeframe Menu-------
btn_1m = KeyboardButton('1m')
btn_5m = KeyboardButton('5m')
btn_15m = KeyboardButton('15m')
btn_1h = KeyboardButton('1h')
btn_4h = KeyboardButton('4h')
btn_1d = KeyboardButton('1d')
tf_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_1m, btn_5m, btn_15m, btn_1h, btn_4h, btn_1d, btn_main)

# -----Custom Pair Menu-------
custom_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_main)
