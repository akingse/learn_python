
a = 1
int(a)
print(type(a))

b = a/2
c = a//2  # 整除
d = a*2
d = a**2 #幂

print(b, c)

def example(a, b):
    # return a,b
    return (a, b)
print(type(example(3, 4)))
print('_____________________________________________________')

# 全局变量
a = 3  # strings, tuples, 和 numbers 是不可更改的对象
# 不可变类型：变量赋值 a=5 后再赋值 a=10，这里实际是新生成一个 int 值对象 10，再让 a 指向它，而 5 被丢弃，不是改变a的值，相当于新生成了a。

def change(a):
    a += 1
    return

change(a)
# 传递的只是a的值，没有影响a对象本身。比如在 fun（a）内部修改 a 的值，只是修改另一个复制的对象，不会影响 a 本身。
print(a)
def change(a):
    #  id() 函数来查看内存地址变化
    print(id(a))   # 指向的是同一个对象
    a = 10
    print(id(a))   # 一个新对象
# 调用函数前后，形参和实参指向的是同一个对象（对象 id 相同），在函数内部修改形参后，形参指向的是不同的 id。


a = 1
print(id(a))
change(a)



# -------------------------------------------
def test(*args):
    print(args)
    return args


print(type(test(1, 2, 3, 4)))
a=[1,2,3]
print(type(a))

# 不定长参数
# *args会将参数外包一层元组类型

def fun(*args):
    print(type(args))
    print(len(args))
    print(args)
    if isinstance(args,tuple) and isinstance(args[0],list):
        print('sucess')
        print(args[0][0])

fun(a)



