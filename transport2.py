# coding:UTF-8import pandas as pdfrom sklearn import preprocessingimport numpy as npfrom keras.utils import to_categoricaldata = pd.DataFrame(pd.read_csv('IO/tran_attr.csv',                                usecols=['A', 'B', 'C', 'D1', 'D2', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'F11', 'F12', 'F13',                                         'F14', 'F21', 'F22', 'F23', 'F24','F25', 'F26', 'F31', 'F32', 'F33', 'F35', 'G', 'H']))# 'D3' has no data# 'F34' all 1163 0sdig_cols=['A', 'B', 'D1', 'D2', 'D4', 'D5', 'E2', 'E3', 'E4', 'F11', 'F12', 'F13',          'F14', 'F21', 'F22', 'F23', 'F24','F25','G' ]str_cols=[ 'C', 'E1','H'] # transformed to one-hotfill_dig_cols=['F26','F31','F32','F33','F35'] # F26 fill with average, else fill with '0'def count(object_name):    counts = data[object_name].value_counts()    quants = counts.values    print('----' + object_name + '-----')    print('sum:   %d'  %sum(quants))    print(counts)    print('\r')    return countsdef average(object_name):    sum = 0    cou = 0    for i in data[object_name]:        if not (i != i):            cou = cou + 1            sum = sum + i    print(object_name + '平均值为：%f' % (sum / cou))    return (sum / cou)def normalization(object_name):    dif = max(data[object_name]) - min(data[object_name])    aver = average(object_name)    data[object_name] = data[object_name].apply(lambda x: (x - aver) / dif)print(data.info())for i in fill_dig_cols:    count(i)# F26 填充平均值data['F26'] = data['F26'].fillna(average('F26'))# F31 F32 F33 F35 填充 0for i in set(fill_dig_cols).difference(set('F26')):    data[i] = data[i].fillna(0)for i in fill_dig_cols:    normalization(i)for i in dig_cols:    normalization(i)def zip_(object_name):    coun = count(object_name)    return dict(zip(coun.keys(), list(range(len(coun.keys())))))def label_to_int(object_name):    a = zip_(object_name)    data[object_name] = data[object_name].apply(lambda x: a[x] )for i in str_cols:   label_to_int(i)   encoded = to_categorical(data[i])   encoded = pd.DataFrame(encoded)   data = pd.concat([data, encoded], axis=1)   for i in str_cols:    del data[i]pd.DataFrame.to_csv(data, 'IO/after.csv', index=None)# 完成空值填充、归一化, 将C、E1、H转化为one-hot，并且删除原来的列