#Scroll to the bottom for user input

def calc(ticker, date, target, risk):
  side = 'CALL'  

  import requests
  import json
  from datetime import datetime
  from dateutil.relativedelta import relativedelta
  import warnings

  warnings.filterwarnings("ignore", category=DeprecationWarning) 

  datelist = date.split('-')
  d = int(datelist[0])
  m = int(datelist[1])
  y = int(datelist[2])
  now =  datetime.strptime(date, '%d-%m-%Y')
  todate = now + relativedelta(months=+6)
  today = datetime.today()
  todate = todate.strftime('%Y-%m-%d')
  fromdate = str(str(y) + '-' + str(m) + '-' + str(d))

  td_consumer_key = 'Y45TLKCXRODPNXTIVI74E3PY5QPQGWDO'

  base_url = 'https://api.tdameritrade.com/v1/marketdata/chains?&symbol={stock_ticker}&contractType={contractType}&fromDate={fromdate}&toDate={todate}'
  endpoint = base_url.format(stock_ticker = ticker,
      contractType = side,
      fromdate = fromdate,
      todate = todate)
  #print(fromdate + ' to ' + todate)
  page = requests.get(url=endpoint, params={'apikey' : td_consumer_key})
  content = json.loads(page.content)

  #Get a list of options that match the criteria (OI>50)
  chain = content['callExpDateMap']
  options = []
  expiries = []
  for i in chain:
    dict1 = chain[i]
    for x in dict1:
      list1 = dict1[x]
      dict2 = list1[0]
      if dict2['openInterest']>50:
        options.append((x,dict2))

  def estimate_prices(options, target, date):
    from scipy.interpolate import interp1d
    from scipy import sqrt, log, exp
    from scipy.stats import norm
    from scipy.optimize import fsolve

    prices = []
    for o in options:
      strike = float(o[0])
      odict = o[1]
      #Black and Scholes Calculation:
      r = 0.02 #blackandscholes.riskfree()
      S = float(target)
      K = strike
      duration = odict['daysToExpiration'] 
      today = datetime.today()
      timediff = now - today
      T = duration-timediff.days
      T = T/365
      price = (odict['bid']+odict['ask'])/2
      option = 'Call'  
      q = 0
      sigma = 0.25
      d1 = (log(S/K) + (r - q + (sigma**2)/2)*T)/(sigma*sqrt(T))
      d2 = d1 - sigma*sqrt(T)
      BS_est = S*exp(-q*T)*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
      expiration = datetime.today() + relativedelta(days=+duration)
      expiration = expiration.strftime('%d-%m-%Y')
      p = (expiration, strike, float(price)*100, BS_est)
      prices.append(p)
    #print('Prices:' + str(prices))    
    return prices

  def profit_est(prices, risk):
    from math import floor
    pl = []
    for k in prices:
      price = k[2]
      max_contracts = floor((float(risk)/price))
      if max_contracts > 0:
        cost = max_contracts*price
        est_profit = k[3]*100*max_contracts-cost
        strike = str(k[1])
        expiration = str(k[0])
        p = (expiration, strike, est_profit)
        pl.append(p)
    return pl, max_contracts

  prices = estimate_prices(options,target,date)
  pl, max_contracts = profit_est(prices, risk)

  from mpl_toolkits import mplot3d
  import numpy as np
  import matplotlib.pyplot as plt
  import matplotlib.ticker as tcker
  fig = plt.figure()
  ax = plt.axes(projection='3d')
  x = []
  y = []
  z = []
  xl = []
  for g in pl:
    if g[2]>0:
      z.append(g[2])
      y.append(float(g[1]))
      x.append(datetime.strptime(g[0], "%d-%m-%Y").timestamp())
      if g[0] not in xl:
        xl.append(g[0])
  ax.scatter3D(x, y, z)
  ax.w_xaxis.set_major_locator(tcker.FixedLocator(x))
  ax.w_xaxis.set_major_formatter(tcker.FuncFormatter(lambda date, _: datetime.fromtimestamp(date).strftime("%Y-%m-%d")))

  ax.set_xlabel('Expiry')
  ax.set_ylabel('Strike Price')
  ax.set_zlabel('Est Profit')
  res = sorted(pl, key = lambda i: i[2], reverse = True)[0]
  print('Risk: ${}'.format(risk))
  print('Option: {} {}C {}'.format(ticker, res[1], res[0]))
  print('# of Contracts: {}'.format(max_contracts))
  print('Estimated Profit: ${}'.format(int(res[2])))
  max = int(res[2]*1.15)
  ax.set_zlim(0,max)
  plt.show()

if __name__ == "__main__":

  #You're input here:
  ticker = 'AAPL'     #Uppercase
  date = '12-08-2021' #DD-MM-YYYY Earliest date by which you believe the target price will be hit
  target = '152'       #What you think the price will reach by the date
  risk = '1000'       #Amount of money to risk
  # press play

  s = calc(ticker, date, target, risk)
  s
