'''
股票市场的周期性是投资者关注的重要因素之一。在Python中，我们可以使用不同的工具来分析股票的上涨和下跌周期，以及绘制频谱图。

首先，我们将探讨如何分析股票的周期性。以下是一些步骤：

使用Fbprophet进行周期性分析：
Fbprophet是Facebook发布的一个开源软件，旨在为大规模预测提供一些有用的指导。
默认情况下，它会将时间序列划分为趋势和季节性，可能包含年度、周度和每日。
你可以根据自己的需求定义自己的周期，找出哪些更适合数据。
通过添加自定义周期，我们可以更好地理解隐藏在股市中的周期。
示例：以Costco为例：
使用pandas_datareader获取Costco标的从2015/10/1到2018/10/1的股票价格数据。
绘制股票价格图表，观察价格的周期性波动。
使用Fbprophet模型进行周期性分析，计算预测回报和样本均方误差。
'''

import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet     # need to test TODO
from sklearn.metrics import mean_squared_error
from pandas_datareader import data

# 获取Costco股票价格数据
ticker = "COST"
start_date = '2015-10-01'
end_date = '2018-10-01'
stock_data = data.DataReader(ticker, 'iex', start_date, end_date)

# 定义自定义周期
cycle = 8
split_date = '2018-03-31'

# 使用自定义函数进行周期性分析
def cycle_analysis(data, split_date, cycle, mode='additive', forecast_plot=False, print_ind=False):
    training = data[:split_date].iloc[:-1,]
    testing = data[split_date:]
    predict_period = len(pd.date_range(split_date, max(data.index)))
    df = training.reset_index()
    df.columns = ['ds', 'y']
    m = Prophet(weekly_seasonality=False, yearly_seasonality=False, daily_seasonality=False)
    m.add_seasonality('self_define_cycle', period=cycle, fourier_order=8, mode=mode)
    m.fit(df)
    future = m.make_future_dataframe(periods=predict_period)
    forecast = m.predict(future)
    ret = max(forecast.self_define_cycle) - min(forecast.self_define_cycle)
    model_tb = forecast['yhat']
    model_tb.index = forecast['ds'].map(lambda x: x.strftime("%Y-%m-%d"))
    out_tb = pd.concat([testing, model_tb], axis=1)
    out_tb = out_tb[~out_tb.iloc[:, 0].isnull()]
    out_tb = out_tb[~out_tb.iloc[:, 1].isnull()]
    mse = mean_squared_error(out_tb.iloc[:, 0], out_tb.iloc[:, 1])
    rep = [ret, mse]
    if print_ind:
        print("Projected return per cycle: {}".format(round(rep[0], 2)))
        print("MSE: {}".format(round(rep[1], 4)))
    return rep

# 调用自定义函数
cycle_analysis(stock_data['close'], split_date, cycle, forecast_plot=True, print_ind=True)