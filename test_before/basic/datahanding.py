print()
'''
1.导入
模块导入，函数使用，类
name.fun()
类名.对象 ；math.pi 数据，含参，无参

2.特殊运算符
成员运算符 in; not in (True False)
身份运算符 is; is not (True False) id(x) == id(y)
优先级

3.随机数函数 (.)
choise(seq) 随机选择元素
random() 随机生成实数，范围[0,1)
seed([x]) 改变随机数生成器的种子seed
shuffle(list) 将序列的所有元素随机排序

4.迭代生成器
for i in list/str/tuple/dict
当一个字符类型含有多个字符时，还可以被迭代  # for i in 'abcde':
数字整型迭代，for i in range(a_int):
多维数据类型操作

6. 数据读取
open()
.read()
with open('name','w') as f:
    f.write('data') #不用关闭文件！
'''

'''关键字
import from as def class lambda #头文件
True False None and or not is     #逻辑
for in while break continue     #循环
if elif else pass yield         #选择
try except raise finally with assert #异常
global nonlocal 
del  return

运算符 - 运算符优先级
算术运算符 +-*/ **//% power(,) divmod(,)
比较运算符 <>!=
赋值运算符 (+-*/)=
逻辑运算符 and or not
位运算符 &|~^ <<>>
成员运算符 in; not in
身份运算符 is; is not
'''
# -------------------------------------------------------------------------
'''
5.标准数据类型
type(name)
number（数字）四种：整数、布尔型、浮点数和复数。int() bool() float() complex()
'''
# 只有 bool(0)==False
# print(bool(1+1j));print(bool(-1.2));print(bool('abc')) #True
# True False 判定
'''a=True
a=float(1)
a=int(a)
# b=1+1j #b=complex(1,1)
a,b,c=eval('1+1'),int('2'),float('3')
# print(a,b,c)
# a=int(b)

# if 'a'==True:
# print(0==False and 1==True)

# if 1:
#     print('True')'''
'''
string（字符串） 构成数据的基本元素
操作
+ * repr() del 
切片 [::1]
转换数字 eval() 
连接 .join(t)
分割 .split(' ')，生成列表
判定 .isalnum() .isalpha() .isdigit() .islower() .isnumeric()
'''
str0='this is a python'
# str0.format()
str1=str0.replace(str0[10:16],'world!') #此方法不改变原字符串
# print(max(str0)) #字符串 str 中最大的字母。'y'
print(str1)

list0=str0.split(' ')
# list0.sort() #列表字母排序 #sorted(list0)
print(list0)

'''


list（列表）、
操作：.append() del list[0]
list0=[0,1,2,3] #最好的数据类型
# print(repr(str(list0)))
str0=str(list0) #产生多余空格
tuple（元组）；固定版列表，不可改写操作
方法函数
.clear()  .copy()  .remove(object)  .count(object)
.append(object)
.reverse()
.insert(index,object)
.extend(iterable)
.index()
.pop()
.sort()
.sorted()
'''
list0=[0,1,2,3]


'''

dict（字典）、为统计而生
函数 
len(dict) #keys的个数；str(dict) #按格式 全部转字符串
方法
.clear() 清除 .copy() 浅复制 .fromkeys() 创建同键空值字典  
字典合并 dict1.update(dict2) 把字典dict2的键值对更新到dict1里
.items() 生成键值对元组的 列表
.get(key, default=None) 返回指定键的值，值不在字典中返回default值
.setdefault(key, default=None) 键不存在于字典中，将会添加键并将值设为default
.keys() 返回一个键的迭代器; .values() 返回一个值的迭代器，用list()转为列表
.pop('c','else return') 删除指定键，并返回该值；.popitem() 返回并删除字典中的最后一对键和值(元组)。
.zip(a,b) 打包为元组的 zip object
.sort()方法， 
sorted函数， sorted(iterable, cmp=None, key=None, reverse=False) key是用来进行比较的元素 key=lambda x:x[1] 比较元组的第二个参数

'''
dict0={'a':1,'b':2,'c':3} # 字典类似于，具有特定字符或数字下标（键）的列表
for k in dict0: #迭代器，默认使用键
    pass#print(k,':',dict0[k])
# 两个或更多序列中循环时，可以用 zip() 函数将其内元素一一匹配。
keys0=list(dict0.keys())  #dict_keys(['a', 'b', 'c']) =>['a', 'b', 'c']
values0=list(dict0.values())  #dict_values([1, 2, 3]) =>[1, 2, 3]
print(dict0.items()) #dict_items([('a', 1), ('b', 2), ('c', 3)])
tupli=zip(dict0.keys(),dict0.values())
dict1=dict(zip(range(3),('a','b','c')))

print(tupli)



# for i in dict0.keys(): #for i in list(dict0.keys()):
#     pass#    # print(i,':',dict0[i])
# print(dict0.pop('c','else return')) #弹出
# print(dict0.popitem())
# print(dict0)

dict1=dict([('sape', 4139), ('guido', 4127), ('jack', 4098)]) #新建字典
# dict1=dict(sape=4139, guido=4127, jack=4098)
list1=list(dict1.items()) #[('sape', 4139), ('guido', 4127), ('jack', 4098)]
# print(list1)
students = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
students.sort( key=lambda s: s[0], reverse=False)
print(students)

'''
set（集合）。
集合运算：差-，并|，交&,反交^
'''
# from operator import *
# import operator #cmp()函数
# print(cmp(1,2))
# print(operator.lt(1,2))
# print(operator.eq(1,1))

'''
数学
abs()  divmod()  pow()
max()  min()  sum()  round()

类型转换 type()
bool() int()  float()  complex()
str()  set()  list()  tuple()  dict()
bin()  oct()  hex()

repr() eval()  ord()  chr()  unicode()
reverse()  sorted()  range()	

输入输出
raw_input() input()	 print()  open()  file()
format()
all()  any()
globals()  locals()

迭代 iter() next()
------------------------------
staticmethod()
enumerate()			
isinstance()
basestring()	
execfile()	
issubclass()		
super()

property()	
filter()	
len()	
bytearray()				
unichr()
callable()			
reduce()	
	
frozenset()	
long()	
reload()	
vars()
classmethod()	
getattr()	
map()		
xrange()
cmp()	cmp(x,y) 函数用于比较2个对象，如果 x < y 返回 -1, 如果 x == y 返回 0, 如果 x > y 返回 1。			
zip()
compile()	
hasattr()	
memoryview()		
__import__()
hash()		
delattr()	
help()		
setattr()	
object()	
slice()	
dir()	
id()			exec 内置表达式'''


'''
星号（*）操作符

使用 * 和 ** 向函数传递参数
使用 * 和 ** 捕捉传递至函数的参数
使用 * 接受 keyword-only 参数
使用 * 捕捉元组解包过程中的项
使用 * 将可迭代对象解包至列表/元组
使用 ** 将字典解包至其他字典
'''
