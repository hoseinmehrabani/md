from itertools import groupby

import numpy as np

import pandas as pd
# df=pd.read_csv('file.csv')
# print(df.head())
# print(df.tail())
#read_excel,read_html,to_csv
# print(df.shape)
# print(df.count())
# print(df.values())
# print(df.describe())
# print(df.set_index('Name'))
# print(df.sort_values(by='Name', ascending=False,axis=0,na_position='last',inplace=True))
#
# df_1=pd.DataFrame("name":['ali','hamid','hasan'],"grade":[80,78,55],"qualifation":['low','high','mid'])
# df_2=pd.DataFrame("name":['ali','hamid','hasan'],"grade":[82,90,55],"qualifation":['mid','high','low'])
# df_3=pd.DataFrame("name":['ali','hamid','hasan'],"grade":[88,52,55],"qualifation":['high','low','mid'])
# print(pd.marge(df_1,df_2,on='name'))
# df_1.set_index('qualifation',inplace=True)
# df_2.set_index('qualifation',inplace=True)
# print(df_1.join(df_2,isuffix='_join'))
# merged=pd.merge(df_1,df_2,on='qualifation',how='left')
# merged.set_index('qualifation',inplace=True)
# print(merged)
# merged=pd.merge(df_1,df_2,on='qualifation',how='outer ')
# merged.set_index('qualifation',inplace=True)
# print(merged)
# merged=pd.merge(df_1,df_2,on='qualifation',how='inner')
# merged.set_index('qualifation',inplace=True)
# print(merged)
# df=pd.read_csv("file.csv")
# print(df)
# mygp=df.groupby("Name")
# print(mygp)
# def myfunc(self):
#     return df.loc[self].Test1 >df.loc[self].Test2
# print(groupby(myfunc).groups)
# print(mygp['Test1'].agg(np.mean))
# for name, group in mygp:
#     print("Name")
#     print(group)
# getgp=mygp.get_group("Ali")
# print(getgp)
# df_1=pd.DataFrame("name":['ali','hamid','hasan'],"grade":[80,78,55],"qualifation":['low','high','mid'])
# df_2=pd.DataFrame("eddited":['ali','hamid','hasan'],"grade":[82,90,55],"qualifation":['mid','high','low'])
# print(pd.cancat([df_1,df_2]))
print(pd.to_datetime('2019-06-15 3:55pm'))
pd.to_datetime('2019-06-15 3:55pm')
pd.to_datetime(['2019-06-15 3:55pm', '7/8/2010','oct 1999'])
pd.to_datetime('2/25/10' ,format='%m/%d/%Y')






