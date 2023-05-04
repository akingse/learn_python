import re
gimName = "GimExFound"
gimName = "GimGeCompositeCaissonFoundation"
# inputPath = r"D:/akingse/BIMBase_SecondaryDev/SecondaryDev_Project/GIM/GimGeBaseModel/"
inputPath = 'D:\\temp\Bim_ElectricalDesign\GIM\GimGeBaseModel\\'
inputFlieH = inputPath + gimName+".h"
inputFlieCPP = inputPath + gimName+".cpp"

outputPath = r"C:/Users/wangqingsheng/Desktop"
outputPath = r'D:\akingse\BIMBaseSDK-Module\BIMBASE-SDK2-Elec\src\ParaGIMExtension\\'
outFileCPP = outputPath + gimName+".cpp"

testFile = r"D:\akingse\BIMBaseSDK-Module\BIMBASE-SDK2-Elec\src\ParaGIMExtension\GimExFound.cpp"
typeList = ["int", "double", "pvector<int>", "pvector<double>", "GeVec3d", "GePoint3d",
            "pvector<GePoint2d>", "pvector<GePoint3d>", "p3d::PString", "wstring"]

with open(testFile, "r", encoding="GB2312") as file:
    text = file.read()
# ----------------------------------cpp------------------------------------

section = '#include "pch.h"\nusing namespace std;\nusing namespace para;\nusing namespace p3d;\nusing namespace BIMBase;\nusing namespace BIMBase::Core;\n\n'
# add construct
section+=gimName
section+='::'
section+=gimName
section+='()\n{\n\tpara::_Para'
section+=gimName
section+='* ptr = para::_Para'
section+=gimName
section+='::get();\n\tif (nullptr == ptr)\n\t\treturn;\n\t_setPrimitive(ptr->_create());\n}\n\n'
section+=gimName
section+='::~'
section+=gimName
section+="()\n{\n}\n\n"



# fl = open(inputFlieH, "r", encoding="GB2312")
# line = fl.readline()
# setFun = dict()
# getFun = dict()
# members = str()
# isPri = False
# while line:
#     line = fl.readline()
#     dllexport = re.findall("GIMGEBASE_API", line)
#     if len(dllexport) != 0:
#         funName = re.sub(r"GIMGEBASE_API", "", line)
#         if len(re.findall(gimName, line)) != 0:  # exclude construct and deconstruct
#             continue
#         if len(re.findall("void", line)) != 0:  # set function
#             funName = re.sub(r"void", "", funName)
#             funName = funName[:-2]  # caution, using re.sub
#             value = re.findall("\(.+?\)", funName)
#             funName = re.sub(value[0], "", funName)
#             funName = re.sub(" |\t|\(|\)", "", funName)
#             setFun[funName] = re.sub("\(|\)", "", value[0])
#         else:  # get function
#             funName = funName[:-2]
#             funName = re.sub("const|\t|\(|\)", "", funName)
#             value, key = funName.split()
#             getFun[key] = value
# fl.close()  # file read finish


# read cpp set&get
fl = open(inputFlieCPP, "r", encoding="GB2312")
line = fl.readline()
setFun = dict()
getFun = dict()
members = str()
isPri = False


tempLine=''
isStore=False

# set
while line:
    line = fl.readline()
    if re.match('void '+gimName+'::set', line) or isStore:
        if not re.match('.*=', line):
            isStore=True
        if re.match('.*=', line) and re.match('void', line):
            line=re.sub('const ','',line)
            words=line.split('::')
            key=words[1].split('(')
            valueT=key[1].split(' ')[0]
            valueV=key[1].split(' ')[1].split(')')[0]
            valueM=key[1].split('{')[1].split('=')[0]
            valueM1=re.sub('[\n\t]', "", valueM)
            setFun[key[0]]=[valueT,valueV,valueM1]
        else:
            if isStore:
                tempLine+=line
            if re.match('.*=', line):
                words=tempLine.split('::')
                key=words[1].split('(')
                valueT=key[1].split(' ')[0]
                valueV=key[1].split(' ')[1].split(')')[0]
                valueM=key[1].split('{')[1].split('=')[0]
                valueM=re.sub('\n|\t', "", valueM)
                setFun[key[0]]=[valueT,valueV,valueM]
                isStore=False
                tempLine=''


fl = open(inputFlieCPP, "r", encoding="GB2312")
line = fl.readline()
tempLine=''
isStore=False
while line:
    line = fl.readline()
    # get
    if re.match('.*'+gimName+'::get', line) or isStore:
        if not re.match('.*return', line):
            isStore=True
        if re.match('.*'+gimName+'::get', line) and re.match('.*return', line):
            words=line.split('::')
            key=words[1].split('(')[0]
            valueT=line.split(' ')[0]
            valueM=line.split(';')[0].split(' ')[-1]
            getFun[key]=[valueT,valueM]
        else:
            if isStore:
                tempLine+=line
            if re.match('.*return', line) and re.match('.*'+gimName, tempLine):
                words=tempLine.split('::')
                key=words[1].split('(')[0]
                valueT=tempLine.split(' ')[0]
                valueM=tempLine.split(';')[0].split(' ')[-1]
                getFun[key]=[valueT,valueM]
                isStore=False
                tempLine=''





# Gim member function
setName='void GimGEONAME::SETNAME(VALUE)\n{\n\tpara::_ParaGimGEONAME* ptr = para::_ParaGimGEONAME::get();\n\tif (nullptr == ptr)\n\t\treturn;\n\t_setPrimitive(ptr->_SETNAME(_getPrimitive(), h1));\n}\n\n'
getName='VALUE GimGEONAME::GETNAME()\n{\n\tpara::_ParaGimGEONAME* ptr = para::_ParaGimGEONAME::get();\n\tif (nullptr == ptr)\n\t\tthrow std::logic_error("_ParaGimGeo::get() error!");\n\treturn ptr->_GETNAME(_getPrimitive());\n}\n\n'
for key in setFun.keys():
    setIter=re.sub('GimGEONAME', gimName, setName)
    setIter=re.sub('SETNAME', key, setIter)
    setIter=re.sub('VALUE', setFun[key][0]+setFun[key][1], setIter)
    section +=setIter
for key in getFun.keys():
    getIter=re.sub('GimGEONAME', gimName, getName)
    getIter=re.sub('GETNAME', key, setIter)
    getIter=re.sub('VALUE', getFun[key][0], setIter)
    section +=setIter

section += "//--------------------------------------------------ToGe--------------------------------------------------\n\n"
headName='ToGeGimNAME::ToGeGimNAME() :\n\tParaPrimitive(typeid(BIMBase::Core::GimNAME))\n'
headName=re.sub('GimNAME', gimName, headName)
section +=headName

# add default para
fl = open(inputFlieCPP, "r", encoding="GB2312")
line = fl.readline()
graphic = list()
isPri = False
while line:
    line = fl.readline()
    if isPri:
        words = line.split()
        members += line
    if len(re.findall("}", line)) != 0:
        break
    if len(re.findall(gimName, line)) == 2:
        isPri = True
section +=members

# add createGeGraphic
section +="\nvoid ToGe"
section+=gimName
section+='::createGeGraphic()\n'
fl = open(inputFlieCPP, "r", encoding="GB2312")
line = fl.readline()
isPri = False

while line:
    line = fl.readline()
    if re.match('.*return graphicsPtr', line):#len(re.findall("return", line)) != 0:
        break
    if isPri:
        # graphic += line
        graphic.append(line)
    if re.match('.*createPhysicalGraphics', line):#
        isPri = True
# process createPhysicalGraphics
graphicStr='{\n\tCore::BPProject* project = Core::BPProject::getActiveProject();\n\tCore::BPModelBase* modelP = project->getActiveModel();\n'
for iter in graphic:
    if (not bool(re.match('.*return', iter))) and (not bool(re.match('{', iter))):
        graphicStr+=iter

section +=graphicStr
section +='}\n'
desName='ToGeGimNAME::~ToGeGimNAME()\n{\n}\n'
desName=re.sub('GimNAME', gimName, desName)
section +=desName

# add Factory set and get
createName='const ParaPrimitive* GimNAMEFactory::_create()\n{\n\tToGeGimNAME* ptr = new ToGeGimNAME();\n\treturn ptr;\n}\n'
createName=re.sub('GimNAME', gimName, createName)
section +=createName

setName='const::para::ParaPrimitive* GimNAMEFactory::_setNAME(const::para::ParaPrimitive* imp, TYPE INVAR)\n{\n\tToGeGimNAME* GeGimNAME = dynamic_cast<ToGeGimNAME*>(const_cast<ParaPrimitive*> (imp));\n\tif (!GeGimNAME)\n\t\treturn imp;\n\tGeGimNAME->MEMBER = INVAR;\n\tconst ParaPrimitive* primitive = dynamic_cast<const ParaPrimitive*>(GeGimNAME);\n\treturn primitive;\n}\n\n'
getName='TYPE GimNAMEFactory::_getNAME(const ::para::ParaPrimitive* imp)\n{\n\tconst ToGeGimNAME* GeGimNAME = dynamic_cast<const ToGeGimNAME*>(imp);\n\tif (!GeGimNAME)\n\t\tthrow std::logic_error("dynamic_cast down-cast error!.");\n\treturn GeGimNAME->MEMBER;\n}\n'
section+=setName
section+=getName

if len(setFun) != len(getFun):
    raise ValueError("seg-get number error")

# sub variable
for key in setFun.keys():
    setIter=re.sub('GimNAME', gimName, setName)
    setIter=re.sub('setNAME', key, setIter)
    setIter=re.sub('TYPE', setFun[key][0], setIter)
    setIter=re.sub('INVAR', setFun[key][1], setIter)
    setIter=re.sub('MEMBER', setFun[key][2], setIter)

section+=setIter
for key in getFun.keys():
    getIter=re.sub('GimNAME', gimName, getName)
    getIter=re.sub('setNAME', key, getIter)
    getIter=re.sub('TYPE', getFun[key][0], getIter)
    getIter=re.sub('MEMBER', getFun[key][1], getIter)
section+=getIter

print(section)
# print(graphicStr)
# exit(0)




# print(section)
# write file
with open(outFileCPP, "w", encoding="GB2312") as fl:
    text = fl.write(section)
