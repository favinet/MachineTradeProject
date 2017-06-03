import pandas_datareader.data as web
import matplotlib.pyplot as plt
import fix_yahoo_finance

def getStockValue():
    gs = web.DataReader("KOSDAQ:041510", "google", "2017-01-01", "2017-02-01")
    #gs = web.get_data_yahoo("095610.KS", "2017-01-01", "2017-02-01")
    print(gs)
    #plt.plot(gs['Adj Close'])
    #plt.show()

def drawMeanGraph():
    gs = web.DataReader("078930", "google")
    new_gs = gs[gs['Volume'] != 0]
    ma5 = new_gs['Close'].rolling(window=5).mean()
    ma20 = new_gs['Close'].rolling(window=20).mean()
    ma60 = new_gs['Close'].rolling(window=60).mean()
    ma120 = new_gs['Close'].rolling(window=120).mean()
    new_gs.insert(len(new_gs.columns), "MA5", ma5)
    new_gs.insert(len(new_gs.columns), "MA20", ma20)
    new_gs.insert(len(new_gs.columns), "MA60", ma60)
    new_gs.insert(len(new_gs.columns), "MA120", ma120)
    plt.plot(new_gs.index, new_gs['Close'], label="Close")
    plt.plot(new_gs.index, new_gs['MA5'], label="MA5")
    plt.plot(new_gs.index, new_gs['MA20'], label="MA20")
    plt.plot(new_gs.index, new_gs['MA60'], label="MA60")
    plt.plot(new_gs.index, new_gs['MA120'], label="MA120")
    plt.legend(loc='best')
    plt.grid()
    plt.show()
    #print(new_gs.tail(5))

class DataReader:

    @staticmethod
    def getStockData(code, start, end):
        data = web.DataReader(code, "google", start, end)
        new_data = data[data['Volume'] != 0]
        dict = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
        for row in new_data:
            date = row["Date"]
            open = row["Open"]
            high = row["High"]
            low = row["Low"]
            close = row["Close"]
            volume = row["Volume"]

            dict['date'].append(date)
            dict['open'].append(int(open))
            dict['high'].append(int(high))
            dict['low'].append(int(low))
            dict['close'].append(int(close))
            dict['volume'].append(int(volume))

        return dict


if __name__ == "__main__":
    getStockValue()


