from distutils.log import error
import re
gimName = "GimExFound"
gimName = "GimGeCompositeCaissonFoundation"
inputPath = r"D:/akingse/BIMBase_SecondaryDev/SecondaryDev_Project/GIM/GimGeBaseModel/"
inputFlieH = inputPath + gimName+".h"

outputPath = r"C:/Users/wangqingsheng/Desktop"
outputPath = r'D:\akingse\BIMBaseSDK-Module\BIMBASE-SDK2-Elec\src\ParaGIMExtension\\'
outFileH = outputPath + gimName+".h"

testFile = r"D:\akingse\BIMBaseSDK-Module\BIMBASE-SDK2-Elec\src\ParaGIMExtension\GimExFound.h"
typeList = ["int", "double", "pvector<int>", "pvector<double>", "GeVec3d", "GePoint3d",
            "pvector<GePoint2d>", "pvector<GePoint3d>", "p3d::PString", "wstring"]

# ----------------------------------h------------------------------------
section = "pragma once\nnamespace BIMBase\n{\n\tnamespace Core\n\t{\n\t\tclass "
section += gimName
section += " :BIMBase::Core::GimGeBaseElement\n\t\t{\n\t\tpublic:\n"

fl = open(inputFlieH, "r", encoding="GB2312")
line = fl.readline()
setFun = dict()
getFun = dict()
members = str()
isPri = False
while line:
    line = fl.readline()
    dllexport = re.findall("GIMGEBASE_API", line)
    if len(dllexport) != 0:
        section += "\t\t"
        funName = re.sub(r"GIMGEBASE_API", "", line)
        section += funName
        if len(re.findall(gimName, line)) != 0:  # exclude construct and deconstruct
            # print(line)
            continue
        if len(re.findall("void", line)) != 0:  # set function
            funName = re.sub(r"void", "", funName)
            funName = funName[:-2]  # caution, using re.sub
            value = re.findall("\(.+?\)", funName)
            funName = re.sub(value[0], "", funName)
            funName = re.sub(" |\t|\(|\)", "", funName)
            setFun[funName] = re.sub("\(|\)", "", value[0])
        else:  # get function
            funName = funName[:-2]
            funName = re.sub("const|\t|\(|\)", "", funName)
            value, key = funName.split()
            getFun[key] = value
    if len(re.findall("private", line)) == 1:
        isPri = True
    if isPri:
        words = line.split()
        for iter in words:
            if (iter in typeList):
                members += "\t"
                members += line
    if len(re.findall("};", line)) != 0:
        break
fl.close()  # file read finish

section += "\t\t};\n\t}\n}\n\n"
section += "namespace para\n{\n\tclass _Para"
section += gimName
section += "\n\t{\n\t\tfriend class BIMBase::Core::"
section += gimName
section += ";\n\tprotected:\n\t\tvirtual const::para::ParaPrimitive* _create() = 0;\n"
if len(setFun) != len(getFun):
    raise ValueError("seg-get number error")

# _Para virtual
for key in setFun.keys():
    section += "\t\tvirtual const::para::ParaPrimitive* _"
    section += key
    section += "(const::para::ParaPrimitive* imp, "
    section += setFun[key]
    section += ") = 0;\n"
for key in getFun.keys():
    section += "\t\tvirtual "
    section += getFun[key]
    section += " _"
    section += key
    section += "(const::para::ParaPrimitive* imp) = 0;\n"

section += "\t\t__declspec(dllexport) static void set(_Para"
section += gimName
section += " * imp);\n"
section += "\tprivate:\n\t\tstatic _Para"
section += gimName
section += " * sm_imp;\n\t\tstatic _Para"
section += gimName
section += " * get();\n\t};\n}\n\n"
section += "//--------------------------------------------------ToGe--------------------------------------------------\n\n"
section += "namespace para\n{\n\tclass ToGe"
section += gimName
section += ":\n\t\tpublic BIMBase::Core::GimGeBaseElement, \n\t\tpublic para::ParaPrimitive\n\t{\n\tpublic:\n\t\tfriend class BIMBase::Core::GimGeBaseElement;\n"
section += "\t\tToGe"
section += gimName
section += "();\n\t\t~ToGe"
section += gimName
section += "();\n"
# add private members
section += members

section += "\t\tvoid createGeGraphic();\n\t};\n\n\tclass "
section += gimName
section += "Factory :public _Para"
section += gimName
section += "\n\t{\n\tprotected:\n\t\tconst ParaPrimitive * _create() override; \n"
# Factory override
for key in setFun.keys():
    section += "\t\tconst::para::ParaPrimitive* _"
    section += key
    section += "(const::para::ParaPrimitive* imp, "
    section += setFun[key]
    section += ") override;\n"
for key in getFun.keys():
    section += "\t\t"
    section += getFun[key]
    section += " _"
    section += key
    section += "(const::para::ParaPrimitive* imp) override;\n"
section += "\t};\n}\n"


# print(section)
# write file
with open(outFileH, "w", encoding="GB2312") as fl:
    text = fl.write(section)
