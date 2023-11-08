strEncode = 'GB2312'  # 'utf-8' # vs必须使用2312

# AUTO = ["EquilateralAngleSteel", 126 , "等边角钢" ]
# AUTO = ["ScaleneAnglesteel", 127 , "不等边角钢" ]
# AUTO = ["I-beam", 128, "工字钢" ]
# AUTO = ["I-Lightbeams", 129 , "轻型T字钢" ]
# AUTO = ["H-beam", 130 , "H型钢" ]
# AUTO = ["BeamChannel", 131 , "槽钢" ]
# AUTO = ["LightBeamChannel", 132 , "轻型槽钢" ]
# AUTO = ["FlatSteel", 133 , "扁钢" ]
# AUTO = ["L-Steel", 134 , "1 , 钢" ] 
# AUTO = ["T-Steel", 135 , "T型钢" ]
# AUTO = ["RoundSteel", 136 , "圆钢" ]
# AUTO = ["RoundSteelTube", 137, "圆钢管" ]
# AUTO = ["RectangularSteelTube", 138 , "矩形钢管" ]
# AUTO = ["SquareSteelTube", 139, "方形钢管" ]
# AUTO = ["DoubleChannelSteel", 140 , "双槽钢" ]
# AUTO = ["EquilateralDoubleAngleSteel", 141 , "等边双角钢" ]
# AUTO = ["UnequalAnglesteel", "不等边双角钢" ]
# AUTO = ["PolygonRoundSteelTube", 142 , "多边形钢管" ] 
# AUTO = ["WrongEntity", 143 , "错误图元" ]

# GIM
# AUTO = ["GeSTL", 100 , "GeSTL" ]
# AUTO = ["ExFound', 101, 'E.7掏挖基础']
# AUTO = ["GeBasicStep', 102, 'E.8 ']
# AUTO = ["ST100, ', 101, 'E.8 ']

# AUTO = ["Sphere", 101, "球体" ]
# AUTO = ["RotationaEllipsoid", 102, "旋转椭球体" ]
# AUTO = ["Cuboid", 103, "长方体" ]
# AUTO = ["Table", 104, "棱台(锥) "]
# AUTO = ["OffsetRectangularTable", 105, "偏移矩形台"]
# AUTO = ["Cylinder", 106, "圆柱体" ]
# AUTO = ["BendingCylindrical", 107, "弯折圆柱" ]
# AUTO = ["TruncatedCone", 108, "圆台体"]
# AUTO = ["EccentricTruncatedCone", 109, "偏心圆台体" ]
# AUTO = ["Ring", 110, "圆环" ]
# AUTO = ["RectangularRing", 111, "矩形环" ]
# AUTO = ["EllipticRing", 112, "椭圆环" ]
# AUTO = ["CircularGasket", 113, "圆形垫片" ] 
# AUTO = ["TableGasket", 114, "台型垫片"]
# AUTO = ["SquareGasket", 115, "方形垫片" ]
# AUTO = ["StretchedBody", 116, "拉伸体" ]
# AUTO = ["PorcelainBushing", 117, "瓷套/绝缘子(未含上下法兰)"]
# AUTO = ["ConePorcelainBushing", 118, "锥形瓷套"]
# AUTO = ["Insulator", 119, "绝缘子串" ]
# AUTO = ["VTypelnsulator", 120, "V型绝缘子串"] 
# AUTO = ["TerminalBlock", 121, "端子板" ]
# AUTO = ["Rectangularfixedplate", 122, "安装矩形开孔板"] 
# AUTO = ["Circularfixedplate", 123, "安装圆形开孔板" ]
# AUTO = ["Wire", 124, "导线" ]
AUTO = ["Boolean", 98, "布尔节点" ]


PRODICT = {
    'Repre': [AUTO[0], AUTO[2], AUTO[0]],
    'Color': ['BPParaColor', '颜色', 'Color'],
    'Material': ['BPParaMaterial', '材质', 'Material'],
    # GimExFound
    # 'H1': ['double', '柱体高度', 'm_H1'],
    # 'H2': ['double', '底座高度', 'm_H2'],
    # 'H3': ['double', '垫层厚度', 'm_H3'],
    # 'd': ['double', '柱体直径', 'm_d'],
    # 'D': ['double', '底座直径', 'm_D'],
    # 'Alpha1': ['double', 'X轴坡度', 'm_Alpha1'],
    # 'Alpha2': ['double', 'Y轴坡度', 'm_Alpha2'],
    # GimST100, 
    # 'Points': ['BPParaVec', '顶点', 'Points'],
    # 'Indexs': ['BPParaVec', '索引', 'Indexs'],
    # 'R': ['double', '半径', 'R'],
    # 'LR': ['double', 'LR', 'LR'],
    # 'WR': ['double', 'WR', 'WR'],
    # 'H': ['double', 'H', 'H'],
    # 'L': ['double', '长', 'L'],
    # 'W': ['double', '宽', 'W'],
    # 'H': ['double', '高', 'H'],
    # 'TL1': ['double', 'TL1', 'TL1'],
    # 'TL2': ['double', 'TL2', 'TL2'],
    # 'LL1': ['double', 'LL1', 'LL1'],
    # 'LL2': ['double', 'LL2', 'LL2'],
    # 'H': ['double', '高', 'H'],

    # 'TL': ['double', 'TL', 'TL'],
    # 'TW': ['double', 'TW', 'TW'],
    # 'LL': ['double', 'LL', 'LL'],
    # 'LW': ['double', 'LW', 'LW'],
    # 'H': ['double', '高', 'H'],
    # 'XOFF': ['double', 'X偏移', 'XOFF'],
    # 'YOFF': ['double', 'Y偏移', 'YOFF'],

    # 'R': ['double', '半径', 'R'],
    # 'H': ['double', '高', 'H'],
    # BendingCylindrical
    # 'R': ['double', '半径', 'R'],
    # 'L': ['double', '长', 'L'],
    # 'Rad': ['double', '弧度', 'Rad'],

    'BooleanType': ['int', '布尔类型', 'BooleanType'],
    'LeftKey': ['BPGeometricPrimitive', '左叶子节点', 'LeftKey'],
    'RightKey': ['BPGeometricPrimitive', '右叶子节点', 'RightKey'],
}

def auto_generate(AUTO,PRODICT):
    NAME = AUTO[0]
    i = AUTO[1]
    nAME = NAME.lower()
    GEONAME = 'GIMGe'+NAME  # 'Geo'+NAME
    PARTS = []  # segment
    fileName = 'C:/Users/Aking/source/repos/para3.0.1/BPParaComponent/ParaPrimitive/GIM/'+GEONAME
    isPrint = False
    number = '0x'+'{:0>16}'.format(str(i))
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
    fileOriginC = '#include "pch.h"\n#define PARA2P3D\nusing namespace p3d;\n// the geometric implement\n#pragma pack(1) // memory alignment\n'
    fileOriginC += 'struct _'+NAME + '\n{\n'
    fileOriginCm = ''
    for key in PRODICT:
        if key != 'Repre':
            fileOriginCm += '    '+PRODICT[key][0]+' m_'+key+';\n'
    fileOriginC1 = '    std::tuple<_' + NAME + ', BPParaTransform> set(const std::map<BPPropertyID, Gnrc>& val, const BPParaTransform& transform) const\n    {\n        _' + \
        NAME + \
        ' '+nAME + \
        '(*this);\n        BPParaTransform mat = transform;\n        for (const auto& iter : val)\n        {\n            switch (long long(iter.first))\n            {\n'
    fileOriginC += fileOriginCm
    fileOriginC += fileOriginC1

    # set
    fileOriginC2 = ''
    for key in PRODICT:
        if key != 'Repre':
            fileOriginC2 += '            case ' + GEONAME + \
                '::en' + NAME + \
                key + \
                ':\n            {\n                ' + nAME + '.m_'+key+' = iter.second.as<' + PRODICT[key][0] + '>();\n' + \
                '                break;\n            }\n'

    fileOriginC += fileOriginC2

    fileOriginC3 = '            default:\n                break;\n            }\n        }\n        return { ' + nAME + \
        ', mat };\n    }\n    Gnrc get(BPPropertyID id, const BPParaTransform& mat) const\n    {\n        switch (long long(id))\n        {\n'
    fileOriginC += fileOriginC3

    # get
    fileOriginC4 = ''
    for key in PRODICT:
        if key != 'Repre':
            fileOriginC4 += '        case ' + GEONAME + \
                '::en' + NAME + key + \
                ':\n            return m_'+key+';\n'
    fileOriginC += fileOriginC4

    # graphic
    fileOriginC5 = '        default:\n            return BPParaNone();\n            break;\n        }\n    }\n' +\
        '    std::vector<std::tuple<bool, BPGraphicPart>> graphic(const BPParaTransform& transform) const\n    {\n        std::vector<std::tuple<bool, BPGraphicPart>> res;\n\n' +\
        '        res.push_back({ true, BPGraphicPart(IGeSolidBasePtr(), transform) });\n        return res;\n    }\n};\n#pragma pack() //end memory alignment\n\n//enrol property\nstatic int _enrol = []()->int\n{\n'
    fileOriginC += fileOriginC5

    # _enrol
    fileOriginC += '    __PrimitiveInterface::enrol<_' + \
        NAME + ', ' + GEONAME + '>( 0,\n        {\n' #去掉编号
    fileOriginC6 = ''
    for key in PRODICT:
        if key=='Repre':
            fileOriginC6 += '        { ' + GEONAME + \
                '::en' + NAME + \
                key + \
                ',    {typeid(GIMGe'+PRODICT[key][0] + \
                '),    { {BPParaLanguage::Chinese, \"' + \
                PRODICT[key][1] + '\" }, {BPParaLanguage::English, \"' + \
                PRODICT[key][2] + '\" } } } }, \n'
        else:
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

GEOLIST=[


'GeoCube'                ,
'GeoCone'                ,
'GeoSphere'              ,
'GeoSweep'               ,
'GeoLoft'                ,
'GeoIntersect'           ,
'GeoFusion'              ,
'GeoCombine'             ,
'GeoArray'               ,
'GeoSplineCurve'         ,
'GeoSegment'             ,
'GeoPoint:'              ,
'GeoLine'                ,
'GeoArc'                 ,
'GeoText'                ,
'GeoSection'             ,
]
'''
a649c1f33adbb37befc4772bab989354  GeoCube
d613e9fd691ba2d2f29aba13146cb6d3  GeoCone
049f90b17d223b3e79b4c67e5dbbf6f9  GeoSphere
15434ae33656a646526cbb4c2ecbc7d6  GeoSweep
91e4053631814eeb72c073a006fb0307  GeoLoft
7bf08cb9bb126dfc3c75f22e0f2ebcb5  GeoIntersect
3c43d93d02036a3138c01ecb739d1f75  GeoFusion
3ed74f5a90487cac45c56fba27c409d2  GeoCombine
85d5e2d0f310916ab86b793e5cb15ca1  GeoArray
4322f2ce24a36e4ad5acd5b0ad7ea923  GeoSplineCurve
b9eb75f1ce389990d472186046503315  GeoSegment
4c92c8c43dfaa7967d5e0aa4defd0dae  GeoPoint:
d1f3222b7e14a5d078c378f1a76ad0c3  GeoLine
279fcb18725fe80b3b944003dac103b9  GeoArc
842b1a5b9fe0ea29901ff1803e45b227  GeoText
706f8949497c84c6b64462653ed01b47  GeoSection
b'po\x89II|\x84\xc6\xb6Dbe>\xd0\x1bG'
0000000000000009
'''

import hashlib
if __name__=='__main__':
    auto_generate(AUTO,PRODICT)

    # for iter in GEOLIST:
    # # 创建MD5对象，可以直接传入要加密的数据
    #     md = hashlib.md5(iter.encode(encoding='utf-8')).hexdigest()
    #     print(md+'  '+iter) # 