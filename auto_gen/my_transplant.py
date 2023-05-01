import re
gimfile = r"D:\Alluser\Program Files (x86)\BIMBase KIT 2022\PythonScript\python-3.7.9-embed-amd64\Lib\site-packages\pyp3d\gim.py"
# -*- coding: UTF-8 -*-

f = open(gimfile, "r", encoding="UTF8")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法

a = re.match("abc", "abcabc")
b = re.match("abc", "ab cabc")


a0 = re.match("123", "abcabc")
b = re.match("abc", "ab cabc").group()

if a:
    print()

if a0:
    print()

# 整理提取头文件名
last = ""
while line:
    line = f.readline()
    note = re.findall("<!--", line)
    if len(note) != 0:
        last = re.sub(r"#", "//", line)
        # print(last, end = '') #

    name = re.findall("class ", line)
    if len(name) != 0:
        # iter=re.finditer("class",line)
        name1 = re.sub(r"class ", "", line)
        name2 = re.sub(r"\(GimGeBaseElement\)", "", name1)
        name3 = re.sub(r"#", "//", name2)
        name4 = re.sub(r":     \n", ".h\"    ", name3)
        print("#include \"" + str(name4)+str(last), end='')
        # print(last, end = '')

f.close()
