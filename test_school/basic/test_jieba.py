print()
'''jieba库基本介绍
jieba库概述
jieba是优秀的中文分词第三方库
中文文本需要通过分词获得单个的词语
jieba库提供三种分词模式

jieba库使用说明
jieba分词的三种模式
精确模式、全模式、搜索引擎模式
- 精确模式：把文本精确的切分开，不存在冗余单词
- 全模式：把文本中所有可能的词语都扫描出来，有冗余
- 搜索引擎模式：在精确模式基础上，对长词再次切分   

jieba.cut(s) #精确模式
jieba.cut(s,cut_all=True) #全模式
jieba.cut_for_search(s) #搜索引擎模式
jieba.lcut(s) #精确模式，返回列表
jieba.lcut_for_search(s) #搜索引擎模式，返回列表
jieba.add_word(w) #向分词词典添加新词

'''

import jieba

#-*- coding : utf-8 -*-
# coding: utf-8
def main():
    txt = open("threekingdomes.txt",mode='r',encoding='gb18030').read() #C:\Users\Public\pyproject\0822\three  UTF-8
    words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
    namedict = {}  # 通过键值对的形式存储词语及其出现的次数 #创建 空字典
    for w in words:
        if len(w) == 1:  # 单个词语不计算在内
            continue
        else:
            namedict[w] = namedict.get(w, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
                                # .get(w.0) 获取key的内容，此处得到累加之后的个数，0的作用是设置初始值
    '''
    #字典操作
    赋值
    dict['key']=0 #如果key原来存在的话，会把原来的值替换掉
    dict.setdefault('key',0)  #如果key原来存在的话，就不修改它的值了
    查询
    dict['key']  #直接查询,如果取的key不存在，会报错
    dict.get('key',otherwise) #get()方法,存在返回1，不存在返回None或者自定义。
    '''
    # print(counts[0:10])
    namelist = list(namedict.items())  # 将键值对转换成列表
    # print('字典长度=',len(namelist))
    namelist.sort(key=lambda x: x[1], reverse=True)  # True  根据词语出现的次数进行从大到小排序
    print('前十个=',namelist[0:10])
    for i in range(20):
        word, count = namelist[i]
        print("{0:<5}{1:>5}".format(word, count))
'''关键词
    新建字典 namedict = {}
    统计个数 namedict[w] = namedict.get(w, 0) + 1
    排序 namelist.sort(key=lambda x: x[1], reverse=True)
    .sorted()
    转换为列表 namelist= list(namedict.items())
    '''

# main()
# key=lambda x: x[1]

# -----------------------------------------------
def main(jieba=None): #
    # text = "　　目前已经有不少部哲学史了，我的目的并不是要仅仅在它们之中再加上一部。"
    txt = open("threekingdomes.txt",mode='r',encoding='gb18030').read() #
    text = jieba.lcut(txt)

    item = text.strip('\n\r').split('\t')
    import jieba.analyse
    tags = jieba.analyse.extract_tags(item[0])
    word_lst = []
    for t in tags:
        word_lst.append(t)

    word_dict = {}
    for item in word_lst:
        if item not in word_dict:
            word_dict[item] = 1
        else:
            word_dict[item] += 1
    print(word_dict)
'''def main(): #参考答案
    txt = open("threekingdomes.txt", mode='r', encoding='gb18030').read()
    words = jieba.lcut(txt) #,cut_all=True
    s='丞相' #孔明  诸葛亮  孟德
    num=words.count(s)
    # for word in words:
    #     if word=='孔明':
    #         num+=1
    print(s,'--',num)'''
# main()

s=jieba.lcut("China is a great country") #汉语库
dict={}
# print(s) #字符列表
for i in s: #['China', ' ', 'is', ' ', 'a', ' ', 'great', ' ', 'country']
    # print(dict.get(i, 0),end=' ')
    dict[i]=dict.get(i,0)+1
    # print(dict.get(i, 0))
print(dict)
# for i in s:
#     print(repr(i))
# DictColor = {"seashell":"海贝色","gold":"金色","pink":"粉红色","brown":"棕色", "purple":"紫色","tomato":"西红柿色"}
# print(DictColor.keys())
