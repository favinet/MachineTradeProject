import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import numpy as np

def get_financial_statements(code):
    url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=%s&fin_typ=0&freq_typ=Y" % (code)
    html = requests.get(url).text
    html = html.replace('<th class="bg r01c02 endLine line-bottom"colspan="8">연간</th>', "")
    html = html.replace("<span class='span-sub'>(IFRS연결)</span>", "")
    html = html.replace("<span class='span-sub'>(IFRS별도)</span>", "")
    html = html.replace("<span class='span-sub'>(GAAP개별)</span>", "")
    html = html.replace("\t", "")
    html = html.replace("\n", "")
    html = html.replace("\r", "")

    for year in range(2009, 2018):
        for month in range(6, 13):
            month = "/%02d" % month
            html = html.replace(str(year)+month, str(year))

        for month in range(1,6):
            month = "/%02d" % month
            html = html.replace(str(year+1)+month, str(year))

        html = html.replace(str(year) + '(E)', str(year))

    #print(html)
    df_list = pd.read_html(html, index_col='주요재무정보')
    df = df_list[0]
    #print(df)
    return df

def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2016"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    tr_data = soup.find_all('tr', id='tr_288401_1')
    td_data = tr_data[0].find_all('td')
    #print(td_data)
    treasury_3year = {}
    start_year = 1998
    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year += 1

    print(treasury_3year)
    return treasury_3year

def get_current_3year_treasury():
    url = "http://info.finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    tbody_data = soup.find_all('tbody')
    tr_data = tbody_data[0].find_all('tr')
    td_data = tr_data[0].find_all('td')
    return td_data[1].text

def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    td_data = soup.find_all('td', {'class': 'cmp-table-cell td0301'})

    if not td_data:
        return ""

    dt_data = td_data[0].find_all('dt')
    dividend_yield = dt_data[5].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]
    return dividend_yield

def get_estimated_dividend_yield(code):
    df = get_financial_statements(code)
    dividend_yield = df.ix["현금배당수익률"]
    now = datetime.datetime.now()
    cur_year = now.year

    if str(cur_year) in dividend_yield.index and not np.isnan(dividend_yield[str(cur_year)]):
        return dividend_yield[str(cur_year)]
    elif str(cur_year-1) in dividend_yield.index and not np.isnan(dividend_yield[str(cur_year-1)]):
        return dividend_yield[str(cur_year-1)]
    else:
        return np.NaN

def get_previous_dividend_yield(code):
    df = get_financial_statements(code)
    dividend_yield = df.ix["현금배당수익률"]
    now = datetime.datetime.now()
    cur_year = now.year

    previous_dividend_yield = {}

    for year in range(cur_year-5, cur_year):
        if str(year) in dividend_yield.index:
            previous_dividend_yield[year] = dividend_yield[str(year)]

    return previous_dividend_yield


if __name__ == "__main__":
    #df = get_financial_statements("035720")
    #print(df)
    #get_3year_treasury()
    #dividend_yield = get_dividend_yield("058470")
    #print(dividend_yield)
    #estimated_dividend_yield = get_estimated_dividend_yield("058470")
    #print(estimated_dividend_yield)
    print(get_previous_dividend_yield("058470"))