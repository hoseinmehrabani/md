import numpy as np
import pandas as pd
# data=np.array(['a','b','c','d','e','f','g','h','u'])
# myseries=pd.Series(data,index=[1,2,3,4,5,6,7,8,9])
# print(myseries)
# data={"first":"ali","sec":"lila","third":"hasan"}
# ser=pd.Series(data,index=['second','third','fourth','fifth'])
# print(ser)
# data_1=pd.Series([16,3,65,33,5,9])
# data_2=pd.Series([16,3,65,33,5,9])
# print(data_1.add(data_2))
# print(data_1.sub(data_2))
# print(data_1.mul(data_2))
# print(data_1.div(data_2))
# print(data_1.pow(data_2))
# data=np.array(['a','b','c','d','e','f','g','h','u'])
# ser=pd.Series(data,index=[5,10,15,20,25,30,35,40])
# print(ser.iloc[3])
# print(ser.loc[20])
# print(ser.iloc[3:6])
# print(ser.loc[20:35])
# mylist=['t','g','k']
# df=pd.DataFrame(mylist,index=['a','b','c'],columns=['ali'])
# print(df)
# data={"name":['ali','matin','king'],"age":[10,20,30],"city":["tehran",'qom','khashan'],"email":['<EMAIL1>','<EMAIL2>','<EMAIL3>']}
# df=pd.DataFrame(data,index=["per1","per2","per3"],columns=mylist)
# print(df.iloc[0:2])
# print(df.loc['per1':'per2','age':'email'])
data={"name":['ali','matin',np.nan,'reza'],"age":[np.nan,20,30,45],"city":["tehran",'qom','khashan',np.nan],"teaching":[np.nan,'python','matlab']}
df=pd.DataFrame(data)
print(df["age"]==30)
print(df['city']=="qom")#culoms
print(df[df.index>1])
print(df[df.colums=="city"])
print(df[df['age']>=20])
print(df.isnull())
print(df.notnull())
print(df[df.notnull()])
print(df[df.isnull()])
print(df.fillna(0))
print(df.fillna('UNDEFINE'))
print(df.dropna(axis=0,how='any',thresh=2,subset=['age','city','teaching'],inplace=False))





