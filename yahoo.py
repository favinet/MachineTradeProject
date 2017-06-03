from pandas_datareader import data as pdr
import fix_yahoo_finance

# download dataframe
#data = pdr.get_data_yahoo("078930.KS", start="2017-01-01", end="2017-04-30")
data = pdr.get_data_yahoo("078930.KS", start="2017-05-01", end="2017-05-29")
#data = pdr.get_data_yahoo_actions("078930.KS", start="2017-01-01", end="2017-04-30")
print(data)

