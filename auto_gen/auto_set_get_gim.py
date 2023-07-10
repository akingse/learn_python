import os
import stat
# strEncode = 'utf-8'
fileDir = r"C:\Users\wangqingsheng\source\Workspaces\BIMBasePlatform\BIMBase-Elec\BIMBase\BIMBaseSln\BimBaseModel\ParaPrimitive"
fileName = r'\auto_gen_enrol.cpp'


PRODICT = \
    ['GimSubstation',
        # GEO_NAME
        ['BCModSphere',
            ['Radius', '半径', 'double'],
            ['Ori', '球心', 'BPParaVec'],
         ]
     ]

# --------------------------------------------------------------------------------------------------------------
#                                               function region
# --------------------------------------------------------------------------------------------------------------


# 统一成员函数写法
def gen_code_class_member(arg: list) -> str:
    # gen_code_enum
    res = '''\npublic:\n\tenum : long long\n\t{\n'''
    for i in range(len(arg)):
        enumIter = '\t\tenENUM,\n'
        if i != 0:
            enumIter = enumIter.replace('ENUM', arg[i][0])
            res += enumIter
    res += '\t};\n'
    # member
    res += 'private:\n'
    for i in range(len(arg)):
        enumIter = '\tTYPE m_FUN\n'
        if i != 0:
            enumIter = enumIter.replace('TYPE', arg[i][2])
            enumIter = enumIter.replace('FUN', arg[i][0])
            res += enumIter
    # cons = '''public:\n\tGIMGEBASE_API GimGeMODEL();\n\tGIMGEBASE_API ~GimGeMODEL();\n'''
    # cons = cons.replace('MODEL', arg[0])
    # res += cons
    res += 'public:\n'
    for i in range(len(arg)):
        func = '''\tinline void setFUN(const TYPE& IN_FUN)\n\t{ \n\t\tm_FUN = FUN;\n\t}\n\tinline TYPE getFUN() const\n\t{\n\t\treturn m_FUN;\n\t}\n'''
        if i != 0:
            func = func.replace('IN_FUN', arg[i][0].lower())
            func = func.replace('TYPE', arg[i][2])
            func = func.replace('FUN', arg[i][0])
            res += func
    return res


def gen_code_enrol_property(arg: list) -> str:
    res = '''\n//enrol property\nstatic int _enrol_PropertyID = []()->int\n{\n\t__PrimitiveInfor::enrol<_Sphere, BIMBase_Common::BCModSphere>( 0,\n\t\t{\n'''
    for i in range(len(arg)):
        enrolIter = '''\t\t{ GEO_NAME::enENUM_PARA,    {typeid(PARA_TYPE),    { {BPParaLanguage::Chinese, "PARA_CN" }, {BPParaLanguage::English, "PARA_EN" } } } },\n'''
        if i != 0:
            enrolIter = enrolIter.replace('GEO_NAME', arg[0])
            enrolIter = enrolIter.replace('ENUM_PARA', arg[i][0])
            enrolIter = enrolIter.replace('PARA_TYPE', arg[i][2])
            enrolIter = enrolIter.replace('PARA_CN', arg[i][1])
            enrolIter = enrolIter.replace('PARA_EN', arg[i][0])
            res += enrolIter
    res += '\t\t}\n\t);\n\treturn 0;\n}();\n\n'
    return res


def gen_code_enrol_set_get(arg: list) -> str:
    setFun = 'bool BCModNAME_setFUNCTION(BIMBase::Data::BPObject* ptr, const BIMBase::ParaComponent::Gnrc& val)\n{\n\tBIMBase_Common::BCModNAME* model = dynamic_cast<BIMBase_Common::BCModNAME*>(ptr);\n\tif (!(ptr && model && val.is<TYPEINDEX>()))\n\t\treturn false;\n\tmodel->setFUNCTION(val.as<TYPEINDEX>());\n\treturn true;\n}\n'
    getFun = 'BIMBase::ParaComponent::Gnrc BCModNAME_getFUNCTION(BIMBase::Data::BPObject* ptr)\n{\n\tBIMBase_Common::BCModNAME* model = dynamic_cast<BIMBase_Common::BCModNAME*>(ptr);\n\tif (!(ptr && model))\n\t\treturn {};\n\treturn model->getFUNCTION();\n}\n'
    enrolFunSet = '\tenrolInterfaceThirdparty(typeid(BIMBase_Common::BCModNAME), BPPropertyID(BCModNAME::enFUNCTION), BCModNAME_setFUNCTION);\n'
    enrolFunction = '//unified set and get\n'
    enrolName = '\nstatic int _enrol_BCModNAME = []()->int\n{\n'
    enrolName = enrolName.replace('BCModNAME', arg[0])
    for i in range(len(arg)):
        if i != 0:
            setFunIter = setFun.replace('BCModNAME', arg[0])
            setFunIter = setFunIter.replace('FUNCTION', arg[i][0])
            setFunIter = setFunIter.replace('TYPEINDEX', arg[i][2])
            getFunIter = getFun.replace('BCModNAME', arg[0])
            getFunIter = getFunIter.replace('FUNCTION', arg[i][0])
            enrolFunIter = enrolFunSet.replace('BCModNAME', arg[0])
            enrolFunIter = enrolFunIter.replace('FUNCTION', arg[i][0])
            if (arg[i][2] == 'BPParaVec'):
                getFunIter = getFunIter.replace(
                    'return m', 'return BPParaVec(m')
                getFunIter = getFunIter.replace('();', '());')
            enrolFunction += setFunIter
            enrolFunction += getFunIter
            enrolName += enrolFunIter  # set
            enrolFunIter = enrolFunIter.replace('set', 'get')#copy
            enrolName += enrolFunIter  # get
    enrolName += '\treturn 0;\n}();\n'
    return enrolFunction+enrolName


if __name__ == '__main__':
    # auto script genarate codes begin
    insertWord = 'insertWord'
    content = ''
    with open(fileDir+fileName, 'r') as file:
        content += file.read()
    res = ''
    # res += gen_code_class_member(PRODICT[1]) #生成类的头文件
    res += gen_code_enrol_property(PRODICT[1])  # 注册属性propertyID
    # res += gen_code_enrol_set_get(PRODICT[1])  # 注册统一set get
    # print(res)
    # if os.path.exists(fileDir+fileName): #auto create
    #     os.chmod(fileDir+fileName, stat.S_IWRITE)
    with open(fileDir+fileName, 'w', encoding='GB2312') as file:
        parts = content.split(insertWord)
        # insert mode
        # file.write(parts[0]+insertWord+res+parts[1])

    with open(fileDir+fileName, 'a', encoding='GB2312') as file:  # a : append mode
        file.write(res)


