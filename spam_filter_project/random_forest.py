# -*- coding: utf-8 -*-
"""
    随机森林

"""

import sys
import time
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, recall_score, precision_score


start_time = time.time()

df = pd.read_csv('./email_data/result_process02', sep=',')
# print(df.head())
# print(df.info())


df.dropna(axis=0, how='any', inplace=True)

# print(df.info())

# sys.exit('暂停')

X_train, X_test, y_train, y_test = train_test_split(df[['has_date', 'jieba_cut_content', 'content_length_sema']],
                                                    df['label'], random_state=42)

# 文本特征数值计算
transformer = TfidfVectorizer(norm='l2', use_idf=True)
# 降维
svd = TruncatedSVD(n_components=20)

jieba_cut_content = list(X_train['jieba_cut_content'].astype('str'))

transformer_model = transformer.fit(jieba_cut_content)
df1 = transformer_model.transform(jieba_cut_content)

svd_model = svd.fit(df1)
df2 = svd_model.transform(df1)

data = pd.DataFrame(df2)

# print(data.info())
# print(data.head())
# print('**'*20)

data['has_date'] = list(X_train['has_date'])
data['content_length_sema'] = list(X_train['content_length_sema'])

# print(data.head())
# print('**'*20)

rf = RandomForestClassifier(n_estimators=100, criterion='gini', max_depth=3, random_state=42)

rf_model = rf.fit(data, y_train)

jieba_cut_content_test = list(X_test['jieba_cut_content'].astype('str'))
data_test = pd.DataFrame(svd_model.transform(transformer_model.transform(jieba_cut_content_test)))

data_test['has_date'] = list(X_test['has_date'])
data_test['content_length_sema'] = list(X_test['content_length_sema'])

y_predict = rf_model.predict(data_test)


precision = precision_score(y_test, y_predict)
f1 = precision_score(y_test, y_predict)
recall = recall_score(y_test, y_predict)

print('精准率: %.5f' % precision)
print('f1: %.5f' % f1)
print('召回率: %.5f' % recall)

end_time = time.time()


print('所用时长:', (end_time - start_time))

"""
    精准率: 0.94649
    f1: 0.94649
    召回率: 0.99065
    所用时长: 43.23180603981018
"""
