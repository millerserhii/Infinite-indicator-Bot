import asyncio
import ccxt.async_support as ccxt
import pandas_ta as ta
import pandas as pd
import PIL
from PIL import Image, ImageDraw, ImageFont


def get_chart(input):
    # percent = 90  # Percent for gauge
    output_file_name = 'images/new_gauge.png'
    x = 825
    y = 825
    loc = (x, y)
    percent = input / 100
    rotation = 180 * percent  # 180 degrees because the gauge is half a circle
    rotation = 90 - rotation  # Factor in the needle graphic pointing to 50 (90 degrees)
    dial = Image.open('images/arrow-2.png')
    dial = dial.rotate(rotation, resample=PIL.Image.BICUBIC, center=loc)  # Rotate needle
    gauge = Image.open('images/gauge_white.png')
    gauge.paste(dial, mask=dial)  # Paste needle onto gauge
    gauge.save(output_file_name)

    img = Image.open('images/new_gauge.png')
    font = ImageFont.truetype('images/Roboto.ttf', 80)

    imgDrawer = ImageDraw.Draw(img)
    if input < 25:
        text = "STRONG DOWN"
        imgDrawer.text((550, 300), text, (0, 0, 0), font=font)
    elif 25 <= input < 45:
        text = 'WEAK DOWN'
        imgDrawer.text((600, 300), text, (0, 0, 0), font=font)
    elif 55 < input <= 75:
        text = 'WEAK UP'
        imgDrawer.text((670, 300), text, (0, 0, 0), font=font)
    elif input > 75:
        text = 'STRONG UP'
        imgDrawer.text((620, 300), text, (0, 0, 0), font=font)
    else:
        text = 'NEUTRAL'
        imgDrawer.text((660, 300), text, (0, 0, 0), font=font)

    img.save(f'images/img.png')


def check_macd(df):
    macd = df.ta.macd()
    # print(macd.iloc[-1])

    # cross_zero = ta.cross_value(macd.iloc[-1]['MACD_12_26_9'], 0).iloc[-1]

    if macd.iloc[-1]['MACDh_12_26_9'] > macd.iloc[-3]['MACDh_12_26_9']:
        if macd.iloc[-1]['MACDh_12_26_9'] > 0:
            msg = "*MACD* - strong UP"
            score = 6.25
        elif macd.iloc[-1]['MACDh_12_26_9'] < 0:
            msg = "*MACD* - weak DOWN"
            score = -3.125
    elif macd.iloc[-1]['MACDh_12_26_9'] < macd.iloc[-3]['MACDh_12_26_9']:
        if macd.iloc[-1]['MACDh_12_26_9'] > 0:
            msg = "*MACD* - weak UP"
            score = 3.125
        elif macd.iloc[-1]['MACDh_12_26_9'] < 0:
            msg = "*MACD* - strong DOWN"
            score = -6.25
    return score, msg


def check_rsi(df):
    rsi = df.ta.rsi()
    rsi_last = rsi.iloc[-1]
    if rsi_last > 70:
        msg = "*RSI* - overbought"
        score = -6.25
    elif rsi_last < 30:
        msg = "*RSI* - oversold"
        score = 6.25
    else:
        if rsi_last > rsi.iloc[-3]:
            if rsi_last > 50:
                msg = "*RSI* - strong UP"
                score = 6.25
            elif rsi_last < 50:
                msg = "*RSI* - weak DOWN"
                score = -3.125
        elif rsi_last < rsi.iloc[-3]:
            if rsi_last > 50:
                msg = "*RSI* - weak UP"
                score = 3.125
            elif rsi_last < 50:
                msg = "*RSI* - strong DOWN"
                score = -6.25
    return score, msg


def check_squeeze(df):
    squeeze_pro = df.ta.squeeze_pro()
    if squeeze_pro.iloc[-1]['SQZPRO_20_2.0_20_2_1.5_1'] > squeeze_pro.iloc[-3]['SQZPRO_20_2.0_20_2_1.5_1']:
        if squeeze_pro.iloc[-1]['SQZPRO_20_2.0_20_2_1.5_1'] > 0:
            msg = "*Squeeze PRO* - strong UP"
            score = 6.25
        elif squeeze_pro.iloc[-1]['SQZPRO_20_2.0_20_2_1.5_1'] < 0:
            msg = "*Squeeze PRO* - weak DOWN"
            score = -3.125
    elif squeeze_pro.iloc[-1]['SQZPRO_20_2.0_20_2_1.5_1'] < squeeze_pro.iloc[-3]['SQZPRO_20_2.0_20_2_1.5_1']:
        if squeeze_pro.iloc[-1]['SQZPRO_20_2.0_20_2_1.5_1'] > 0:
            msg = "*Squeeze PRO* - weak UP"
            score = 3.125
        elif squeeze_pro.iloc[-1]['SQZPRO_20_2.0_20_2_1.5_1'] < 0:
            msg = "*Squeeze PRO* - strong DOWN"
            score = -6.25
    return score, msg


def check_supertrend(df):
    trend = df.ta.supertrend().iloc[-1]['SUPERTd_7_3.0']
    if trend == -1:
        msg = "*Supertrend* - Downtrend"
        score = -3.125
    elif trend == 1:
        msg = "*Supertrend* - Uptrend"
        score = 3.125
    return score, msg


def check_ichimoku(df):
    ichimoku = df.ta.ichimoku()
    current_price = df['close'].iloc[-1]
    last = ichimoku[0].iloc[-1]
    last_f = ichimoku[1].iloc[-1]
    chikou_span = ichimoku[0].iloc[-27]['ICS_26']
    price_chikou = df['close'].iloc[-27]
    up = 0
    down = 0

    # check Tenkan Sen and Kijun Sen
    if last['ITS_9'] > last['IKS_26']:
        up += 1
        if current_price > last['ITS_9']:
            up += 1
    elif last['ITS_9'] < last['IKS_26']:
        down += 1
        if current_price < last['ITS_9']:
            down += 1
    elif last['ITS_9'] == last['IKS_26']:
        if current_price < last['IKS_26']:
            down += 1
        elif current_price > last['IKS_26']:
            up += 1

    # Check Chikou Span
    if price_chikou < chikou_span:
        up += 1
    elif price_chikou > chikou_span:
        down += 1

    # Check SpanA and SpanB (cloud) current time
    if current_price > last['ISA_9'] and current_price > last['ISB_26']:
        up += 1
    elif current_price < last['ISA_9'] and current_price < last['ISB_26']:
        down += 1

    # Check cloud crossover in future
    if last_f['ISA_9'] > last_f['ISB_26']:
        up += 1
    elif last_f['ISA_9'] < last_f['ISB_26']:
        down += 1

    # Calculate result

    if up >= 4 and down <= 1:
        msg = f"*Ichimoku* - strong UP || UP = {up}, DOWN = {down}"
        score = 6.25
    elif down >= 4 and up <= 1:
        msg = f"*Ichimoku* - strong DOWN || UP = {up}, DOWN = {down}"
        score = -6.25
    elif up == 3 and down <= 2:
        msg = f"*Ichimoku* - weak UP || UP = {up}, DOWN = {down}"
        score = 3.125
    elif down == 3 and up <= 2:
        msg = f"*Ichimoku* - weak DOWN || UP = {up}, DOWN = {down}"
        score = -3.125
    else:
        msg = f"*Ichimoku* - neutral || UP = {up}, DOWN = {down}"
        score = 0
    return score, msg


def check_cmf(df):
    cmf = df.ta.cmf()
    cmf_last = df.ta.cmf().iloc[-1]
    crossover = ta.cross_value(cmf, 0).iloc[-1]

    if crossover == 1 and cmf_last > 0:
        msg = f"*CMF* - crossover UP - {cmf_last:.2f}"
        score = 6.25
    elif crossover == 1 and cmf_last < 0:
        msg = f"*CMF* - crossover DOWN - {cmf_last:.2f}"
        score = -6.25
    else:
        msg = f"*CMF* - neutral - {cmf_last:.2f}"
        score = 0
    return score, msg


def check_adx(df):
    adx = df.ta.adx().iloc[-1]["ADX_14"]
    dmp = df.ta.adx().iloc[-1]["DMP_14"]
    dmn = df.ta.adx().iloc[-1]["DMN_14"]

    if adx >= 25:
        if dmp > dmn:
            msg = f"*ADX* - strong uptrend ({adx:.2f})"
            score = 6.25
        if dmn > dmp:
            msg = f"*ADX* - strong downtrend ({adx:.2f})"
            score = -6.25
    elif adx < 25:
        msg = f"*ADX* - no trend ({adx:.2f})"
        score = 0
    return score, msg


def check_bbands(df):
    price = df['close']
    upper_line = df.ta.bbands(length=20)['BBU_20_2.0']
    middle_line = df.ta.bbands(length=20)['BBM_20_2.0']
    lower_line = df.ta.bbands(length=20)['BBL_20_2.0']


    crossover_middle = ta.cross(price, middle_line).iloc[-1]
    crossunder_middle = ta.cross(middle_line, price).iloc[-1]

    crossunder_high = ta.cross(upper_line, price).iloc[-1]
    crossoveer_low = ta.cross(price, lower_line).iloc[-1]

    if crossover_middle == 1:
        msg = '*Bollinger* - strong UP (cross UP middle line)'
        score = 6.25
    elif crossunder_middle == 1:
        msg = '*Bollinger* - strong DOWN (cross DOWN middle line)'
        score = -6.25
    elif crossunder_high == 1:
        msg = '*Bollinger* - strong DOWN (cross DOWN upper line)'
        score = -6.25
    elif crossoveer_low == 1:
        msg = '*Bollinger* - strong UP (cross UP lower line)'
        score = 6.25

    else:
        if upper_line.iloc[-1] > price.iloc[-1] > middle_line.iloc[-1]:
            msg = '*Bollinger* - weak UP'
            score = 3.125
        elif lower_line.iloc[-1] < price.iloc[-1] < middle_line.iloc[-1]:
            msg = '*Bollinger* - weak DOWN'
            score = -3.125
        else:
            msg = "*Bollinger* - neutral"
            score = 0
    return score, msg


async def get_data(ticker, tf):
    exchange = ccxt.binance()
    try:
        bars = await exchange.fetch_ohlcv(ticker, timeframe=tf, limit=100)
        await exchange.close()
        data = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        price = data['close'].iloc[-1]
        super_score, supert = check_supertrend(data)
        adx_score, adx = check_adx(data)
        rsi_score, rsi = check_rsi(data)
        macd_score, macd = check_macd(data)
        squeeze_score, squeeze = check_squeeze(data)
        ichimoku_score, ichimoku = check_ichimoku(data)
        cmf_score, cmf = check_cmf(data)
        bb_score, bbands = check_bbands(data)
        result = 50 + super_score + adx_score + rsi_score + macd_score + squeeze_score + \
                 ichimoku_score + cmf_score + bb_score
        get_chart(result)

        msg = f"🔸*{ticker}* - *{tf}*🔸\n" \
              f"*Price* - {price}\n\n" \
              f"_Trend Indicators:_\n\n" \
              f"{supert}\n" \
              f"{adx}\n\n" \
              f"_Oscilators:_\n\n" \
              f"{rsi}\n" \
              f"{macd}\n" \
              f"{squeeze}\n" \
              f"{cmf}\n\n" \
              f"_MA indicators:_\n\n" \
              f"{ichimoku}\n" \
              f"{bbands}"

    except:
        msg = "No data available"
        await exchange.close()
        result = 0
    return msg, result


async def generate_msg(pair, ft):
    # msg, score = asyncio.get_event_loop().run_until_complete(get_data(pair, ft))
    msg, score = await get_data(pair, ft)
    return msg


if __name__ == "__main__":
    async def main():
        tf = ['1m', '5m', '5m', '15m', '30m', '1h', '4h', '1d']
        eth = await asyncio.create_task(generate_msg("ETH/USDT", '1m'))
        # for i in tf:
            # eth = asyncio.create_task(generate_msg("ETH/USDT", i))
            # btc = asyncio.create_task(generate_msg("BTC/USDT", i))
            # bnb = asyncio.create_task(generate_msg("BNB/USDT", i))
            # dot = asyncio.create_task(generate_msg("DOT/USDT", i))
            # await eth
            # await btc
            # await bnb
            # await dot
        print(eth)

    asyncio.run(main())
