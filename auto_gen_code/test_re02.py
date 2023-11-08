import re
strEncode = 'GB2312'  # 'utf-8' # vs必须使用2312
# fileName = r'C:/Users/Aking/source/repos/para3.0.1/BPParaComponent/ParaPrimitive/GeoCube.cpp'  # 读取文件
# with open(fileName, 'r', encoding='gb2312') as f:
#     content = f.read()
#     print()

'''
批量处理代码

single:
cube sphere cone

line
point segment arc splineCurve
Line Section
Sweep Loft
'''

# AUTO = ['Cube', 1]
# AUTO = ['Sphere', 2]
# AUTO = ['Cone', 3]
# AUTO = ['Point', 4]
# AUTO = ['Segment', 5]
# AUTO = ['Arc', 6]
# AUTO = ['SplineCurve', 7, '样条线']
# AUTO = ['Line', 8]
# AUTO = ['Section', 9, '面']
# AUTO = ['Combine', 11]
# AUTO = ['Fusion', 12, '融合']
# AUTO = ['Intersect', 13, '布尔交']
# AUTO = ['Sweep', 14, '扫掠体']
# AUTO = ['Loft', 15, '放样体']
# AUTO = ['Text', 16, '文字']
# AUTO = ['Array', 17, '阵列']
AUTO = ['Box', '盒体']


PRODICT = {
    'Repre': ['Geo'+AUTO[0], AUTO[1], AUTO[0]],  #
    'Color': ['BPParaColor', '颜色', 'Color'],
    'Material': ['BPParaMaterial', '材质', 'Material'],

    # custom
	'BottomOrigin': ['BPParaVec', '底部原点', 'BottomOrigin'],
	'TopOrigin': ['BPParaVec', '顶部原点', 'TopOrigin'],
	'VectorX': ['BPParaVec', 'x方向的向量', 'VectorX'],
	'VectorY': ['BPParaVec', 'y方向的向量', 'VectorY'],
	'BottomX': ['double', '底部x方向上的长度', 'BottomX'],
	'BottomY': ['double', '底部y方向上的长度', 'BottomY'],
	'TopX': ['double', '顶部x方向的向量', 'TopX'],
	'TopY': ['double', '顶部y方向的向量', 'TopY'],
	'Capped': ['bool', '端面是否封闭', 'Capped'],


    # 'CtrlPoints': ['std::vector<BPParaVec>', '元素', 'CtrlPoints'],
    # 'DisNum': ['long long', '离散数', 'DisNum'],
    # 'OrderCoef': ['long long', '阶次', 'OrderCoef'],
    # 'SplineType': ['std::string', '类型', 'SplineType'],

    # 'ArrayType': ['para::ParaArrayType', '阵列类型', 'ArrayType'],
    # 'ArrayLinear': ['para::ArrayLinear', '线性阵列', 'ArrayLinear'],
    # 'ArrayCircle': ['para::ArrayCircle', '环形阵列', 'ArrayCircle'],
    # 'CustomMatrix': ['std::vector<BPParaTransform>', '自定义矩阵', 'CustomMatrix'],

    # 'String': ['std::string', '字符串', 'String'],
    # 'FontStyle': ['para::ParaFontStyle', '文字样式', 'FontStyle'],

    # 'FontName': ['std::string', '字体名', 'FontName'],
    # 'FontNameBig': ['std::string', '字体名Big', 'FontNameBig'],
    # 'FontTypeBig': ['std::string', '字体类型Big', 'FontTypeBig'],
    # 'FontSize': ['double', '字体大小', 'FontSize'],
    # 'ScaleHorz': ['double', '水平缩放', 'ScaleHorz'],
    # 'ScaleVert': ['double', '竖直缩放', 'ScaleVert'],

    # 'SectionList': ['std::vector<BPGeometricPrimitive>', '多截面', 'SectionList'],
    # 'Smooth': ['bool', 'Mesh', 'Smooth'],

    # 'Section': ['BPGeometricPrimitive', '截面', 'Section'],
    # 'Trajectory': ['BPGeometricPrimitive', '路径', 'Trajectory'],
    # 'Smooth': ['bool', 'Mesh', 'Smooth'],

    # 'PointStart': ['BPParaVec', '起点', 'PointStart'],
    # 'PointEnd': ['BPParaVec', '终点', 'PointEnd'],
    # 'Norm': ['double', '长度', 'Norm'],
    # 'Vec': ['BPParaVec', '方向', 'Vec'],
    # 'PointStartX': ['double', '起点x', 'PointStartX'],
    # 'PointStartY': ['double', '起点y', 'PointStartY'],
    # 'PointStartZ': ['double', '起点z', 'PointStartZ'],
    # 'PointEndX': ['double', '终点x', 'PointEndX'],
    # 'PointEndY': ['double', '终点y', 'PointEndY'],
    # 'PointEndZ': ['double', '终点z', 'PointEndZ'],

    # 'BottomPoint': ['BPParaVec', '底面圆心', 'BottomPoint'],
    # 'BottomRadius': ['double', '底面半径', 'BottomRadius'],
    # 'TopPoint': ['BPParaVec', '底面圆心', 'TopPoint'],
    # 'TopRadius': ['double', '底面半径', 'TopRadius'],
    # 'SegmentNorm': ['double', '轴线长度', 'SegmentNorm'],
    # 'SegmentVec': ['BPParaVec', '轴线方向', 'SegmentVec'],
    # 'BottomPointX': ['double', '底面圆心x', 'BottomPointX'],
    # 'BottomPointY': ['double', '底面圆心y', 'BottomPointY'],
    # 'BottomPointZ': ['double', '底面圆心z', 'BottomPointZ'],
    # 'TopPointX': ['double', '顶面圆心x', 'TopPointX'],
    # 'TopPointY': ['double', '顶面圆心y', 'TopPointY'],
    # 'TopPointZ': ['double', '顶面圆心z', 'TopPointZ'],

    # 'Point': ['BPParaVec', '点', 'Point'],
    # 'PointX': ['double', '点x', 'PointX'],
    # 'PointY': ['double', '点y', 'PointY'],
    # 'PointZ': ['double', '点z', 'PointZ'],

    # 'Origin': ['BPParaVec', '原点', 'Origin'],
    # 'Length': ['double', '长度', 'Length'],
    # 'Width': ['double', '宽度', 'Width'],
    # 'Height': ['double', '高度', 'Height'],
    # 'OriginX': ['double', '原点X', 'OriginX'],
    # 'OriginY': ['double', '原点Y', 'OriginY'],
    # 'OriginZ': ['double', '原点Z', 'OriginZ'],
    # 'Vertex1': ['BPParaVec', '顶点1', 'Vertex1'],
    # 'Vertex2': ['BPParaVec', '顶点2', 'Vertex2'],
    # 'Vertex3': ['BPParaVec', '顶点3', 'Vertex3'],
    # 'Vertex4': ['BPParaVec', '顶点4', 'Vertex4'],
    # 'Vertex5': ['BPParaVec', '顶点5', 'Vertex5'],
    # 'Vertex6': ['BPParaVec', '顶点6', 'Vertex6'],
    # 'Vertex7': ['BPParaVec', '顶点7', 'Vertex7'],
    # 'Vertex8': ['BPParaVec', '顶点8', 'Vertex8'],
    # 'Edge1': ['para::PGSegment', '边1', 'Edge1'],
    # 'Edge2': ['para::PGSegment', '边2', 'Edge2'],
    # 'Edge3': ['para::PGSegment', '边3', 'Edge3'],
    # 'Edge4': ['para::PGSegment', '边4', 'Edge4'],
    # 'Edge5': ['para::PGSegment', '边5', 'Edge5'],
    # 'Edge6': ['para::PGSegment', '边6', 'Edge6'],
    # 'Edge7': ['para::PGSegment', '边7', 'Edge7'],
    # 'Edge8': ['para::PGSegment', '边8', 'Edge8'],
    # 'Edge9': ['para::PGSegment', '边9', 'Edge9'],
    # 'Edge10': ['para::PGSegment', '边10', 'Edge10'],
    # 'Edge11': ['para::PGSegment', '边11', 'Edge11'],
    # 'Edge12': ['para::PGSegment', '边12', 'Edge12'],
    # 'VertexAll': ['std::vector<BPParaVec>', '顶点', 'VertexAll'],
    # 'EdgeAll': ['std::vector<para::PGSegment>', '边', 'EdgeAll'],

    # 'Radius': ['double', '半径', 'Radius'],
    # 'Center': ['BPParaVec', '球心', 'Center'],
    # 'CenterX': ['double', '球心X', 'CenterX'],
    # 'CenterY': ['double', '球心Y', 'CenterY'],
    # 'CenterZ': ['double', '球心Z', 'CenterZ'],
    # custom
}

NAME = AUTO[0]
i = AUTO[1]
nAME = NAME.lower()
GEONAME = 'Geo'+NAME
PARTS = []  # segment
fileName = 'C:/Users/Aking/source/repos/para3.0.1/BPParaComponent/ParaPrimitive/'+GEONAME
isPrint = False
# number = '0x'+'{:0>16}'.format(str(i))
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
    if key != 'Repre':
        fileOriginH3 += '    inline '+PRODICT[key][0] + \
            ' get'+key+'() const\n    {\n        return getPropertyValue<' + \
            PRODICT[key][0]+'>(BPPropertyID(en'+NAME+key+'));\n    }\n'
        # using const refer
        fileOriginH3 += '    inline void set'+key + \
            '(const '+PRODICT[key][0] + \
            '& val)\n    {\n        setPropertyValue({ { BPPropertyID(en' + \
            NAME+key+'), val} });\n    }\n'
fileOriginH += fileOriginH3
fileOriginH += '};\n'

if isPrint:
    print(fileOriginH)
else:
    with open(fileName+'.h', "w", encoding=strEncode) as f:  # new file
        f.write(fileOriginH)


# -----------------------------------------------------------------------------------------------
#                                              cpp
# -----------------------------------------------------------------------------------------------

# head
fileOriginC = '#include "pch.h"\n#define PARA2P3D\n// the geometric implement\n#pragma pack(1) // memory alignment\n'
fileOriginC += 'struct _'+NAME + '\n{\n'
fileOriginCm = ''
for key in PRODICT:
    if key != 'Repre':
        fileOriginCm += '    '+PRODICT[key][0]+' m_'+key.lower()+';\n'
fileOriginC1 = '    std::tuple<_' + NAME + ', BPParaTransform> set(const std::map<BPPropertyID, Gnrc>& val, const BPParaTransform& transform) const\n    {\n        _' + \
    NAME + \
    ' '+nAME + \
    '(*this);\n        BPParaTransform mat = transform;\n        for (const auto& iter : val)\n        {\n            switch (long long(iter.first))\n            {\n'
fileOriginC += fileOriginCm
fileOriginC += fileOriginC1

# set
fileOriginC2 = ''
for key in PRODICT:
    if key == 'Color':
        fileOriginC2 += '            case '+GEONAME + \
            '::en'+NAME + 'Color:\n                ' + nAME + \
            '.m_color = iter.second.as<BPParaColor>();\n                break;\n'
    elif key == 'Material':
        fileOriginC2 += '            case '+GEONAME + \
            '::en'+NAME + 'Material:\n                ' + nAME + \
            '.m_material = iter.second.as<BPParaMaterial>();\n                break;\n'
    else:
        if key != 'Repre':
            fileOriginC2 += '            case ' + GEONAME + \
                '::en' + NAME + \
                key + \
                ':\n            {\n                ' + nAME + '.m_'+key.lower()+' = iter.second.as<' + PRODICT[key][0] + '>();\n' + \
                '                break;\n            }\n'

fileOriginC += fileOriginC2

fileOriginC3 = '            default:\n                break;\n            }\n        }\n        return { ' + nAME + \
    ', mat };\n    }\n    Gnrc get(BPPropertyID id, const BPParaTransform& mat) const\n    {\n        switch (long long(id))\n        {\n'
fileOriginC += fileOriginC3

# get
fileOriginC4 = ''
for key in PRODICT:
    if key == 'Color':
        fileOriginC4 += '        case ' + GEONAME + \
            '::en' + NAME + 'Color:\n            return m_color;\n'
    elif key == 'Material':
        fileOriginC4 += '        case ' + GEONAME + \
            '::en' + NAME + 'Material:\n            return m_material;\n'
    else:  # old distinguish member
        if key != 'Repre':
            fileOriginC4 += '        case ' + GEONAME + \
                '::en' + NAME + key + \
                ':\n            return m_'+key.lower()+';\n'
fileOriginC += fileOriginC4

# graphic
fileOriginC5 = '        default:\n            return BPParaNone();\n            break;\n        }\n    }\n' +\
    '    std::vector<std::tuple<bool, BPGraphicPart>> graphic(const BPParaTransform& transform) const\n    {\n        std::vector<std::tuple<bool, BPGraphicPart>> res;\n        p3d::IGeSolidBasePtr solidPrimitive ;\n' +\
    '        res.push_back({ true, BPGraphicPart(solidPrimitive, transform) });\n        return res;\n    }\n};\n#pragma pack() //end memory alignment\n\n//enrol property\nstatic int _enrol = []()->int\n{\n'
fileOriginC += fileOriginC5

# _enrol
fileOriginC += '    __PrimitiveInterface::enrol<_' + \
    NAME + ', ' + GEONAME + '>( 0,\n        {\n'
fileOriginC6 = ''
for key in PRODICT:
    fileOriginC6 += '        { ' + GEONAME + \
        '::en' + NAME + \
        key + \
        ',    {typeid('+PRODICT[key][0] + \
        '),    { {BPParaLanguage::Chinese, \"' + \
        PRODICT[key][1] + '\" }, {BPParaLanguage::English, \"' + \
        PRODICT[key][2] + '\" } } } }, \n'
fileOriginC += fileOriginC6

fileOriginC += '        }\n    );\n    return 0;\n}();\n// the geometric primitive\n' + GEONAME + \
    '::' + GEONAME + \
    '() :\n    BPGeometricPrimitive(__PrimitiveInterface::create(_' + NAME + '(), BPParaTransform()))\n{\n}\n' + \
    GEONAME + '::~' + GEONAME + '()\n{\n}\n'

# generate file
if isPrint:
    print(fileOriginC)
else:
    with open(fileName+'.cpp', "w", encoding=strEncode) as f:  # new file
        f.write(fileOriginC)
