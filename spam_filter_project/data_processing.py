# -*- coding: utf-8 -*-
"""
    数据处理

"""

import os
import sys
import time

def read_index_file(file_path):

    """
    制作标签字典
    :param file_path:
    :return:
    """

    type_dict = {"spam": "1", "ham": "0"}
    index_file = open(file_path)
    index_dict = {}
    try:
        for line in index_file:
            arr = line.split(" ")
            if len(arr) == 2:
                key, value = arr
            value = value.replace("../data", "").replace('\n', '')
            index_dict[value] = type_dict[key.lower()]
    finally:
        index_file.close()

    return index_dict


def read_file(file_path):
    """
    读取邮件文件
    :param file_path:
    :return:
    """
    file = open(file_path, 'r',encoding='gb2312', errors='ignore')

    content_dict = {}

    try:
        is_content = False
        for line in file:
            line = line.strip()
            if line.startswith("From"):
                content_dict['from'] = line[5:]
            elif line.startswith('To'):
                content_dict['to'] = line[3:]
            elif line.startswith('Date'):
                content_dict['date'] = line[5:]
            elif not line:
                is_content = True

            if is_content:
                if 'content' in content_dict:
                    content_dict['content'] += line
                else:
                    content_dict['content'] = line
    finally:
        file.close()

    return content_dict


def dict_to_text(file_path):
    """
    字典转文本
    :param file_path:
    :return:
    """
    content_dict = read_file(file_path)
    result_str = content_dict.get('from', 'unknown').replace(',', '').strip() + ','
    result_str += content_dict.get('to', 'unknown').replace(',', '').strip() + ','
    result_str += content_dict.get('date', 'unknown').replace(',', '').strip() + ','
    result_str += content_dict.get('content', 'unknown').replace(',', '').strip()

    return result_str


print('开始处理数据')

start_time = time.time()

index_dict = read_index_file('./email_data/full/index')

# print(index_dict)

# sys.exit('打印索引标签')


list0 = os.listdir('./email_data/data')
# print(list0)
# sys.exit('打印文件名称')

# 000~215
for l1 in list0:
    file_path = './email_data/data/' + l1
    list1 = os.listdir(file_path)

    wirte_file_path = './email_data/process01_' + l1

    with open(wirte_file_path, 'w', encoding='utf-8') as writer:
        for l2 in list1:
            l2_path = file_path + '/' + l2
            index_key = '/' + l1 + '/' + l2

            if index_key in index_dict:
                content_str = dict_to_text(l2_path)
                content_str += ',' + index_dict[index_key]+ '\n'
                writer.writelines(content_str)

with open('./email_data/process01', 'w', encoding='utf-8') as writer:
    for l in list0:
        file_path = './email_data/process01_' + l

        print('合并文件', file_path)

        with open(file_path,  encoding='utf-8') as file:
            for line in file:
                writer.writelines(line)

end_time = time.time()

print('数据处理结束,共用时%.2f' % (end_time - start_time))
