# -*- coding: utf-8 -*-
"""
    k最近邻

"""

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import precision_score, f1_score, recall_score

import time



df = pd.read_csv('./email_data/result_process02', sep=',')

df.dropna(how='any', axis=0, inplace=True)

X_train, X_test, y_train, y_test = train_test_split(df[['has_date', 'jieba_cut_content', 'content_length_sema']],
                                                    df['label'], random_state=42)


jieba_cut_content = list(X_train['jieba_cut_content'].astype('str'))

transformer = TfidfVectorizer(norm='l2', use_idf=True)
transformer_model = transformer.fit(jieba_cut_content)
df1 = transformer_model.transform(jieba_cut_content)

svd = TruncatedSVD(n_components=20)
svd_model = svd.fit(df1)
df2 = svd_model.transform(df1)

data = pd.DataFrame(df2)

data['has_date'] = list(X_train['has_date'])
data['content_length_sema'] = list(X_train['content_length_sema'])

knn = KNeighborsClassifier(n_neighbors=5)
knn_model = knn.fit(data, y_train)


jieba_cut_content_test = list(X_test['jieba_cut_content'].astype('str'))
data_test = pd.DataFrame(svd_model.transform(transformer_model.transform(jieba_cut_content_test)))

start_time = time.time()
y_pred = knn_model.predict(data_test)
end_time = time.time()

precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)



print('精准度: %.5f' % precision)
print('f1均值: %.5f' % f1)
print('召回率: %.5f' % recall)

print('预测所用时间: ', (end_time - start_time))
