import pyupbit
import time
import pandas
# pandas는 데이터 조작 및 분석을 위한 Python 프로그래밍 언어 용으로 작성된 소프트웨어 라이브러리

# 로그인 
access = "sSM1aDu6usf0GX18HXfeHx9u8yVrDrjutNoRszqu"          # 본인 값으로 변경
secret = "XKmFcOI6Uau565KChW6IagyLN1vIdnmnE8HzhOhz"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

#   RSI란?
#   주어진 기간의 모든 날의 코인가격에 대해서
#   가격이 전일 가격보다 상승한 날의 상승분 = U (Up)
#   가격이 전일 가격보다 하락한 날의 하락분 = D (Down)
#   U 값과 D 값의 평균값을 구하여 그것을 각각 AU (Average Up) 와 AD (Average Down)이라 한다
#   AU를 AD로 나눈것을 RS(Relative Strength)라 한다
    # RSI = 100 - [ 100 / ( 1+ RS ) ]

# RSI 구하는 함수
def rsi(ohlc: pandas.DataFrame, period: int = 14) :
       delta = ohlc["close"].diff()
       ups,downs = delta.copy(), delta.copy()
       ups[ups < 0] = 0
       downs[downs > 0] = 0
       AU = ups.ewm(com = period-1, min_periods = period).mean()
       AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
       RS = AU / AD
       return pandas.Series(100 - (100 / (1 + RS)), name = "RSI")

#MACD 구하는 지표 [https://technfin.tistory.com/entry/MACD-%EC%A7%80%ED%91%9C-%EA%B5%AC%ED%95%98%EA%B8%B0-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%97%85%EB%B9%84%ED%8A%B8-%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8-%EC%9E%90%EB%8F%99%EB%A7%A4%EB%A7%A4]
# - Name : get_macd
# - Desc : MACD 조회
# - Input
#   1) target_item : 대상 종목
#   2) tick_kind : 캔들 종류 (1, 3, 5, 10, 15, 30, 60, 240 - 분, D-일, W-주, M-월)
#   3) inq_range : 캔들 조회 범위
#   4) loop_cnt : 지표 반복계산 횟수
# - Output
#   1) MACD 값

def get_macd(target_item, tick_kind, inq_range, loop_cnt):
    try:
 
        # 캔들 데이터 조회용
        candle_datas = []
 
        # MACD 데이터 리턴용
        macd_list = []
 
        # 캔들 추출
        candle_data = get_candle(target_item, tick_kind, inq_range)
 
        # 조회 횟수별 candle 데이터 조합
        for i in range(0, int(loop_cnt)):
            candle_datas.append(candle_data[i:int(len(candle_data))])
 
        df = pd.DataFrame(candle_datas[0])
        df = df.iloc[::-1]
        df = df['trade_price']
 
        # MACD 계산
        exp1 = df.ewm(span=12, adjust=False).mean()
        exp2 = df.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
 
        for i in range(0, int(loop_cnt)):
            macd_list.append(
                {"type": "MACD", "DT": candle_datas[0][i]['candle_date_time_kst'], "MACD": round(macd[i], 4), "SIGNAL": round(exp3[i], 4),
                 "OCL": round(macd[i] - exp3[i], 4)})
 
        return macd_list
    except Exception:
        raise

# # 업비트에 있는 현금 확인
seed_m = upbit.get_balance("KRW")
tickers = ["KRW-BTC", "KRW-ETH", "KRW-MTL", "KRW-LTC", "KRW-XRP", "KRW-ETC", "KRW-OMG", "KRW-SNT", "KRW-WAVES", "KRW-XEM", "KRW-QTUM", "KRW-LSK", "KRW-STEEM", "KRW-XLM", "KRW-ARDR", "KRW-ARK", "KRW-STORJ", "KRW-GRS", "KRW-REP", "KRW-ADA", "KRW-SBD", "KRW-POWR", "KRW-BTG", "KRW-ICX", "KRW-EOS", "KRW-TRX", "KRW-SC", "KRW-ONT", "KRW-ZIL", "KRW-POLY", "KRW-ZRX", "KRW-LOOM", "KRW-BCH", "KRW-BAT", "KRW-IOST", "KRW-RFR", "KRW-CVC", "KRW-IQ", "KRW-IOTA", "KRW-MFT", "KRW-ONG", "KRW-GAS", "KRW-UPP", "KRW-ELF", "KRW-KNC", "KRW-BSV", "KRW-THETA", "KRW-QKC", "KRW-BTT", "KRW-MOC", "KRW-ENJ", "KRW-TFUEL", "KRW-MANA", "KRW-ANKR", "KRW-AERGO", "KRW-ATOM", "KRW-TT", "KRW-CRE", "KRW-MBL", "KRW-WAXP", "KRW-HBAR", "KRW-MED", "KRW-MLK", "KRW-STPT", "KRW-ORBS", "KRW-VET", "KRW-CHZ", "KRW-STMX", "KRW-DKA", "KRW-HIVE", "KRW-KAVA", "KRW-AHT", "KRW-LINK", "KRW-XTZ", "KRW-BORA", "KRW-JST", "KRW-CRO", "KRW-TON", "KRW-SXP", "KRW-HUNT", "KRW-PLA", "KRW-DOT", "KRW-SRM", "KRW-MVL", "KRW-STRAX", "KRW-AQT", "KRW-GLM", "KRW-SSX" ]
mycoin = upbit.get_balance(tickers)

# 지정 RSI값 터치 확인용
lower_touch = [] 

# RSI 터치 초기화 작업용 
for i in range(len(tickers)): 
    lower_touch.append(False) 

print(seed_m)

while True :
    for i in range(len(tickers)) :
       t_price = pyupbit.get_current_price(tickers[i])
       data = pyupbit.get_ohlcv(tickers[i], interval = "minute240")
       now_rsi = rsi(data, 14).iloc[-1]

       if now_rsi < 27 :
          lower_touch[i] = True

       # 매수 평균가 얻어오기
       avg = upbit.get_avg_buy_price(tickers[i]) 

       # 매수 조건 설정하기
       # 만약 RSI가 30보다 작고, 평균 매수가 (매수 평단가)가 0이면 10000원 매수 
       if now_rsi < 30 and avg == 0 and lower_touch[i] == True :
           upbit.buy_market_order(tickers[i], 200000)
           lower_touch[i] = False
           print("Buy")
           print(seed_m)


       # 매도 조건1 설정하기
       # 만약 RSI가 70 보다크고, 현재 가격이 매수평단가 보다 2%이상 높다면 단," 매수평단가가 0이 아니어야 함 "  
       if now_rsi > 70 and t_price > ( avg*1.02 ) and avg != 0 :
            s_coin = upbit.get_balance(tickers[i])
            upbit.sell_market_order(tickers[i], s_coin)
            print("sell")
            print(seed_m)


       # 매도 조건2 설정하기
       # 현재 가격이 매수평단가 보다 2%이상 높다면 
       if t_price > ( avg*1.02 ) and avg != 0 :
              s_coin = upbit.get_balance( tickers[i] )
              upbit.sell_market_order(tickers[i], s_coin)
              print("sell")
              print(seed_m)

       # 출력
       

       time.sleep(0.1)
