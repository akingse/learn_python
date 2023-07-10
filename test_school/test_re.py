import re

# # 1.单字符匹配打印----match()方法，group()方法
text = 'python'
reslut = re.match('py', text)
# 结果存储在一个Object对象里，使用group打印
print(reslut.group())

# # 2.'.'匹配任意字符,但无法匹配换行符'\n'
# text = '_1python'
# reslut = re.match('.', text)
# print(reslut.group())

# # 3.'\d'只匹配数字
# text = '1python'
# reslut = re.match('\d', text)
# print(reslut.group())

# # 4.'\D'除数字之外都可以匹配
# text = '_python'
# reslut = re.match('\D', text)
# print(reslut.group())

# # 5.'\s'只匹配空白字符'\n'、'\r'、'\t'、空格
# text = '\t_python'
# reslut = re.match('\s', text)
# print(reslut.group())

# # 6.'\w'匹配小写a-z，大写A-Z，数字以及下划线,除下划线外其他符号均不匹配
# text = '_python'
# reslut = re.match('\w', text)
# print(reslut.group())

# # 7.'\W'匹配除'\w'能匹配之外的字符
# text = '=python'
# reslut = re.match('\W', text)
# print(reslut.group())

# # 8.'[]'匹配内[]包含的内容，多个条件的任意一个条件满足进行匹配---输出的是p
# text = 'python'
# reslut = re.match('[py]', text)
# print(reslut.group())

# # 9.'*'匹配零次或多次
# num = '156-3234-4234'
# reslut = re.match('[-\d]*', num)
# print(reslut.group())

# # 10. '+'匹配一个或多个，至少匹配一次
# num = '156-3234-4234'
# reslut = re.match('[-\d]+', num)
# print(reslut.group())

# # 11.'[]?'匹配0个或1个
# num = '156-3234-4234'
# reslut = re.match('[-\d]?', num)
# print(reslut.group())

# # 12.'{m}'匹配指定个数(m)
# num = '156-3234-4234'
# reslut = re.match('[\d]{2}', num)
# print(reslut.group())

# # 13.'{m,n}'匹配m到n次，默认匹配最多,保底m次
# num = '156-3234-4234'
# reslut = re.match('[-\d]{2,7}', num)
# print(reslut.group())
