import os, re

# 批量处理文本文件

addr=r"D:\Commun\CODES\desktop-tutorial\learn_record" #一个路径

paths=[]
for root,dirs, files in os.walk(os.path.abspath(addr)): #遍历当前相对路径，可以更改为绝对路径
    for file in files:
        if file[-3:] !=".md": #以.txt结尾的文件
            continue
        paths.append(os.path.join(root,file))


with open (addr+"\\merge_data_01.txt" , "w",encoding="UTF8") as f:
    for iter in paths:
        with open (iter, "r",encoding="UTF8") as f_iter:
            com=f_iter.read()
            f.write(com)


pathlist=[]
import datetime 
today=str(datetime.date.today())
day=today.replace("-","")
print(day)

import pandas as pd

merge_data=pd.DataFrame(columns=['电影名称','上映时间','发行公司','电影导演','电影主演','累计票房(万)'])
# print(merge_data)

rawdata=open(addr+'\\'+pathlist[0],'r',encoding='utf-8') 
line=rawdata.readline() 
lines=rawdata.readlines() 
print(line) 
print(lines)

for file_name in pathlist: 
    rawdata=open(addr+'\\'+file_name,'r',encoding='utf-8') 
    line=rawdata.readline() 
    lines=rawdata.readlines() 
    
# print(line) 
# print(lines)

data_lines=pd.DataFrame(lines)
data_lines.columns=["中国电影数据"]
print(data_lines)



import pandas as pd
import os
 
mypath = r"D:\Alluser\Program Files (x86)\BIMBase KIT 2022\DwgAndT"
files = os.listdir(mypath)
txts = pd.DataFrame()
# for file in files:
#     position = mypath + os.sep + file
#     print(position)
#     data = pd.read_csv(position, sep='\\s+')
#     txts = pd.concat([txts, data])
# txts.to_csv('data003.txt', encoding='gbk', index=False)

