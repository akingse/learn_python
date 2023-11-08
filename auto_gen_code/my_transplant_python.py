import re
inputPath = 'D:\\akingse\BIMBasePlatform\BIMBASE-SDK2\BIMBASE\Source\BPParametricPython\\test_script1\interpret.py'
outputPath = 'D:\\akingse\BIMBasePlatform\BIMBASE-SDK2\BIMBASE\Source\BPParametricPython\\test_script1\cpp_fun.py'

# C++ python 语言翻译

# 翻译python函数到cpp
# 限定4space缩进
# 函数名需要完全统一

subDict = dict()
subDict['float'] = 'double'
subDict['str'] = 'std::string'
subDict['list'] = 'std::vector<>'
subDict['Vec2'] = ''
subDict['Vec3'] = ''
subDict['GeVec2d'] = ''
subDict['GeVec3d'] = ''
subDict['append'] = 'push_back'


def get_sentence_type() -> str:
    return 'DEF_FUN'  # is_function_upper_camel_case
    return 'IF_ELSE'
    return 'FOR_RANGE'
    return 'FOR_ITER'
    return 'THREE_ORDER'
# def is_three_orders_expression(expre:str)->str: #转三目表达式
#     # words=expre.split()
#     return True if re.match('.*if',expre) and re.match('.*else',expre) else False

    ...


def using_function_upper_camel_case(py_name: str) -> str:  # 使用大驼峰命名法则
    camelName = str()
    for i in range(len(py_name)):
        if (py_name[i] == '_') and (not py_name[i+1].isupper()):
            upWord = py_name[i+1].upper()
            camelName += upWord
        else:
            if not (py_name[i-1] == '_'):
                camelName += py_name[i]
    return camelName


def using_three_orders_expression(expre: str) -> str:  # 转三目表达式
    words = expre.split('else')
    no = words[1]
    ori = words[0].split('if')
    yes = ori[0].split()[-1]
    choose = ori[1]
    if re.match('.*return', ori[0]):
        yes = ori[0].split('return')[1]
    if re.match('.*=', ori[0]):
        yes = ori[0].split('=')[1]
    head = re.sub(yes, '', ori[0])
    return head+choose+yes+':'+no


def is_code_not_comment(sentence):
    if len(re.findall('\'\'\'|\"\"\"', sentence)) != 0:
        return False
    words = sentence.split('#')[0]
    if re.match('.*\w', words):
        return True
    return False

# 函数需要按规定写法书写


def transfer_python_to_cpp():
    section = str()
    rank = 0
    recd = 1
    fl = open(inputPath, "r", encoding="utf-8")
    line = fl.readline()
    section += line
    while line:
        line = fl.readline()
        if re.match(4*(rank+1)*' ', line) and rank == recd-1:
            section += rank*'\t'
            section += '{\n'
            rank += 1
            recd += 1
        if not re.match(4*rank*' ', line):  # and rank!=0:
            space = 0
            for iter in line:
                if iter == ' ':
                    space += 1
            retract = space//4
            for i in range(rank-retract):
                section += (rank-i-1)*'\t'
                section += '}\n'
                i += 1
            rank = retract
            recd = retract+1

        # if re.match(8*' ',line) and rank==1:
        #     section+='\t{\n'
        #     rank+=1
        # if not re.match()
        if is_code_not_comment(line):
            if re.match('.*#', line):  # with #
                line = re.sub(' #', '; #', line)
            else:
                line = re.sub('\n', ';\n', line)

        section += line
    print(section)
    return section

# def using_symbol_format(code)


if __name__ == "__main__":
    transfer_python_to_cpp()

    name = '_is_float_zero'
    name = ' int a=0   #bl = True if (abs(num) < eps) else False'
    bl = is_code_not_comment(name)
    if re.match('.*#', name):  # with #
        line = re.sub('#', '; #', name)
    is_code_not_comment(name)
    cpp = using_three_orders_expression(name)
    exit(0)

    '''
    注释问题 全局替换，#和' ''
    三目表达式
    缩进问题
    关键词替换
    处理 if
    处理 for iter in , for i in range
    
    '''
