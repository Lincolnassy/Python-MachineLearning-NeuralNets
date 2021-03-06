
'''
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

X_train = [[1,2],[2,4],[6,7]]
y_train = [1.2, 4.5, 6.7]
X_test = [[1,3],[2,5]]

# create a Linear Regressor
lin_regressor = LinearRegression()

# pass the order of your polynomial here
poly = PolynomialFeatures(2)

# convert to be used further to linear regression
X_transform = poly.fit_transform(X_train)

print(X_transform)

# fit this to Linear Regressor
lin_regressor.fit(X_transform,y_train)

# get the predictions
lin_regressor.fit(X_transform, y_train)
'''


import pandas as pd
import quandl, math, datetime
import numpy as np
#from sklearn import preprocessing, cross_validation, svm
from sklearn import preprocessing, model_selection, svm
from sklearn.linear_model import LinearRegression
from sklearn.isotonic import isotonic_regression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle



style.use('ggplot')

quandl.ApiConfig.api_key = "xp-xmYQENNfYgnM1M8ZS"

df = quandl.get("BITFINEX/BTCUSD")
forecast_col = 'Last'
df = df[['Last', 'Volume']]

#df = quandl.get("WIKI/GOOGL")
# df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume', ]]
# df['HL_PCT'] = (df['Adj. High'] - df['Adj. Close']) / df['Adj. Close'] * 100.0
# df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0
# df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
#forecast_col = 'Adj. Close'

df = df.tail(n=60)
#print(df.tail(n=20))

df.fillna(-99999, inplace=True)

forecast_out = int(math.ceil(0.003*len(df)))
#print(forecast_out)
df['label'] = df[forecast_col].shift(-forecast_out)


x = np.array(df.drop(['label'], 1))
x = preprocessing.scale(x)
x_lately = x[-forecast_out:]
x = x[:-forecast_out]


df.dropna(inplace=True)
y = np.array(df['label'])


x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.30)

clf = LinearRegression(n_jobs=-1)
clf.fit(x_train, y_train)


with open('linearregression.pickle', 'wb') as f:
    pickle.dump(clf, f)

pickle_in = open('linearregression.pickle', 'rb')
clf = pickle.load(pickle_in)





accuracy = clf.score(x_test, y_test)

forecast_set = clf.predict(x_lately)
print(forecast_set, accuracy, forecast_out)
df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += one_day
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)] + [i]

print(df.tail())

#df['Adj. Close'].plot()
df['Last'].plot()

df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

































