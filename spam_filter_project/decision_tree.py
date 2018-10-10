# -*- coding: utf-8 -*-
"""
    决策树

"""

import time
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import precision_score, f1_score, recall_score




df = pd.read_csv('./email_data/result_process02', sep=',')

df.dropna(axis=0, how='any', inplace=True)

X_train, X_test, y_train, y_test = train_test_split(df[['has_date', 'jieba_cut_content', 'content_length_sema']],
                                                    df['label'], random_state=42)

jieba_cut_content = list(X_train['jieba_cut_content'].astype('str'))

transformer = TfidfVectorizer(norm='l2', use_idf=True)

svd = TruncatedSVD(n_components=20)

transformer_model = transformer.fit(jieba_cut_content)
df1 = transformer_model.transform(jieba_cut_content)

svd_model = svd.fit(df1)
df2 = svd_model.transform(df1)

data = pd.DataFrame(df2)

data['has_date'] = list(X_train['has_date'])
data['content_length_sema'] = list(X_train['content_length_sema'])

# 决策树
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree_model = tree.fit(data, y_train)

# 测试数据
jieba_cut_content_test = list(X_test['jieba_cut_content'].astype('str'))
data_test = pd.DataFrame(svd_model.transform(transformer_model.transform(jieba_cut_content_test)))
data_test['has_date'] = list(X_test['has_date'])
data_test['content_length_sema'] = list(X_test['content_length_sema'])

start_time = time.time()
# 预测
y_pred = tree_model.predict(data_test)
end_time = time.time()

# 评估
precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)


print('精准率: %.5f' % precision)
print('f1均值: %.5f' % f1)
print('召回率: %.5f' % recall)

print('预测所用时长:', (end_time - start_time))


"""
    精准率: 0.95839
    f1均值: 0.97494
    召回率: 0.99207
    所用时长: 41.7101628780365
    
"""