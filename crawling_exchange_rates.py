### 환율 예측
from bs4 import BeautifulSoup
import urllib.request as req
from pandas import DataFrame
import numpy as np
import json
import requests
import re

def SoupConvert(arg):
    res = req.urlopen(arg)
    soup = BeautifulSoup(res,'html.parser')
    return soup
# 환율 페이지 추출
url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW"
soup = SoupConvert(url)
page = soup.select_one('div.paging > a').get('href')
page_url = 'https://finance.naver.com/'+page[1:-1]

# 환율 추출
exchange = DataFrame(columns = ['exchange','v'])

# 420일
date = 42

# exhcnage
e_iter = int(date/10)
for i in range(1,e_iter+1):
    url = page_url+str(i)
    soup = SoupConvert(url)
    webdata = soup.select('tbody > tr')
    for i in webdata:
        ex_temp = i.select('td.num')
        exchange.loc[i.select('td.date')[0].string] = [ex_temp[0].string.replace(',',''),ex_temp[1].find('img').get('alt')]
        print(exchange.index[-1])
print('총 %d건 추출'%len(exchange))


# attrubute
## kospi kosdaq (6)
k_iter = int(date/6)
exchange = exchange.reindex(columns = np.append(exchange.columns,['KOSPI','KOSDAQ']))
# kos_index = DataFrame(columns = ['KOSPI','KOSDAQ'])
kos_url = "https://finance.naver.com/sise/sise_index_day.nhn?code={}&page="
for i in range(1,k_iter+1):
    kospi_url = kos_url.format('KOSPI')+str(i)
    kosdaq_url = kos_url.format('KOSDAQ')+str(i)
    
    kospi_soup = SoupConvert(kospi_url)
    kosdaq_soup = SoupConvert(kosdaq_url)
    
    date_kos = kospi_soup.select('td.date')
    kospi = [kospi_soup.select('td.number_1')[i] for i in range(0,24,4)]
    kosdaq = [kosdaq_soup.select('td.number_1')[i] for i in range(0,24,4)]

    for i in range(6):
        exchange['KOSPI'].loc[date_kos[i].string] = float(kospi[i].string.replace(',',''))
        exchange['KOSDAQ'].loc[date_kos[i].string] = float(kosdaq[i].string.replace(',',''))
print('KOSPI,KOSDAQ 추출')
exchange

## WTI,Gasoline, gold
u_iter = int(date/7)
mk_index = DataFrame(columns = ['OIL','GOLD'])
mk_url = 'https://finance.naver.com/marketindex/worldDailyQuote.nhn?marketindexCd={}&fdtc=2&page='
symbol_mk = ['OIL_CL','CMDT_GC']

for i in range(1,u_iter+1):
    oil_url = mk_url.format(symbol_mk[0])+str(i)
    gold_url = mk_url.format(symbol_mk[1])+str(i)
    
    oil_soup = SoupConvert(oil_url)
    gold_soup = SoupConvert(gold_url)
    
    mk_date = oil_soup.select('td.date')
    oil = oil_soup.select('td.num')
    gold = gold_soup.select('td.num')
    
    v_iter = 0
    for i in range(7):
        mk_index.loc[re.sub('\s+','',mk_date[i].string)] = [re.sub('\s+','',oil[v_iter].string),re.sub('\s+','',gold[v_iter].string)]
        v_iter += 3
print('마켓인덱스 추출')

## exchange = exchange.reindex(columns = np.append(exchange.columns,['WTI','GSL','GOLD']))
## NASDAQ
us_index = DataFrame(columns = ['NASDAQ','DOW','S&P'])
usd_url = 'https://finance.naver.com/world/worldDayListJson.nhn?symbol={}&fdtc=0&page='
symbol = ['NAS@IXIC','DJI@DJI','SPI@SPX']
for i in range(1,e_iter+1): # KOSPI level
    json_url = usd_url.format(symbol[0])+str(i)
    json_string = requests.get(json_url).text
    for i in json.loads(json_string):
        us_index.at[i['xymd'][0:4]+'.'+i['xymd'][4:6]+'.'+i['xymd'][6:8],'NASDAQ'] = float(i['clos'])
## S&P
for i in range(1,e_iter+1): # KOSPI level
    json_url = usd_url.format(symbol[1])+str(i)
    json_string = requests.get(json_url).text
    for i in json.loads(json_string):
        us_index.at[i['xymd'][0:4]+'.'+i['xymd'][4:6]+'.'+i['xymd'][6:8],'DOW'] = float(i['clos'])

## S&P
for i in range(1,e_iter+1): # KOSPI level
    json_url = usd_url.format(symbol[2])+str(i)
    json_string = requests.get(json_url).text
    for i in json.loads(json_string):
        us_index.at[i['xymd'][0:4]+'.'+i['xymd'][4:6]+'.'+i['xymd'][6:8],'S&P'] = float(i['clos'])

print('미국인덱스 추출')


## 클래스작업


## 예측 알고리즘



## 시각화