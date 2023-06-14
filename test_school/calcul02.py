
from math import *
# from numpy import *
import os


a=True
b=False

x=(a ^ b)

def fix_e402(self, result): ...
    # (line_index, offset, target) = get_index_offset_contents(result,
    #                                                          self.source)
    # for i in range(1, 100):
    #     line = "".join(self.source[line_index:line_index+i])
    #     try:
    #         generate_tokens("".join(line))
    #     except (SyntaxError, tokenize.TokenError):
    #         continue
    #     break
    # if not (target in self.imports and self.imports[target] != line_index):
    #     mod_offset = get_module_imports_on_top_of_file(self.source,
    #                                                    line_index)
    #     self.source[mod_offset] = line + self.source[mod_offset]
    # for offset in range(i):
    #     self.source[line_index+offset] = ''

a=os.getcwd()
# a=os.getcwdb()
a=os.getenv(a)
# a=os.curdir()


a=range(1)
a=range(0)
a=range(-1)
print(a)
# print(sqrt(complex(-1.1)))

lst=[3,1,2]
lst.sort()
lst

c=1+1j
bl=isinstance(c,complex)
i=abs(c.real)
r=abs(c.imag)
# print(sqrt(4j))

print()

xList=[1,2,3]
for iter in xList:
    iter=2*iter
for i in range(len(xList)):
    xList[i]=2*xList[i]

print(xList)


def fun(bl:bool):
    aList=[1,2,3]
    # bList= aList if bl else aList.reverse()
    # return bList
    # if bl:
    #     return aList
    # else:
    #     aList.reverse()
    #     return aList
    if not bl:
        aList.reverse()
    return aList


print(fun(True))
print(fun(False))
if (a <= 1):
    a != 2

# if(min(a.x,b.x)<=max(c.x,d.x) && min(c.y,d.y)<=max(a.y,b.y)&&min(c.x,d.x)<=max(a.x,b.x) && min(a.y,b.y)<=max(c.y,d.y)) 
# 　　return true;

if a<=1:
    a=1


