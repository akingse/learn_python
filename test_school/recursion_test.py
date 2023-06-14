
def recursion(n):
    v = n//2 # 地板除，保留整数
    # print(v) # 每次求商，输出商的值
    if v==0:
        ''' 当商为0时，停止，返回Done'''
        return 'Done'
    v = recursion(v) # 递归调用，函数内自己调用自己
# print(recursion(10))



# 1！+2！+3！+4！+5！+...+n!
def factorial(n):
    ''' n表示要求的数的阶乘 '''
    if n==1:
        return n # 阶乘为1的时候，结果为1,返回结果并退出
    n = n*factorial(n-1) # n! = n*(n-1)!
    return n  # 返回结果并退出
res = factorial(5) #调用函数，并将返回的结果赋给res
print(res) # 打印结果


ls=[]
ls.extend(0,2)
print(ls)