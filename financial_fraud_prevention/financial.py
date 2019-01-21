# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import sys

df = pd.read_csv('./data/LoanStats3a.csv', skiprows=1, low_memory=True)


# 清洗数据 去除特征中的特殊字符
df.term.replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)

df.emp_length.replace('n/a', value=np.nan, inplace=True)
df.emp_length.replace(to_replace='[^0-9]+', value='', inplace=True, regex=True)

# 删除空值
df.dropna(axis=1, how='all', inplace=True)
df.dropna(axis=0, how='all', inplace=True)

# print('*'*20)
# print(df.info())


"""
    删除空值较多的列

debt_settlement_flag_date     160 non-null object
settlement_status             160 non-null object
settlement_date               160 non-null object
settlement_amount             160 non-null float64
settlement_percentage         160 non-null float64
settlement_term               160 non-null float64
"""
df.drop(['debt_settlement_flag_date',
         'settlement_status',
         'settlement_date',
         'settlement_amount',
         'settlement_percentage',
         'settlement_term'], axis=1, inplace=True)

# 删除不为空,单特征重复较多的 0/n/f
# 删除方法: 删除float类型的列,删object的列


def dropFeature(f):
    df.drop(f, axis=1, inplace=True)


for clo in df.select_dtypes(include=['object', 'float']).columns:
    if len(df[clo].unique()) < 1000:
        # print(clo, len(df[clo].unique()))
        if clo not in ['loan_status', 'int_rate'] :
            dropFeature(clo)

dropFeature(['desc', 'title', 'emp_title'])

# 标签二值化
df.loan_status.replace('Fully Paid', value=int(1), inplace=True)
df.loan_status.replace('Charged Off', value=int(0), inplace=True)

df.loan_status.replace('Does not meet the credit policy. Status:Fully Paid', value=np.nan, inplace=True)
df.loan_status.replace('Does not meet the credit policy. Status:Charged Off', value=np.nan, inplace=True)

# 删除标签为 0 的样本
df.dropna(subset=['loan_status'], inplace=True)

# 填充空值 0.0
df.fillna(0.0, inplace=True)

print(df.loan_status.value_counts())

print(df.info())

# 去除多重相关性特征,保留一列

# cor = df.corr()
# cor.iloc[:, :] = np.tril(cor, k=-1)
# cor = cor.stack()
# print(cor[(cor > 0.55) | (cor < -0.55)])

dropFeature(['funded_amnt', 'total_pymnt'])

print(df.info())

# 哑编码
df = pd.get_dummies(df)

df.to_csv('./data/df_data.csv')
