# 自动删除指定后缀的文件
import os
mypath = "D:\Alluser\Program Files (x86)\BIMBase KIT 2022\PythonScript\python-3.7.9-embed-amd64\Lib\site-packages\test_script0\test_re03.py"


def findFile():
    for root, dirs, files in os.walk(mypath):
        for file in files:
            if file.find('.exp') != -1:
                os.remove(root+'/'+file)
            if file.find('.obj') != -1:
                os.remove(root+'/'+file)


if __name__ == '__main__':
    findFile()
