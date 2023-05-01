import os, re

# 批量处理文本文件

addr=r"D:\Commun\CODES\desktop-tutorial\learn_record" #一个路径

paths=[]
for root,dirs, files in os.walk(os.path.abspath(addr)): #遍历当前相对路径，可以更改为绝对路径
    for file in files:
        if file[-3:] !=".txt": #以.txt结尾的文件
            continue
        paths.append(os.path.join(root,file))


with open (addr+"\\merge_data_01.txt" , "w",encoding="UTF8") as f: #新建文件
    for iter in paths:
        with open (iter, "r",encoding="UTF8") as f_iter:
            com=f_iter.read()
            f.write(com)

