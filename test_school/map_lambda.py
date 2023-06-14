a = [1, 2, ['A', 'B']]
# print(a)
b = 2
# print('a={}'.format(a))


# -------------------------------------

# lambda函数(匿名函数)
# 形式# lambda argument_list:expersion
# argument_list是参数列表，它的结构与Python中函数(function)的参数列表是一样的
# expression是一个关于参数的表达式，表达式中出现的参数需要在argument_list中有定义，并且表达式只能是单行的。

lambda x:x**2

squa=lambda x:x**2

def function(a,b):...
def function(a=1,b=2):...
def function(*args):...
def function(**kwargs):...
def function(a,b=1,*args):...

# 直接赋给一个变量，然后再像一般函数那样调用
c=lambda x,y,z:x*y*z
c(2,3,4)

# 在函数后面直接传递实参
(lambda x:x**2)(3)

# 将lambda函数作为参数传递给其他函数比如说结合map、filter、sorted、reduce等一些Python内置函数使用
filter(lambda x:x%3==0,[1,2,3,4,5,6])
squares = map(lambda x:x**2,range(5))

# map 映射，一一对应
# map() 会根据提供的函数对指定序列做映射。
# 第一个参数 function 以参数序列中的每一个元素调用 function 函数，返回包含每次 function 函数返回值的新列表。

# f = lambda x: 'big' if x > 100 else 'small'
a=101
f = lambda x: 100 if x > 100 else x
# a=f(101)
f(101)
# print(a)
# print(f(101))
def square(x) :            # 计算平方数
    return x ** 2

map(square, [1,2,3,4,5])   # 计算列表各个元素的平方

list(map(lambda x: x ** 2, [1, 2, 3, 4, 5]))  # 使用 lambda 匿名函数

# 提供了两个列表，对相同位置的列表数据进行相加
list(map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10]))


# ----------------------------------------------------------------

print([i for i in range(5)])
# 表达式[i for i in range(1,10)]，这种表达式称为列表解析（List Comprehensions）
# 列表解析式是将一个列表（实际上适用于任何可迭代对象）转换成另一个列表的工具。在转换过程中，可以指定元素必须符合一定的条件，才能添加至新的列表中，这样每个元素都可以按需要进行转换。

# 每个列表解析式都可以重写为 for 循环，但不是每个 for 循环都能重写为列表解析式，列表解析比 for 更精简，运行更快。

# for 循环
li = []
for i in range(1, 11):
	li.append(i*2)

# 列表解析式
li = [i*2 for i in range(1, 11)]

# 筛选条件
li = [i*2 for i in range(1, 11) if i*2 > 10]
# 嵌套循环
li1 = ['A', 'B', 'C']
li2 = ['1', '2', '3']
li3 = []
for m in li1:
	for n in li2:
		li3.append((m,n))


li1 = ['A', 'B', 'C']
li2 = ['1', '2', '3']
li3 = [(m,n) for m in li1 for n in li2]


print('')

# -------------------------------------------------------------
a=[1,2,3]
d=[1,1,1]


print(list(map(lambda x: x ** 2, [1, 2, 3, 4, 5])))
print(list(map(lambda x: a+x*d, range(2))))
print(map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10]))
# print(A)
