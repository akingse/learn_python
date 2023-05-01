import re
strEncode = 'GB2312'  # 'utf-8' # vs必须使用2312

# // 变电站换流站 25个
GEOTYPEALL='''
    { L"Sphere", L"球体" },
    { L"RotationalEllipsoid", L"旋转椭球体" },
    { L"Cuboid", L"长方体" },
    { L"Table", L"棱台（锥）" },
    { L"OffsetRectangularTable", L"偏移矩形台" },
    { L"Cylinder", L"圆柱体" },
    { L"BendingCylindrical", L"弯折圆柱" },
    { L"TruncatedCone", L"圆台体" },
    { L"EccentricTruncatedCone", L"偏心圆台体" },
    { L"Ring", L"圆环" },
    { L"RectangularRing", L"矩形环" },
    { L"EllipticRing", L"椭圆环" },
    { L"CircularGasket", L"圆形垫片" },
    { L"TableGasket", L"台型垫片" },
    { L"SquareGasket", L"方形垫片" },
    { L"StretchedBody", L"拉伸体" },
    { L"PorcelainBushing", L"瓷套/绝缘子(未含上下法兰）" },
    { L"ConePorcelainBushing", L"锥形瓷套" },
    { L"Insulator", L"绝缘子串" },
    { L"VTypeInsulator", L"V型绝缘子串" },
    { L"TerminalBlock", L"端子板" },
    { L"Rectangularfixedplate", L"安装矩形开孔板" },
    { L"Circularfixedplate", L"安装圆形开孔板" },
    { L"Wire", L"导线" },
    { L"Cable", L"电缆" },
'''
g_GimGePowertransParaDic ='''
    { L"Sphere", { { L"R", GIMGeElementParaType::DOUBLE } } },
    { L"RotationalEllipsoid", { { L"LR", GIMGeElementParaType::DOUBLE },
    { L"WR", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE } } },
    { L"Cuboid", { { L"L", GIMGeElementParaType::DOUBLE },
    { L"W", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE } } },
    { L"Table", { { L"TL1", GIMGeElementParaType::DOUBLE },
    { L"TL2", GIMGeElementParaType::DOUBLE },
    { L"LL1", GIMGeElementParaType::DOUBLE },
    { L"LL2", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE } } },
    { L"OffsetRectangularTable", { { L"TL", GIMGeElementParaType::DOUBLE },
    { L"TW", GIMGeElementParaType::DOUBLE },
    { L"LL", GIMGeElementParaType::DOUBLE },
    { L"LW", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE },
    { L"XOFF", GIMGeElementParaType::DOUBLE },
    { L"YOFF", GIMGeElementParaType::DOUBLE } } },
    { L"Cylinder", { { L"R", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE } } },
    { L"BendingCylindrical", { { L"R", GIMGeElementParaType::DOUBLE },
    { L"L", GIMGeElementParaType::DOUBLE },
    { L"Rad", GIMGeElementParaType::DOUBLE } } },
    { L"TruncatedCone", { { L"TR", GIMGeElementParaType::DOUBLE },
    { L"BR", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE } } },
    { L"EccentricTruncatedCone", { { L"TR", GIMGeElementParaType::DOUBLE },
    { L"BR", GIMGeElementParaType::DOUBLE },
    { L"H", GIMGeElementParaType::DOUBLE },
    { L"TOPXOFF", GIMGeElementParaType::DOUBLE },
    { L"TOPYOFF", GIMGeElementParaType::DOUBLE } } },
    { L"Ring", { { L"DR", GIMGeElementParaType::DOUBLE },
    { L"R", GIMGeElementParaType::DOUBLE },
    { L"Rad", GIMGeElementParaType::DOUBLE } } },
    { L"RectangularRing", { { L"DR", GIMGeElementParaType::DOUBLE },
    { L"R", GIMGeElementParaType::DOUBLE },
    { L"L", GIMGeElementParaType::DOUBLE },
    { L"W", GIMGeElementParaType::DOUBLE } } },
	{ L"EllipticRing", { { L"DR", GIMGeElementParaType::DOUBLE },
	{ L"W", GIMGeElementParaType::DOUBLE },
	{ L"L", GIMGeElementParaType::DOUBLE } } },
	{ L"CircularGasket", { { L"OR", GIMGeElementParaType::DOUBLE },
	{ L"IR", GIMGeElementParaType::DOUBLE },
	{ L"H", GIMGeElementParaType::DOUBLE },
	{ L"Rad", GIMGeElementParaType::DOUBLE } } },
	{ L"TableGasket", { { L"TR", GIMGeElementParaType::DOUBLE },
	{ L"OR", GIMGeElementParaType::DOUBLE },
	{ L"IR", GIMGeElementParaType::DOUBLE },
	{ L"H", GIMGeElementParaType::DOUBLE },
	{ L"Rad", GIMGeElementParaType::DOUBLE } } },
	{ L"SquareGasket", { { L"L1", GIMGeElementParaType::DOUBLE },
	{ L"W1", GIMGeElementParaType::DOUBLE },
	{ L"L2", GIMGeElementParaType::DOUBLE },
	{ L"W2", GIMGeElementParaType::DOUBLE },
	{ L"H", GIMGeElementParaType::DOUBLE },
	{ L"CT", GIMGeElementParaType::INT },
	{ L"Rad", GIMGeElementParaType::DOUBLE },
	{ L"CL", GIMGeElementParaType::DOUBLE } } },
	{ L"StretchedBody", { { L"Array", GIMGeElementParaType::TEXT },
	{ L"Normal", GIMGeElementParaType::TEXT },
	{ L"L", GIMGeElementParaType::DOUBLE } } },
	{ L"PorcelainBushing", { { L"H", GIMGeElementParaType::DOUBLE },
	{ L"R", GIMGeElementParaType::DOUBLE },
	{ L"R1", GIMGeElementParaType::DOUBLE },
	{ L"R2", GIMGeElementParaType::DOUBLE },
	{ L"N", GIMGeElementParaType::INT } } },
	{ L"ConePorcelainBushing", { { L"H", GIMGeElementParaType::DOUBLE },
	{ L"BR", GIMGeElementParaType::DOUBLE },
	{ L"TR", GIMGeElementParaType::DOUBLE },
	{ L"BR1", GIMGeElementParaType::DOUBLE },
	{ L"BR2", GIMGeElementParaType::DOUBLE },
	{ L"TR1", GIMGeElementParaType::DOUBLE },
	{ L"TR2", GIMGeElementParaType::DOUBLE },
	{ L"N", GIMGeElementParaType::INT } } },
	{ L"Insulator", { { L"N", GIMGeElementParaType::INT },
	{ L"D", GIMGeElementParaType::DOUBLE },
	{ L"N1", GIMGeElementParaType::INT },
	{ L"H1", GIMGeElementParaType::DOUBLE },
	{ L"R1", GIMGeElementParaType::DOUBLE },
	{ L"R2", GIMGeElementParaType::DOUBLE },
	{ L"R", GIMGeElementParaType::DOUBLE },
	{ L"FL", GIMGeElementParaType::DOUBLE },
	{ L"AL", GIMGeElementParaType::DOUBLE },
	{ L"LN", GIMGeElementParaType::INT } } },
	{ L"VTypeInsulator", { { L"X", GIMGeElementParaType::DOUBLE },
	{ L"AD", GIMGeElementParaType::DOUBLE },
	{ L"N1", GIMGeElementParaType::INT },
	{ L"H1", GIMGeElementParaType::DOUBLE },
	{ L"R", GIMGeElementParaType::DOUBLE },
	{ L"R1", GIMGeElementParaType::DOUBLE },
	{ L"R2", GIMGeElementParaType::DOUBLE },
	{ L"FL", GIMGeElementParaType::DOUBLE },
	{ L"AL", GIMGeElementParaType::DOUBLE },
	{ L"LN", GIMGeElementParaType::INT } } },
	{ L"TerminalBlock", { { L"L", GIMGeElementParaType::DOUBLE },
	{ L"W", GIMGeElementParaType::DOUBLE },
	{ L"T", GIMGeElementParaType::DOUBLE },
	{ L"CL", GIMGeElementParaType::DOUBLE },
	{ L"CS", GIMGeElementParaType::DOUBLE },
	{ L"RS", GIMGeElementParaType::DOUBLE },
	{ L"R", GIMGeElementParaType::DOUBLE },
	{ L"CN", GIMGeElementParaType::INT },
	{ L"RN", GIMGeElementParaType::INT },
	{ L"BL", GIMGeElementParaType::DOUBLE },
	{ L"Phase", GIMGeElementParaType::TEXT } } },
	{ L"Rectangularfixedplate", { { L"L", GIMGeElementParaType::DOUBLE },
	{ L"W", GIMGeElementParaType::DOUBLE },
	{ L"T", GIMGeElementParaType::DOUBLE },
	{ L"CS", GIMGeElementParaType::DOUBLE },
	{ L"RS", GIMGeElementParaType::DOUBLE },
	{ L"CN", GIMGeElementParaType::INT },
	{ L"RN", GIMGeElementParaType::INT },
	{ L"MH", GIMGeElementParaType::INT },
	{ L"D", GIMGeElementParaType::DOUBLE } } },
	{ L"Circularfixedplate", { { L"L", GIMGeElementParaType::DOUBLE },
	{ L"W", GIMGeElementParaType::DOUBLE },
	{ L"T", GIMGeElementParaType::DOUBLE },
	{ L"CS", GIMGeElementParaType::DOUBLE },
	{ L"N", GIMGeElementParaType::INT },
	{ L"MH", GIMGeElementParaType::INT },
	{ L"D", GIMGeElementParaType::DOUBLE } } },
	{ L"Wire", { { L"StartCoord", GIMGeElementParaType::TEXT },
	{ L"EndCoord", GIMGeElementParaType::TEXT },
	{ L"StartVector", GIMGeElementParaType::TEXT },
	{ L"EndVector", GIMGeElementParaType::TEXT },
	{ L"Sag", GIMGeElementParaType::DOUBLE },
	{ L"D", GIMGeElementParaType::DOUBLE },
	{ L"FitCoordArray", GIMGeElementParaType::TEXT } } },
	{ L"Cable", { { L"StartCoord", GIMGeElementParaType::TEXT },
	{ L"EndCoord", GIMGeElementParaType::TEXT },
	{ L"InflectionCoordArray", GIMGeElementParaType::TEXT },
	{ L"IRArray", GIMGeElementParaType::DOUBLE },
	{ L"D", GIMGeElementParaType::DOUBLE } } },

'''
g_GimGePowertransParaDic4Property ='''
	{ L"Sphere", { { L"半径 R", GIMGeElementParaType::DOUBLE } } },
	{ L"RotationalEllipsoid", { { L"极半径 LR", GIMGeElementParaType::DOUBLE },
	{ L"赤道半径 WR", GIMGeElementParaType::DOUBLE },
	{ L"横切高度 H", GIMGeElementParaType::DOUBLE } } },
	{ L"Cuboid", { { L"长 L", GIMGeElementParaType::DOUBLE },
	{ L"宽 W", GIMGeElementParaType::DOUBLE },
	{ L"高 H", GIMGeElementParaType::DOUBLE } } },
	{ L"Table", { { L"顶面对角线长1 TL1", GIMGeElementParaType::DOUBLE },
	{ L"顶面对角线长2 TL2", GIMGeElementParaType::DOUBLE },
	{ L"底面对角线长1 LL1", GIMGeElementParaType::DOUBLE },
	{ L"底面对角线长2 LL2", GIMGeElementParaType::DOUBLE },
	{ L"高 H", GIMGeElementParaType::DOUBLE } } },
	{ L"OffsetRectangularTable", { { L"顶面长 TL", GIMGeElementParaType::DOUBLE },
	{ L"顶面宽 TW", GIMGeElementParaType::DOUBLE },
	{ L"底面长 LL", GIMGeElementParaType::DOUBLE },
	{ L"底面宽 LW", GIMGeElementParaType::DOUBLE },
	{ L"高度 H", GIMGeElementParaType::DOUBLE },
	{ L"顶面中心相对底面中心的X方向偏移量 XOFF", GIMGeElementParaType::DOUBLE },
	{ L"顶面中心相对底面中心的Y方向偏移量 YOFF", GIMGeElementParaType::DOUBLE } } },
	{ L"Cylinder", { { L"半径 R", GIMGeElementParaType::DOUBLE },
	{ L"高度 H", GIMGeElementParaType::DOUBLE } } },
	{ L"BendingCylindrical", { { L"半径 R", GIMGeElementParaType::DOUBLE },
	{ L"接头长度 L", GIMGeElementParaType::DOUBLE },
	{ L"弯折角度 Deg", GIMGeElementParaType::DOUBLE } } },
	{ L"TruncatedCone", { { L"顶面半径 TR", GIMGeElementParaType::DOUBLE },
	{ L"底面半径 BR", GIMGeElementParaType::DOUBLE },
	{ L"高度 H", GIMGeElementParaType::DOUBLE } } },
	{ L"EccentricTruncatedCone", { { L"顶面半径 TR", GIMGeElementParaType::DOUBLE },
	{ L"底面半径 BR", GIMGeElementParaType::DOUBLE },
	{ L"圆台体高度 H", GIMGeElementParaType::DOUBLE },
	{ L"顶面圆心X轴方向偏移量 TOPXOFF", GIMGeElementParaType::DOUBLE },
	{ L"顶面圆心Y轴方向偏移量 TOPYOFF", GIMGeElementParaType::DOUBLE } } },
	{ L"Ring", { { L"管半径 DR", GIMGeElementParaType::DOUBLE },
	{ L"圆环半径 R", GIMGeElementParaType::DOUBLE },
	{ L"角度 Deg", GIMGeElementParaType::DOUBLE } } },
	{ L"RectangularRing", { { L"管半径 DR", GIMGeElementParaType::DOUBLE },
	{ L"倒角半径 R", GIMGeElementParaType::DOUBLE },
	{ L"环长度 L", GIMGeElementParaType::DOUBLE },
	{ L"环宽度 W", GIMGeElementParaType::DOUBLE } } },
	{ L"EllipticRing", { { L"管半径 DR", GIMGeElementParaType::DOUBLE },
	{ L"椭圆短半轴 W", GIMGeElementParaType::DOUBLE },
	{ L"椭圆长半轴 L", GIMGeElementParaType::DOUBLE } } },
	{ L"CircularGasket", { { L"外围半径 OR", GIMGeElementParaType::DOUBLE },
	{ L"内围半径 IR", GIMGeElementParaType::DOUBLE },
	{ L"高度 H", GIMGeElementParaType::DOUBLE },
	{ L"角度用来表示转弯的角度 Deg", GIMGeElementParaType::DOUBLE } } },
	{ L"TableGasket", { { L"顶部外围半径 TR", GIMGeElementParaType::DOUBLE },
	{ L"底部外围半径 OR", GIMGeElementParaType::DOUBLE },
	{ L"内围半径 IR", GIMGeElementParaType::DOUBLE },
	{ L"高度 H", GIMGeElementParaType::DOUBLE },
	{ L"角度用来表示转弯的角度 Deg", GIMGeElementParaType::DOUBLE } } },
	{ L"SquareGasket", { { L"外围长 L1", GIMGeElementParaType::DOUBLE },
	{ L"外围宽 W1", GIMGeElementParaType::DOUBLE },
	{ L"内围长 L2", GIMGeElementParaType::DOUBLE },
	{ L"内围宽 W2", GIMGeElementParaType::DOUBLE },
	{ L"高度 H", GIMGeElementParaType::DOUBLE },
	{ L"倒角类型 CT", GIMGeElementParaType::INT },
	{ L"倒角半径 Rad", GIMGeElementParaType::DOUBLE },
	{ L"倒角边长 CL", GIMGeElementParaType::DOUBLE } } },
	{ L"StretchedBody", { { L"顶点坐标 Array", GIMGeElementParaType::TEXT },
	{ L"拉伸方向 Normal", GIMGeElementParaType::TEXT },
	{ L"拉伸长度 L", GIMGeElementParaType::DOUBLE } } },
	{ L"PorcelainBushing", { { L"瓷套高度 H", GIMGeElementParaType::DOUBLE },
	{ L"瓷套外半径 R", GIMGeElementParaType::DOUBLE },
	{ L"大伞裙半径 R1", GIMGeElementParaType::DOUBLE },
	{ L"小伞裙半径 R2", GIMGeElementParaType::DOUBLE },
	{ L"片数 N", GIMGeElementParaType::INT } } },
	{ L"ConePorcelainBushing", { { L"瓷套高度 H", GIMGeElementParaType::DOUBLE },
	{ L"底部绝缘子半径 BR", GIMGeElementParaType::DOUBLE },
	{ L"顶部绝缘子半径 TR", GIMGeElementParaType::DOUBLE },
	{ L"底部伞裙半径1 BR1", GIMGeElementParaType::DOUBLE },
	{ L"底部伞裙半径2 BR2", GIMGeElementParaType::DOUBLE },
	{ L"顶部伞裙半径 TR1", GIMGeElementParaType::DOUBLE },
	{ L"顶部伞裙半径 TR2", GIMGeElementParaType::DOUBLE },
	{ L"片数 N", GIMGeElementParaType::INT } } },
	{ L"Insulator", { { L"联数 N", GIMGeElementParaType::INT },
	{ L"双串间距 D", GIMGeElementParaType::DOUBLE },
	{ L"单串绝缘子片数量 N1", GIMGeElementParaType::INT },
	{ L"绝缘子单片连接高度 H1", GIMGeElementParaType::DOUBLE },
	{ L"大伞裙半径 R1", GIMGeElementParaType::DOUBLE },
	{ L"小伞裙半径 R2", GIMGeElementParaType::DOUBLE },
	{ L"绝缘子半径 R", GIMGeElementParaType::DOUBLE },
	{ L"前端长度(架构端) FL", GIMGeElementParaType::DOUBLE },
	{ L"后端长度(导线端) AL", GIMGeElementParaType::DOUBLE },
	{ L"连接导线分裂数 LN", GIMGeElementParaType::INT } } },
	{ L"VTypeInsulator", { { L"前端间距 X", GIMGeElementParaType::DOUBLE },
	{ L"后端间距 AD", GIMGeElementParaType::DOUBLE },
	{ L"单串绝缘子片数量 N1", GIMGeElementParaType::INT },
	{ L"绝缘子单片连接高度 H1", GIMGeElementParaType::DOUBLE },
	{ L"伞顶面半径 R", GIMGeElementParaType::DOUBLE },
	{ L"大伞半径 R1", GIMGeElementParaType::DOUBLE },
	{ L"小伞半径 R2", GIMGeElementParaType::DOUBLE },
	{ L"前端长度(架构端) FL", GIMGeElementParaType::DOUBLE },
	{ L"后端长度(导线端) AL", GIMGeElementParaType::DOUBLE },
	{ L"连接导线分裂数 LN", GIMGeElementParaType::INT } } },
	{ L"TerminalBlock", { { L"长度 L", GIMGeElementParaType::DOUBLE },
	{ L"宽度 W", GIMGeElementParaType::DOUBLE },
	{ L"厚度 T", GIMGeElementParaType::DOUBLE },
	{ L"倒角边长 CL", GIMGeElementParaType::DOUBLE },
	{ L"孔列间距 CS", GIMGeElementParaType::DOUBLE },
	{ L"孔行间距 RS", GIMGeElementParaType::DOUBLE },
	{ L"孔半径 R", GIMGeElementParaType::DOUBLE },
	{ L"列孔个数 CN", GIMGeElementParaType::INT },
	{ L"行孔个数 RN", GIMGeElementParaType::INT },
	{ L"孔行距底边距离 BL", GIMGeElementParaType::DOUBLE },
	{ L"Phase", GIMGeElementParaType::TEXT } } },
	{ L"Rectangularfixedplate", { { L"长度 L", GIMGeElementParaType::DOUBLE },
	{ L"宽度 W", GIMGeElementParaType::DOUBLE },
	{ L"厚度 T", GIMGeElementParaType::DOUBLE },
	{ L"孔列间距 CS", GIMGeElementParaType::DOUBLE },
	{ L"孔行间距 RS", GIMGeElementParaType::DOUBLE },
	{ L"列孔个数 CN", GIMGeElementParaType::INT },
	{ L"行孔个数 RN", GIMGeElementParaType::INT },
	{ L"孔深度 MH", GIMGeElementParaType::INT },
	{ L"孔直径 D", GIMGeElementParaType::DOUBLE } } },
	{ L"Circularfixedplate", { { L"长度 L", GIMGeElementParaType::DOUBLE },
	{ L"宽度 W", GIMGeElementParaType::DOUBLE },
	{ L"厚度 T", GIMGeElementParaType::DOUBLE },
	{ L"开孔环半径 CS", GIMGeElementParaType::DOUBLE },
	{ L"孔个数 N", GIMGeElementParaType::INT },
	{ L"孔深度 MH", GIMGeElementParaType::INT },
	{ L"孔直径 D", GIMGeElementParaType::DOUBLE } } },
	{ L"Wire", { { L"StartCoord", GIMGeElementParaType::TEXT },
	{ L"EndCoord", GIMGeElementParaType::TEXT },
	{ L"StartVector", GIMGeElementParaType::TEXT },
	{ L"EndVector", GIMGeElementParaType::TEXT },
	{ L"Sag", GIMGeElementParaType::DOUBLE },
	{ L"D", GIMGeElementParaType::DOUBLE },
	{ L"FitCoordArray", GIMGeElementParaType::TEXT } } },
	{ L"Cable", { { L"StartCoord", GIMGeElementParaType::TEXT },
	{ L"EndCoord", GIMGeElementParaType::TEXT },
	{ L"InflectionCoordArray", GIMGeElementParaType::TEXT },
	{ L"IRArray", GIMGeElementParaType::DOUBLE },
	{ L"D", GIMGeElementParaType::DOUBLE } } },
'''

# GEODICT=re.findall(r"L\".+?\"", GEOTYPEALL)
GEODICT0=re.findall(r"{\sL.+?}", GEOTYPEALL)
GEODICT_NAME=[]
for iter in GEODICT0:
    arg0 = re.sub(r'{|}', '', iter)
    arg1 = re.sub(r' |L|\'|\"', '', arg0)
    # GEODICT1.append(arg1)
    GEODICT_NAME.append(arg1.split(','))


# GEODICT2=re.findall(r"{\s{\sL|\n|.+?\s}\s}\s},", g_GimGePowertransParaDic)
GEODICT2=g_GimGePowertransParaDic.split('\n')
GEODICT3=[]
for i in range(len(GEODICT2)-1):
    if GEODICT2[i].find("{ { L")!=-1:
        if len(re.findall(r"{\s{\s.+?\s}\s}\s}", GEODICT2[i]))!=0:
            GEODICT3.append(GEODICT2[i])
            continue
        temp=GEODICT2[i]
        while GEODICT2[i].find("} } }")==-1 :
            if (i!=len(GEODICT2)-1):
                i+=1
            temp+=GEODICT2[i]
        GEODICT3.append(temp)

GEODICT_ENG=[]
for iter in GEODICT3:
    arg0 = re.sub(r'{|}|\sL\"|\'|\"|\s', '', iter)
    arg1 = re.sub(r'GIMGeElementParaType::DOUBLE', 'double', arg0)
    arg2 = re.sub(r'GIMGeElementParaType::INT', 'int', arg1)
    arg3 = re.sub(r'GIMGeElementParaType::TEXT', 'BPParaVec', arg2)
    GEODICT_ENG.append(arg3)

GEODICT2=g_GimGePowertransParaDic4Property.split('\n')
GEODICT3=[]
for i in range(len(GEODICT2)-1):
    if GEODICT2[i].find("{ { L")!=-1:
        if len(re.findall(r"{\s{\s.+?\s}\s}\s}", GEODICT2[i]))!=0:
            GEODICT3.append(GEODICT2[i])
            continue
        temp=GEODICT2[i]
        while GEODICT2[i].find("} } }")==-1 :
            if (i!=len(GEODICT2)-1):
                i+=1
            temp+=GEODICT2[i]
        GEODICT3.append(temp)
GEODICT_CN=[]
for iter in GEODICT3:
    arg0 = re.sub(r'\{\sL\"|\'|\"|\t|{|}', '', iter)
    arg1 = re.sub(r'GIMGeElementParaType::DOUBLE', 'double', arg0)
    arg2 = re.sub(r'GIMGeElementParaType::INT', 'int', arg1)
    arg3 = re.sub(r'GIMGeElementParaType::TEXT', 'BPParaVec', arg2)
    GEODICT_CN.append(arg3)

GEODICT_ALL=[]
AUTO=[]
for i in range(len(GEODICT_NAME)):
    AUTO.append([GEODICT_NAME[i][0],101+i,GEODICT_NAME[i][1]])

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
    sz=len(engKey)/2-1
    for k in range(int(sz)):
        value=[engKey[2+2*k],cnKey[1+2*k].lstrip().rstrip(),engKey[1+2*k]]
        PRODICT[engKey[1+2*k]]=value
    GEODICT_ALL.append(PRODICT)


from test_re02_GIM import auto_generate
for i in range(len(GEODICT_NAME)):
    auto_generate(AUTO[i],GEODICT_ALL[i])
