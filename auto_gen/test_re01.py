import re

# 读取文件，批量处理代码


strEncode = 'utf-8'
# fileName = 'C:/Users/Aking/source/repos/para3.0.1/BPParaComponent/ParaPrimitive/GeoCube.h'
# with open(fileName, 'r', encoding=strEncode) as f:
#     content = f.read()
#     print()


NAME = 'Sphere'
GEONAME = 'Geo'+NAME
fileName = 'C:/Users/Aking/source/repos/para3.0.1/BPParaComponent/ParaPrimitive/'+GEONAME+'.h'


PRODICT = {
    'Color': 'BPParaColor',
    'Material': 'BPParaMaterial',
    # custom
    'Length': 'double',
    'Width': 'double',
    'Height': 'double',
}

# -----------------------------------------------------------------------------------------------
#                                              h
# -----------------------------------------------------------------------------------------------
fileOriginH = ''
# head
fileOriginH1 = '#pragma once\nclass '+GEONAME + \
    ' :\n    public BPGeometricPrimitive\n{\npublic:\n    enum : short\n    {\n'
fileOriginH += fileOriginH1
# enum
fileOriginH2 = ''
for key in PRODICT:
    fileOriginH2 += '        '+'en'+NAME+key+',\n'
fileOriginH += fileOriginH2
# export
fileOriginH1 = '    };\n    __declspec(dllexport) ' + \
    GEONAME+'();\n    __declspec(dllexport) ~'+GEONAME+'();\n'
fileOriginH += fileOriginH1
# set&get
fileOriginH3 = ''
for key in PRODICT:
    fileOriginH3 += '    inline '+PRODICT[key] + \
        ' get'+key+'() const\n    {\n        return getPropertyValue<' + \
        PRODICT[key]+'>(BPPropertyID(en'+NAME+key+'));\n    }\n'
    # using const refer
    fileOriginH3 += '    inline void set'+key + \
        '(const '+PRODICT[key] + \
        '& val)\n    {\n        setPropertyValue({ { BPPropertyID(' + \
        NAME+key+'), val} });\n    }\n'
fileOriginH += fileOriginH3
fileOriginH += '};\n'

print(fileOriginH)
# with open(fileName, "w", encoding=strEncode) as f:  # new file
#     f.write(fileOriginH)
