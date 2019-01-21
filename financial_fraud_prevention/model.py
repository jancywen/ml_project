# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model.logistic import LogisticRegression
from sklearn.ensemble.forest import RandomForestClassifier


from sklearn.metrics import f1_score, recall_score, accuracy_score

import matplotlib.pyplot as plt

import time


df = pd.read_csv('./data/df_data.csv', low_memory=True)

# print(df.revol_util.head())

# print(df.loan_status.value_counts())



y = df.loan_status

X = df.drop(['loan_status'], axis=1)


train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=0)

lr_start = time.time()

lr = LogisticRegression()

lr.fit(train_X, train_y)
train_pred = lr.predict(train_X)

print('*'*20, '逻辑回归', '*'*20)

print('训练集准确率:', accuracy_score(train_y, train_pred))
print('训练集召回率:', recall_score(train_y, train_pred))
print('训练集 f1:', f1_score(train_y, train_pred))


test_pred = lr.predict(test_X)

print('测试集准确率:', accuracy_score(test_y, test_pred))
print('测试集召回率:', recall_score(test_y, test_pred))
print('测试集 f1:', f1_score(test_y, test_pred))

lr_end = time.time()

print('lr耗时: ', lr_end - lr_start)




rf_start = time.time()

rf = RandomForestClassifier()
rf.fit(train_X, train_y)
train_pred = rf.predict(train_X)

print('*'*20, '逻辑回归', '*'*20)

print('训练集准确率:', accuracy_score(train_y, train_pred))
print('训练集召回率:', recall_score(train_y, train_pred))
print('训练集 f1:', f1_score(train_y, train_pred))

test_pred = rf.predict(test_X)

print('测试集准确率:', accuracy_score(test_y, test_pred))
print('测试集召回率:', recall_score(test_y, test_pred))
print('测试集 f1:', f1_score(test_y, test_pred))

rf_end = time.time()

print('lr耗时: ', rf_end - rf_start)

feature_importance = rf.feature_importances_

# feature_importance = 100*(feature_importance/feature_importance.max())
# index = np.argsort(feature_importance)[-13:]
# print(index)
# plt.barh(np.arange(13), feature_importance[index], color='dodgerblue', alpha=0.4)
# plt.yticks(np.arange(10+0.25), np.array(X.columns)[index])
# plt.xlabel('Relative importance')
# plt.title('Top 10 Importance Variable')
# plt.show()


feature_importance = 100.0*(feature_importance/feature_importance.max())
index = np.argsort(feature_importance)[-13:]
plt.barh(np.arange(13), feature_importance[index], color = 'dodgerblue', alpha = 0.4)
print(np.array(X.columns)[index])
plt.yticks(np.arange(13+0.25), np.array(X.columns)[index])
plt.xlabel('Relative importance')
plt.title('Top 10 Importance Variable')
plt.tight_layout()
plt.show()