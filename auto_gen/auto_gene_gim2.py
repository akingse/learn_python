import re
strEncode = 'GB2312'  # 'utf-8' # vs必须使用2312


# 型钢参数不全 18个
GEOTYPEALL='''
    { L"EquilateralAngleSteel", L"等边角钢" },
    { L"ScaleneAngleSteel", L"不等边角钢" },
    { L"I-beam", L"工字钢" },
    { L"I-Lightbeams", L"轻型工字钢" },
    { L"H-beam", L"H型钢" },
    { L"BeamChannel", L"槽钢" },
    { L"LightBeamChannel", L"轻型槽钢" },
    { L"FlatSteel", L"扁钢" },
    { L"L-Steel", L"L钢" },
    { L"T-Steel", L"T型钢" },
    { L"RoundSteel", L"圆钢" },
    { L"RoundSteelTube", L"圆钢管" },
    { L"RectangularSteelTube", L"矩形钢管" },
    { L"SquareSteelTube", L"方形钢管" },
    { L"DoubleChannelSteel", L"双槽钢" },
    { L"EquilateralDoubleAngleSteel", L"等边双角钢" },
    { L"UnequalAngleSteel", L"不等边双角钢" },
    { L"PolygonRoundSteelTube", L"多边形钢管" },
'''

TEXT_CN='''
{ L"FlatSteel",//扁钢,
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"高度 h", GIMGeElementParaType::DOUBLE },
    { L"宽度 b", GIMGeElementParaType::DOUBLE },
}
},
{ L"DoubleChannelSteel",//双槽钢,
{
    { L"型号",GIMGeElementParaType::TEXT },
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"间隙 d", GIMGeElementParaType::DOUBLE },
}
},
{ L"EquilateralDoubleAngleSteel",//等边双角钢,
{
    { L"型号",GIMGeElementParaType::TEXT },
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"间隙 d", GIMGeElementParaType::DOUBLE },
}
},
{ L"UnequalAngleSteel",//不等边双角钢,
{
    { L"型号",GIMGeElementParaType::TEXT },
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"间隙 d", GIMGeElementParaType::DOUBLE },
}
},
{ L"PolygonRoundSteelTube",//多边形钢管,
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"边长 r", GIMGeElementParaType::DOUBLE },
    { L"边数 n", GIMGeElementParaType::INT },
    { L"厚度 t", GIMGeElementParaType::DOUBLE },
}
},
{ L"I-beam", //"工字钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"I-Lightbeams", //"轻型工字钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"H-beam", //"H型钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"BeamChannel",// "槽钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"LightBeamChannel", //"轻型槽钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"L-Steel", //"L钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"T-Steel", //"T型钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"RoundSteel", //"圆钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"RoundSteelTube", //"圆钢管" ,
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"RectangularSteelTube", //"矩形钢管" ,
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"SquareSteelTube", //"方形钢管" ,
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"EquilateralAngleSteel", //"等边角钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
},
{ L"ScaleneAngleSteel", //"不等边角钢",
{
    { L"长度 L", GIMGeElementParaType::DOUBLE },
    { L"型号",GIMGeElementParaType::TEXT },
}
}//
'''
# -----------------------------------------------------------------
# -----------------------------------------------------------------
TEXT_ENG='''
{ L"FlatSteel",//扁钢
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"h", GIMGeElementParaType::DOUBLE },
    { L"b", GIMGeElementParaType::DOUBLE },
}
},
{ L"DoubleChannelSteel",//双槽钢
{
    { L"Model",GIMGeElementParaType::TEXT },
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"d", GIMGeElementParaType::DOUBLE },
}
},
{ L"EquilateralDoubleAngleSteel",//等边双角钢
{
    { L"Model",GIMGeElementParaType::TEXT },
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"d", GIMGeElementParaType::DOUBLE },
}
},
{ L"UnequalAngleSteel",//不等边双角钢
{
    { L"Model",GIMGeElementParaType::TEXT },
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"d", GIMGeElementParaType::DOUBLE },
}
},
{ L"PolygonRoundSteelTube",//多边形钢管
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"r", GIMGeElementParaType::DOUBLE },
    { L"n", GIMGeElementParaType::INT },
    { L"t", GIMGeElementParaType::DOUBLE },
}
},
{ L"I-beam", //"工字钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"I-Lightbeams", //"轻型工字钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"H-beam", //"H型钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"BeamChannel",// "槽钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"LightBeamChannel", //"轻型槽钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"L-Steel", //"L钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"T-Steel", //"T型钢" 
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"RoundSteel", //"圆钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"RoundSteelTube", //"圆钢管" 
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"RectangularSteelTube", //"矩形钢管" 
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"SquareSteelTube", //"方形钢管" 
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"EquilateralAngleSteel", //"等边角钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
},
{ L"ScaleneAngleSteel", //"不等边角钢"
{
    { L"Length", GIMGeElementParaType::DOUBLE },
    { L"Model",GIMGeElementParaType::TEXT },
}
}
//
'''


# 类名
GEODICT0=re.findall(r"{\sL.+?}", GEOTYPEALL)
GEODICT_NAME=[]
for iter in GEODICT0:
    arg0 = re.sub(r'{|}', '', iter)
    arg1 = re.sub(r'\sL|\'|\"|\s', '', arg0)
    # GEODICT1.append(arg1)
    GEODICT_NAME.append(arg1.split(','))

# 中文
GEODICT2=TEXT_CN.split('\n')
GEODICT3=[]
for i in range(len(GEODICT2)-2):
    if GEODICT2[i].find("//")!=-1:
        temp=''#GEODICT2[i]
        while GEODICT2[i+1].find("//")==-1 :
            a=GEODICT2[i].find("//")
            i+=1
            temp+=GEODICT2[i]
        GEODICT3.append(temp)

GEODICT_CN=[]
for iter in GEODICT3:
    arg = re.sub(r'{|}|\sL\"|\'|\"|\s|/', '', iter)
    arg = re.sub(r'GIMGeElementParaType::DOUBLE', 'double', arg)
    arg = re.sub(r'GIMGeElementParaType::INT', 'int', arg)
    arg = re.sub(r'GIMGeElementParaType::TEXT', 'std::string', arg)
    arg = re.sub(r',,', '', arg)
    GEODICT_CN.append(arg)

# 英文
GEODICT2=TEXT_ENG.split('\n')
GEODICT3=[]
for i in range(len(GEODICT2)-2):
    if GEODICT2[i].find("//")!=-1:
        temp=''#temp=GEODICT2[i]
        while GEODICT2[i+1].find("//")==-1 :
            a=GEODICT2[i].find("//")
            i+=1
            temp+=GEODICT2[i]
        GEODICT3.append(temp)
GEODICT_ENG=[]
for iter in GEODICT3:
    arg = re.sub(r'{|}|\sL\"|\'|\"|\s|/', '', iter)
    arg = re.sub(r'GIMGeElementParaType::DOUBLE', 'double', arg)
    arg = re.sub(r'GIMGeElementParaType::INT', 'int', arg)
    arg = re.sub(r'GIMGeElementParaType::TEXT', 'std::string', arg)
    arg = re.sub(r',,', '', arg)
    GEODICT_ENG.append(arg)
# exit(0)

#部分类名含有-，需要额外处理
GEODICT_NAME=[ #copy from debug
['EquilateralAngleSteel', '等边角钢'],
['ScaleneAngleSteel', '不等边角钢'],
['Ibeam', '工字钢'],  #I-beam
['ILightbeams', '轻型工字钢'], #I-Lightbeams
['Hbeam', 'H型钢'],#H-beam
['BeamChannel', '槽钢'],
['LightBeamChannel', '轻型槽钢'],
['FlatSteel', '扁钢'],
['LSteel', 'L钢'],#L-Steel
['TSteel', 'T型钢'],#T-Steel
['RoundSteel', '圆钢'],
['RoundSteelTube', '圆钢管'],
['RectangularSteelTube', '矩形钢管'],
['SquareSteelTube', '方形钢管'],
['DoubleChannelSteel', '双槽钢'],
['EquilateralDoubleAngleSteel', '等边双角钢'],
['UnequalAngleSteel', '不等边双角钢'],
['PolygonRoundSteelTube', '多边形钢管'],
]

# 处理

GEODICT_ALL=[]
AUTO=[]
for i in range(len(GEODICT_NAME)):
    AUTO.append([GEODICT_NAME[i][0],201+i,GEODICT_NAME[i][1]])

for i in range(len(GEODICT_NAME)):
    PRODICT = {
        'Repre': [AUTO[i][0], AUTO[i][2], AUTO[i][0]],
        'Color': ['BPParaColor', '颜色', 'Color'],
        'Material': ['BPParaMaterial', '材质', 'Material'],
    }
    eng=GEODICT_ENG[i]
    engKey=eng.split(',')
    cn=GEODICT_CN[i]
    cnKey=cn.split(',')
    sz=len(engKey)/2
    for k in range(int(sz)):
        # 'Length': ['double', '长度', 'Length'],
        value=[engKey[1+2*k],cnKey[2*k].lstrip().rstrip(),engKey[2*k]]
        PRODICT[engKey[2*k]]=value
    GEODICT_ALL.append(PRODICT)

# for iter in AUTO:
#     print('#include "'+iter[0]+'.h"')


from test_re02_GIM import auto_generate
for i in range(len(GEODICT_NAME)):
    auto_generate(AUTO[i],GEODICT_ALL[i])



# 20+25
GEOTYPEALL_OVERHEAD='''
    {L"PileFoundation"							,L"挖孔桩基础"},
    {L"PileFoundation"							,L"灌注桩单桩基础"},
    {L"DiggingPilePlatformFoundation"			,L"承台挖孔桩基础"},
    {L"DiggingPilePlatformFoundation"			,L"承台灌注桩基础"},
    {L"DirectAnchoredRockAnchoredPileFoundation",L"直锚式岩石锚桩基础"},
    {L"RockAnchorPilePlatformFoundation"		,L"承台式岩石锚桩基础"},
    {L"EmbeddedRockAnchorPileFoundation"		,L"嵌固式岩石锚桩基础"},
    {L"InclinedAnchorRockPileFoundation"		,L"斜锚式岩石锚桩基础"},
    {L"ExFound"									,L"掏挖基础"},
    {L"BasicStep"								,L"台阶基础"},
    {L"SteppedBaseFoundation"					,L"台阶底板基础"},
    {L"SlopeTypeFloorFoundation"				,L"斜坡底板基础"},
    {L"CompositeCaissonFoundation"				,L"复合式沉井基础"},
    {L"RaftFoundation"							,L"筏板基础"},
    {L"GimGeDirectlyBuriedFoundation"			,L"直埋式基础"},
    {L"SleeveFoundation"						,L"钢套筒式基础"},
    {L"StraightColumnFoundation"				,L"装配式直柱固接型基础"},
    {L"StraightColumnHingedFoundation"			,L"装配式直柱铰接型基础"},
    {L"FabricatedMetalHolder"					,L"装配式金属支架型基础"},
    {L"ConcreteSupportBase"						,L"装配式混凝土构件支架型基础"},

    {L"OpticalCable",L"光电缆"},
    {L"MiddleJoint",L"接头"},
    {L"CableTerminal",L"终端"},
    {L"StraightWell",L"直线井"},
    {L"StraightLineTunnelHole",L"直线暗挖隧道井"},
    {L"CornerWell",L"转角井"},
    {L"TWell",L"三通井"},
    {L"CrossWell",L"四通井"},
    {L"ExhaustPipe",L"排管"},
    {L"CableTrench",L"电缆沟"},
    {L"CableTunnel",L"电缆隧道"},
    {L"ShaftPosition",L"竖井仓"},
    {L"TunnelBaffle",L"隧道井隔板"},
    {L"DirectAirduct",L"直通风道"},
    {L"DrainWell",L"排水井"},
    {L"CableAttachment",L"电缆附件"},
    {L"CableBeam",L"电缆梁"},
    {L"CableManhole",L"电缆人孔"},
    {L"CableClamp",L"电缆夹具"},
    {L"CableBracket",L"电缆支架"},
    {L"CableColumn",L"电缆立柱"},
    {L"GroundingFlatIron",L"接地扁铁"},
    {L"EmbeddedPart",L"预埋件"},
    {L"UTAB",L"U型拉环"},
    {L"LiftClimb",L"吊攀"},
'''

g_GimGePowertransParaDic ='''

        //1挖孔桩基础、灌注桩单桩基础
{ L"PileFoundation",
    {
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE },
        { L"H3", GIMGeElementParaType::DOUBLE },
        { L"H4", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"D", GIMGeElementParaType::DOUBLE }
    }
},

//2 承台挖孔桩基础、承台灌注桩基础
{ L"DiggingPilePlatformFoundation",
    {

        { L"cs",GIMGeElementParaType::BOOLEAN},
        {L"n",GIMGeElementParaType::INT},
        {L"L1",GIMGeElementParaType::DOUBLE},
        {L"B1",GIMGeElementParaType::DOUBLE},
        {L"e1",GIMGeElementParaType::DOUBLE},
        {L"e2",GIMGeElementParaType::DOUBLE},
        {L"H1",GIMGeElementParaType::DOUBLE},
        {L"H2",GIMGeElementParaType::DOUBLE},
        {L"H3",GIMGeElementParaType::DOUBLE},
        {L"H4",GIMGeElementParaType::DOUBLE},
        {L"H5",GIMGeElementParaType::DOUBLE},
        {L"H6",GIMGeElementParaType::DOUBLE},
        {L"b",GIMGeElementParaType::DOUBLE},
        {L"d",GIMGeElementParaType::DOUBLE},
        {L"D",GIMGeElementParaType::DOUBLE},
        {L"ZPOSTARRAY",GIMGeElementParaType::ARRAY}
    }
},

//3直锚式岩石锚桩基础 
{ L"DirectAnchoredRockAnchoredPileFoundation",
    {
        { L"n", GIMGeElementParaType::INT },
        { L"L1", GIMGeElementParaType::DOUBLE },
        { L"B1", GIMGeElementParaType::DOUBLE },
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"桩顶点坐标", GIMGeElementParaType::ARRAY}
    }
},

//4承台式岩石锚桩基础
{ L"RockAnchorPilePlatformFoundation",
    {
        { L"cs",GIMGeElementParaType::BOOLEAN},
        {L"n",GIMGeElementParaType::INT},
        {L"L1",GIMGeElementParaType::DOUBLE},
        {L"B1",GIMGeElementParaType::DOUBLE},
        {L"e1",GIMGeElementParaType::DOUBLE},
        {L"e2",GIMGeElementParaType::DOUBLE},
        {L"H1",GIMGeElementParaType::DOUBLE},
        {L"H2",GIMGeElementParaType::DOUBLE},
        {L"H3",GIMGeElementParaType::DOUBLE},
        {L"b",GIMGeElementParaType::DOUBLE},
        {L"d",GIMGeElementParaType::DOUBLE},
        {L"ZPOSTARRAY",GIMGeElementParaType::ARRAY}
    }
},


//5嵌固式岩石锚桩基础
{ L"EmbeddedRockAnchorPileFoundation",
    {
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE },
        { L"H3", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"D", GIMGeElementParaType::DOUBLE }
    }
},

{ L"InclinedAnchorRockPileFoundation",
    {
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"D", GIMGeElementParaType::DOUBLE },
        { L"B", GIMGeElementParaType::DOUBLE },
        { L"L", GIMGeElementParaType::DOUBLE },
        { L"e1", GIMGeElementParaType::DOUBLE },
        { L"e2", GIMGeElementParaType::DOUBLE },
        { L"α1", GIMGeElementParaType::DOUBLE },
        { L"α2", GIMGeElementParaType::DOUBLE }
    }
},

{ L"ExFound",
    {
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE },
        { L"H3", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"D", GIMGeElementParaType::DOUBLE },
        { L"α1", GIMGeElementParaType::DOUBLE },
        { L"α2", GIMGeElementParaType::DOUBLE }
    }
},

{ L"BasicStep", { { L"N", GIMGeElementParaType::INT },
{ L"H", GIMGeElementParaType::DOUBLE },
{ L"b", GIMGeElementParaType::DOUBLE },
{ L"StepInfos", GIMGeElementParaType::TEXT } } },

{ L"SteppedBaseFoundation",
{
{ L"N", GIMGeElementParaType::INT },
{ L"H", GIMGeElementParaType::DOUBLE },
{ L"b", GIMGeElementParaType::DOUBLE },
{ L"α1", GIMGeElementParaType::DOUBLE },
{ L"α2", GIMGeElementParaType::DOUBLE },
{ L"LsArray", GIMGeElementParaType::DOUBLE },
{ L"BsArray", GIMGeElementParaType::DOUBLE },
{ L"HsArray", GIMGeElementParaType::DOUBLE }
} },

{ L"SlopeTypeFloorFoundation",
{
{ L"H1", GIMGeElementParaType::DOUBLE },
{ L"H2", GIMGeElementParaType::DOUBLE },
{ L"H3", GIMGeElementParaType::DOUBLE },
{ L"b", GIMGeElementParaType::DOUBLE },
{ L"L1", GIMGeElementParaType::DOUBLE },
{ L"L2", GIMGeElementParaType::DOUBLE },
{ L"B1", GIMGeElementParaType::DOUBLE },
{ L"B2", GIMGeElementParaType::DOUBLE },
{ L"α1", GIMGeElementParaType::DOUBLE },
{ L"α2", GIMGeElementParaType::DOUBLE }}},

{ L"CompositeCaissonFoundation",
    {
        { L"H1",GIMGeElementParaType::DOUBLE },
        { L"H2",GIMGeElementParaType::DOUBLE },
        { L"H3",GIMGeElementParaType::DOUBLE },
        { L"H4",GIMGeElementParaType::DOUBLE },
        { L"D",GIMGeElementParaType::DOUBLE },
        { L"t",GIMGeElementParaType::DOUBLE },
        { L"b",GIMGeElementParaType::DOUBLE },
        { L"B1",GIMGeElementParaType::DOUBLE },
        { L"L1",GIMGeElementParaType::DOUBLE },
        { L"B2",GIMGeElementParaType::DOUBLE },
        { L"L2",GIMGeElementParaType::DOUBLE }
    }
},

{ L"RaftFoundation", { { L"ShapeType", GIMGeElementParaType::INT },
{ L"H1", GIMGeElementParaType::DOUBLE },
{ L"H2", GIMGeElementParaType::DOUBLE },
{ L"H3", GIMGeElementParaType::DOUBLE },
{ L"b1", GIMGeElementParaType::DOUBLE },
{ L"b2", GIMGeElementParaType::DOUBLE },
{ L"B1", GIMGeElementParaType::DOUBLE },
{ L"B2", GIMGeElementParaType::DOUBLE },
{ L"L1", GIMGeElementParaType::DOUBLE },
{ L"L2", GIMGeElementParaType::DOUBLE },
} },

// 13 直埋式基础
{ L"GimGeDirectlyBuriedFoundation",
    {
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"t", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"固定盘形式", GIMGeElementParaType::INT},
        { L"D", GIMGeElementParaType::DOUBLE },
        { L"B", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE }
    }
},

{ L"SleeveFoundation", { { L"ShapeType", GIMGeElementParaType::INT },
{ L"H1", GIMGeElementParaType::DOUBLE },
{ L"H2", GIMGeElementParaType::DOUBLE },
{ L"H3", GIMGeElementParaType::DOUBLE },
{ L"H4", GIMGeElementParaType::DOUBLE },
{ L"D1", GIMGeElementParaType::DOUBLE },
{ L"D2", GIMGeElementParaType::DOUBLE },
{ L"B1", GIMGeElementParaType::DOUBLE },
{ L"B2", GIMGeElementParaType::DOUBLE },
{ L"d", GIMGeElementParaType::DOUBLE },
{ L"t", GIMGeElementParaType::DOUBLE } } },

{ L"StraightColumnFoundation",
    {
        { L"H1", GIMGeElementParaType::DOUBLE },
        { L"H2", GIMGeElementParaType::DOUBLE },
        { L"H3", GIMGeElementParaType::DOUBLE },
        { L"d", GIMGeElementParaType::DOUBLE },
        { L"B1", GIMGeElementParaType::DOUBLE },
        { L"B2", GIMGeElementParaType::DOUBLE },
        { L"L1", GIMGeElementParaType::DOUBLE },
        { L"L2", GIMGeElementParaType::DOUBLE }
    }
},

{ L"StraightColumnHingedFoundation", { { L"有无卡盘", GIMGeElementParaType::BOOLEAN },
{ L"H1", GIMGeElementParaType::DOUBLE },
{ L"H2", GIMGeElementParaType::DOUBLE },
{ L"d", GIMGeElementParaType::DOUBLE },
{ L"B1", GIMGeElementParaType::DOUBLE },
{ L"B2", GIMGeElementParaType::DOUBLE },
{ L"L1", GIMGeElementParaType::DOUBLE },
{ L"L2", GIMGeElementParaType::DOUBLE },
{ L"B", GIMGeElementParaType::DOUBLE },
{ L"H", GIMGeElementParaType::DOUBLE },
{ L"L", GIMGeElementParaType::DOUBLE },
{ L"H3", GIMGeElementParaType::DOUBLE } } },

{ L"FabricatedMetalHolder",
    {
        { L"S1", GIMGeElementParaType::TEXT },
        { L"S2", GIMGeElementParaType::TEXT },
        {L"H1",GIMGeElementParaType::DOUBLE},
        {L"H2",GIMGeElementParaType::DOUBLE},
        {L"H3",GIMGeElementParaType::DOUBLE},
        {L"H4",GIMGeElementParaType::DOUBLE},
        {L"H5",GIMGeElementParaType::DOUBLE},
        {L"H6",GIMGeElementParaType::DOUBLE},
        {L"H7",GIMGeElementParaType::DOUBLE},
        {L"L1",GIMGeElementParaType::DOUBLE},
        {L"L2",GIMGeElementParaType::DOUBLE},
        {L"b1",GIMGeElementParaType::DOUBLE},
        {L"b2",GIMGeElementParaType::DOUBLE},
        {L"B1",GIMGeElementParaType::DOUBLE},
        {L"B2",GIMGeElementParaType::DOUBLE},
        {L"n1",GIMGeElementParaType::INT},
        {L"n2",GIMGeElementParaType::INT}
    }
},

{ L"ConcreteSupportBase",
    {
        { L"S1", GIMGeElementParaType::TEXT },
        {L"H1",GIMGeElementParaType::DOUBLE},
        {L"H2",GIMGeElementParaType::DOUBLE},
        {L"H3",GIMGeElementParaType::DOUBLE},
        {L"H4",GIMGeElementParaType::DOUBLE},
        {L"H5",GIMGeElementParaType::DOUBLE},
        {L"L1",GIMGeElementParaType::DOUBLE},
        {L"L2",GIMGeElementParaType::DOUBLE},
        {L"b1",GIMGeElementParaType::DOUBLE},
        {L"b2",GIMGeElementParaType::DOUBLE},
        {L"b3",GIMGeElementParaType::DOUBLE},
        {L"B1",GIMGeElementParaType::DOUBLE},
        {L"B2",GIMGeElementParaType::DOUBLE},
        {L"n1",GIMGeElementParaType::INT},
    }
},

{ L"Bolt",
    {
        { L"型号",GIMGeElementParaType::TEXT },
        { L"材质", GIMGeElementParaType::TEXT }
    }
},
{ L"Wire",
    {
        { L"型号",GIMGeElementParaType::TEXT },
        { L"导线截面", GIMGeElementParaType::DOUBLE },
        { L"外径", GIMGeElementParaType::DOUBLE },
        { L"单位长度质量", GIMGeElementParaType::DOUBLE },
        { L"弹性系数", GIMGeElementParaType::DOUBLE },
        { L"线膨胀系数", GIMGeElementParaType::DOUBLE },
        { L"破坏拉断力", GIMGeElementParaType::DOUBLE }
    }
},
{ L"Cross",
    {
        { L"CODE",GIMGeElementParaType::INT },
        { L"POINTNUM", GIMGeElementParaType::INT },
        { L"POINTCOR", GIMGeElementParaType::TEXT_ARRAY },
        { L"LINENUM", GIMGeElementParaType::INT },
        { L"LINEINF", GIMGeElementParaType::TEXT_ARRAY },
    }
},
//E20架空线路绝缘子串
    { L"GTInsulator",
            {
    {L"型号",GIMGeElementParaType::TEXT},
    {L"导线分裂数",GIMGeElementParaType::INT},
    {L"分裂排列方式",GIMGeElementParaType::INT},
    {L"分裂间距",GIMGeElementParaType::DOUBLE},
    {L"串用途",GIMGeElementParaType::INT},
    {L"串类型",GIMGeElementParaType::INT},
    {L"V串夹角(左)",GIMGeElementParaType::DOUBLE},
    {L"V串夹角(右)",GIMGeElementParaType::DOUBLE},
    {L"U串连接长度",GIMGeElementParaType::DOUBLE},
    {L"金具长度(左上)",GIMGeElementParaType::DOUBLE},
    {L"金具长度(右上)",GIMGeElementParaType::DOUBLE},
    {L"金具长度(左下)",GIMGeElementParaType::DOUBLE},
    {L"金具长度(右下)",GIMGeElementParaType::DOUBLE},
    {L"绝缘子片数(左)",GIMGeElementParaType::INT},
    {L"绝缘子片数(右)",GIMGeElementParaType::INT},
    {L"联数",GIMGeElementParaType::INT},
    {L"联间距",GIMGeElementParaType::DOUBLE},
    {L"联排列方式",GIMGeElementParaType::INT},
    {L"绝缘子结构高度",GIMGeElementParaType::DOUBLE},
    {L"重量",GIMGeElementParaType::DOUBLE},
    {L"绝缘子半径",GIMGeElementParaType::DOUBLE},
    {L"绝缘子材质",GIMGeElementParaType::INT},
    {L"均压环个数",GIMGeElementParaType::INT},
    {L"均压环安装位置",GIMGeElementParaType::TEXT},
    {L"均压环高度",GIMGeElementParaType::DOUBLE},
    {L"均压环半径",GIMGeElementParaType::DOUBLE},

     }
    },

'''