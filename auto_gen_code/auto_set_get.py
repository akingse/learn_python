import os
import stat
strEncode='utf-8'
filDir=r"C:\Users\wangqingsheng\source\Workspaces\BIMBasePlatform\BIMBase-Elec\BIMBase\BIMBaseSln\BimBaseModel\ParaPrimitive"
outFileName=r'\auto_gen_enrol.cpp'
# filDir+='ParaInterfaceEnrol.cpp'
# with open(filename,'r') as f:
#     content=f.read()

PRODICT=[  # auto judge set/get

['BCModSphere','getRadius', 'double', 'GeoSphere::enSphereRadius'], 
['BCModSphere','setOri', 'BPParaVec', 'GeoSphere::enSphereCenter'], 


# ['BCModStdCone','setTopPoint', 'BPParaVec', 'GeoCone::enConeTopPoint'], 
# ['BCModStdCone','getBottomCenPoint', 'BPParaVec', 'GeoCone::enConeBottomPoint'],
# ['BCModStdCone','getRadius', 'double', 'GeoCone::enConeRadius'], 
# ['BCModStdCone','getHeight', 'double', 'GeoCone::enConeHeight'], 

# ['BCModArcType','getXRadius', 'double', 'GeoArc::enArcXRadius'], 
# ['BCModArcType','getYRadius', 'double', 'GeoArc::enArcYRadius'], 
# ['BCModArcType','getSweep', 'double', 'GeoArc::enArcScope'], 
# ['BCModArcType','setThetaStart', 'double', 'GeoArc::enArcThetaStart'], 

]

setFun='bool BCModNAME_setFUNCTION(BIMBase::Data::BPObject* ptr, const BIMBase::ParaComponent::Gnrc& val)\n{\n\tBIMBase_Common::BCModNAME* model = dynamic_cast<BIMBase_Common::BCModNAME*>(ptr);\n\tif (!(ptr && model && val.is<TYPEINDEX>()))\n\t\treturn false;\n\tmodel->setFUNCTION(val.as<TYPEINDEX>());\n\treturn true;\n}\n'
getFun='BIMBase::ParaComponent::Gnrc BCModNAME_getFUNCTION(BIMBase::Data::BPObject* ptr)\n{\n\tBIMBase_Common::BCModNAME* model = dynamic_cast<BIMBase_Common::BCModNAME*>(ptr);\n\tif (!(ptr && model))\n\t\treturn {};\n\treturn model->getFUNCTION();\n}\n'
enrolFun='\tenrolInterfaceThirdparty(typeid(BIMBase_Common::BCModNAME), BPPropertyID(PROPERTYID), BCModNAME_setFUNCTION);\n'
enrolName='\nstatic int _enrol_BCModNAME = []()->int\n{\n'
enrolName=enrolName.replace('BCModNAME',PRODICT[0][0])

ALL_FUNCTION=[]
ALL_ENROL=[]

# set
for iter in PRODICT:
    # isSet
    sfun=iter[1]
    tfun=sfun[3:]
    setFunIter=setFun.replace('BCModNAME',iter[0])
    setFunIter=setFunIter.replace('FUNCTION',tfun)
    setFunIter=setFunIter.replace('TYPEINDEX',iter[2])
    getFunIter=getFun.replace('BCModNAME',iter[0])
    getFunIter=getFunIter.replace('FUNCTION',tfun)
    enrolFunIter=enrolFun.replace('BCModNAME',iter[0])
    enrolFunIter=enrolFunIter.replace('FUNCTION',tfun)
    enrolFunIter=enrolFunIter.replace('PROPERTYID',iter[3])
    if (iter[2]=='BPParaVec'):
        getFunIter=getFunIter.replace('return m','return BPParaVec(m')
        getFunIter=getFunIter.replace('();','());')
    ALL_FUNCTION.append(setFunIter+getFunIter)
    ALL_ENROL.append(enrolFunIter)
    # print()

if os.path.exists(filDir+outFileName):
    os.chmod(filDir+outFileName, stat.S_IWRITE)
with open(filDir+outFileName,'w',encoding='GB2312') as f:
    for iter in ALL_FUNCTION:
        f.write(iter)
    f.write(enrolName)
    for iter in ALL_ENROL:
        f.write(iter)
    f.write('\treturn 0;\n}();\n')


