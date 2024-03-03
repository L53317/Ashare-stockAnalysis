#股市行情数据获取和作图 -2
from  Ashare import *          #股票数据库    https://github.com/mpquant/Ashare
from  MyTT import *            #myTT麦语言工具函数指标库  https://github.com/mpquant/MyTT
'''
可以使用Meta的Prophet包来分析数据,更好地体现线性(增长)和非线性的时序数据。
'''

# 证券代码兼容多种格式 通达信，同花顺，聚宽
# sh000001 (000001.XSHG)    sz399006 (399006.XSHE)   sh600519 ( 600519.XSHG)

df=get_price('000001.XSHG',frequency='1d',count=1000)      #默认获取今天往前120天的日线行情
print('上证指数日线行情\n',df.tail(5))

#-------有数据了，下面开始正题 -------------
#基础数据定义，只要传入的是序列都可以  Close=df.close.values
#例如  CLOSE=list(df.close) 都是一样
CLOSE=df.close.values
OPEN=df.open.values
HIGH=df.high.values
LOW=df.low.values

MA5=MA(CLOSE,5)                                #获取5日均线序列
MA10=MA(CLOSE,10)                              #获取10日均线序列
up,mid,lower=BOLL(CLOSE)                       #获取布林带指标数据


#-------------------------作图显示-----------------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
# plt.figure(figsize=(10,5))
plt.figure()
plt.plot(CLOSE,label='CLOSE')
plt.plot(up,label='UP')           #画图显示
plt.plot(mid,label='MID')
plt.plot(lower,label='LOW')
plt.plot(MA5,label='MA5',linewidth=0.5,alpha=0.7)
plt.plot(MA10,label='MA10',linewidth=0.5,alpha=0.7)
plt.legend()
plt.grid(linewidth=0.5,alpha=0.7)
plt.gcf().autofmt_xdate(rotation=45)
plt.gca().xaxis.set_major_locator(MultipleLocator(len(CLOSE)/30))    #日期最多显示30个
plt.title('SH-INDEX   &   BOLL SHOW',fontsize=20)
plt.show()


## Spectrum analysis
import numpy as nps
from scipy import stats, signal
from scipy.fft import fft, fftfreq

def plotSpectrum(data, fs = 1e2):
    N = len(data)
    data = data.values.tolist() # TODO
    xf = fftfreq(N, 1/fs)[:N//2]
    yf = fft(data)
    return xf, yf


# # frequecy
# fs = 1e2
# N = len(df)
# # Fourier transform
# npArray = df.close.values
# # npArray = MA5
# yf = fft(npArray)
# xf = fftfreq(N, 1/fs)[:N//2]
# plt.figure()
# plt.subplot(211)
# plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
# plt.xlabel('Frequency (B:Hz)')
# plt.ylabel('Amplitude (A)')
# plt.grid()
# # plt.show()
# # spectrum analysis
# F, T, Sxx = signal.spectrogram(npArray, fs=fs) # freqs, time, Spectrogram of x
# plt.subplot(212)
# plt.pcolormesh(T, F, Sxx, shading='auto') #, shading='flat'; auto=nearest, gouraud
# plt.ylabel('Frequency (B: Hz)')
# plt.xlabel('Time (s)')
# plt.show()


figSpe=plt.figure()
stockId='600519.XSHG'
df=get_price(stockId,frequency='1d',count=1000)
# print('茅台日线行情\n',df.tail(5))
xf,yf = plotSpectrum(df)
plt.subplot()
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),label=stockId)
stockId='600900.XSHG'
df=get_price(stockId,frequency='1d',count=1000)
# print('长江水电日线行情\n',df.tail(5))
xf,yf = plotSpectrum(df)
plt.subplot()
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),label=stockId)
stockId='601857.XSHG'
df=get_price(stockId,frequency='1d',count=1000)
# print('中国石油日线行情\n',df.tail(5))
xf,yf = plotSpectrum(df)
plt.subplot()
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),label=stockId)
stockId='002415.XSHE'
df=get_price(stockId,frequency='1d',count=1000)
# print('海康威视日线行情\n',df.tail(5))
xf,yf = plotSpectrum(df)
plt.subplot()
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]),label=stockId)


figSpe.legend()
plt.xlabel('Frequency (B:Hz)')
plt.ylabel('Amplitude (A)')
plt.grid()
plt.show()