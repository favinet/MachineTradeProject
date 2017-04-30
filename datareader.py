import pandas_datareader.data as web
import matplotlib.pyplot as plt

gs = web.DataReader("078930.KS", "yahoo")

plt.plot(gs['Adj Close'])
plt.show()