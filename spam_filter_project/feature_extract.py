# -*- coding: utf-8 -*-
"""
    特征提取

"""


import pandas as pd
import re
import numpy as np
import jieba


# 读取文件
df = pd.read_csv('./email_data/process01', sep=',', header=None, names=['from', 'to', 'date', 'content', 'label'])

# print(df.head())


def extract_email_server_address(strl):
    """
    提取邮件收发地址
    :param strl:
    :return:
    """
    # 正则匹配
    it = re.findall(r'@([A-Za-z0-9]*\.[A-Za-z0-9\.]+)', str(strl))

    result = ''

    if len(it) > 0:
        result = it[0]
    else:
        result = 'unknown'

    return result


df['from_address'] = pd.Series(map(lambda strl: extract_email_server_address(strl), df['from']))
df['to_address'] = pd.Series(map(lambda strl: extract_email_server_address(strl), df['to']))

# print(df.to_address.value_counts())
# print('*'*20)
# print(df.to_address.unique())

# 转为结构化的输出,带出列名
# from_address_df = df.from_address.value_counts().to_frame()
# print(from_address_df)
#
#
# less_than_10_from_address_count = from_address_df[from_address_df.from_address <= 10].shape
# print(less_than_10_from_address_count)

# print(df['date'])
# print('*'*20)
# print(np.unique(list(map(lambda t: len(str(t).strip()), df["date"]))))
#
# print('+'*20)
#
#
# print(np.unique(list(filter(lambda t: len(str(t).strip()) > 21, df['date']))))


def extract_date(date_str):
    """
    提取日期特征
     24~8=3;8~13=0;13~19=1;19~24=2;
    :param date_str:
    :return:
    """
    if not isinstance(date_str, str):
        date_str = str(date_str)

    date_str_len = len(date_str)

    week = ""
    hour = ""
    time_quantum = ""

    if date_str_len < 10:
        week = "unknown"
        hour = 'unknown'
        time_quantum = 'unknown'
        pass
    elif date_str_len == 16:    # ['2005-9-2 上午10:55' '2005-9-2 上午11:04' 'of Birth 1981/03']
        rex = r'(\d{2}):\d{2}'  # 只取冒号前的两位
        tem = re.findall(rex, date_str)
        if len(tem) == 1:
            hour = tem[0]
        else:
            hour = 'unknown'
        week = "Fri"
        time_quantum = '0'
        pass
    elif date_str_len == 19:    # ['Sep 23 2005 1:04 AM']
        week = 'Fri'
        hour = '01'
        time_quantum = '3'
        pass
    elif date_str_len == 21:    # ['of Birth:Nov. 29 1962']
        week = "unknown"
        hour = 'unknown'
        time_quantum = 'unknown'
        pass
    else:                       # Fri 1 Feb 2002 02:16:30 +0800
        rex = r"([A-Za-z]+\d?[A-Za-z]*) .*?(\d{2}):\d{2}:\d{2}.*"
        tem = re.findall(rex, date_str)
        if len(tem) == 1 and len(tem[0]) == 2:
            week = tem[0][0][-3:]
            hour = tem[0][1]
            int_hour = int(hour)
            if int_hour < 8:
                time_quantum = '3'
            elif int_hour < 13:
                time_quantum = '0'
            elif int_hour < 19:
                time_quantum = '1'
            else:
                time_quantum = '2'
        else:
            week = 'unknown'
            hour = 'unknown'
            time_quantum = 'unknown'
        pass

    week = week.lower()
    hour = hour.lower()
    time_quantum = time_quantum.lower()
    return(week, hour, time_quantum)


date_time_extract_result = list(map(lambda t: extract_date(t), df['date']))
df['date_week'] = pd.Series(map(lambda t: t[0], date_time_extract_result))
df['date_hour'] = pd.Series(map(lambda t: t[1], date_time_extract_result))
df['date_time_quantum'] = pd.Series(map(lambda t: t[2], date_time_extract_result))

# print('='*30)
# print(df.date_week.value_counts().head())
# print('='*30)
# print(df[['date_week', 'label']])
# print('='*30)
# print(df[['date_week', 'label']].groupby(['date_week', 'label']))
# print('='*30)
# print(df[['date_week', 'label']].groupby(['date_week', 'label'])['label'].count())

df['has_date'] = df.apply(lambda c: 0 if c['date_week'] == 'unknown' else 1, axis=1)    # 1:行

# 分词
df['content'] = df['content'].astype(str)
df['jieba_cut_content'] = list(map(lambda t: "  ".join(jieba.cut(t)), df['content']))


def extract_content_length(lg):
    """
    内容长度提取
    :param lg:
    :return:
    """
    if lg <= 10:
        return 0
    elif lg <= 100:
        return 1
    elif lg <= 500:
        return 2
    elif lg <= 1000:
        return 3
    elif lg <= 1500:
        return 4
    elif lg <= 2000:
        return 5
    elif lg <= 2500:
        return 6
    elif lg <= 3000:
        return 7
    elif lg <= 4000:
        return 8
    elif lg <= 5000:
        return 9
    elif lg <= 10000:
        return 10
    elif lg <= 20000:
        return 11
    elif lg <= 30000:
        return 12
    elif lg <= 50000:
        return 13
    else:
        return 14


df['content_length'] = pd.Series(map(lambda t: len(t), df['content']))
df['content_length_type'] = pd.Series(map(lambda t: extract_content_length(t), df['content_length']))


def extract_length_information(cl):
    """
    长度信息量
    :param cl:
    :return:    0~1之间
    """
    if cl > 10000:
        return 0.5 / np.exp(np.log10(cl) - np.log10(500)) + np.log(abs(cl - 500) + 1) - np.log(abs(cl - 10000)) + 1
    else:
        return 0.5 / np.exp(np.log10(cl) - np.log10(500)) + np.log(abs(cl - 500) + 1)


df["content_length_sema"] = pd.Series(map(lambda t: extract_length_information(t), df['content_length']))

df.drop(['from', 'to', 'date', 'from_address', 'to_address', 'date_week',
         'date_hour', 'date_time_quantum', 'content',
         'content_length', 'content_length_type'], 1, inplace=True)

df.to_csv('./email_data/result_process02', encoding='utf-8', index=False)
# df.to_csv('./email_data/process02.csv', encoding='utf-8', index=False)
