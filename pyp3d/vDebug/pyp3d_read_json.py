from .pyp3d_modeling import *
import json  # read json

countNum = int(0)
numReserve=int(0)

def _getVecRound(pos):
    vec = 'Vec3('
    if (numReserve==0):
        vec += str(pos.x)+","
        vec += str(pos.y)+","
        vec += str(pos.z)+'),'
    else:
        vec += str(round(pos.x, numReserve))+","
        vec += str(round(pos.y, numReserve))+","
        vec += str(round(pos.z, numReserve))+'),'
    return vec

def _getGePoint(pos, isCode=True):
    if isCode:
        vec = 'Vec3('
        vec += str(pos["GePoint3d"]["x"])+","
        vec += str(pos["GePoint3d"]["y"])+","
        vec += str(pos["GePoint3d"]["z"])+'),'
        return vec
    else:
        point = Vec3(pos["GePoint3d"]["x"],
                    pos["GePoint3d"]["y"], 
                    pos["GePoint3d"]["z"])
        return point

def _getLineCode(parts):
    global numReserve
    res = ''
    for iter in parts:
        if isinstance(iter, GeVec3d):
            res += _getVecRound(iter)
        elif isinstance(iter, Segment):
            res += 'Segment('
            res += _getVecRound(iter.start)
            res += _getVecRound(iter.end)+'),'
        elif isinstance(iter, (Ellipse, Arc)):
            vecX = get_matrixs_axisx(iter.transformation)
            vecY = get_matrixs_axisy(iter.transformation)
            vecZ = get_matrixs_axisz(iter.transformation)
            pos = get_matrixs_position(iter.transformation)
            scope = iter.scope
            res += 'set_matrix_by_column_vectors('
            res += _getVecRound(vecX)
            res += _getVecRound(vecY)
            res += _getVecRound(vecZ)
            res += _getVecRound(pos)
            res += ')*Arc('
            if (abs(scope-2*pi) > PL_A):
                res += str(round(scope, 6))
            res += '),'
        elif isinstance(iter, SplineCurve):
            res += 'SplineCurve(['
            for point in iter.points:
                res += _getVecRound(point)
            res += '],0,{}),'.format(iter.k)
        else:
            continue
    return res


def _getLineFromGeCurveArray(curve_data):  # , removeCoin=True
    line = []
    for curve in curve_data:
        # Point
        if curve["IGeCurveBase"]["CurveBaseType"] == "CURVE_BASE_TYPE_LineString":
            points = curve["IGeCurveBase"]["pvector<GePoint3d>"]
            for iter in points:
                point = Vec3(iter["GePoint3d"]["x"],
                             iter["GePoint3d"]["y"], 
                             iter["GePoint3d"]["z"])
                if len(line) == 0 or not isinstance(line[-1], GeVec3d) or not is_coincident(point, get_part_end_point(line[-1])):
                    line.append(point)  # line.pop()
        # Segment
        elif curve["IGeCurveBase"]["CurveBaseType"] == "CURVE_BASE_TYPE_Segment":
            segment = curve["IGeCurveBase"]['GeSegment3d']
            pointS = Vec3(segment['point0']["GePoint3d"]["x"], segment['point0']
                          ["GePoint3d"]["y"], segment['point0']["GePoint3d"]["z"])
            pointE = Vec3(segment['point1']["GePoint3d"]["x"], segment['point1']
                          ["GePoint3d"]["y"], segment['point1']["GePoint3d"]["z"])
            line.append(Segment(pointS, pointE))
            # if len(line)==0 or not is_coincident(pointS,get_part_end_point(line[-1])):
            #     line.append(pointS)
            # line.append(Vec3(segment['point1']["GePoint3d"]["x"],segment['point1']["GePoint3d"]["y"],segment['point1']["GePoint3d"]["z"]))
        # Arc
        elif curve["IGeCurveBase"]["CurveBaseType"] == "CURVE_BASE_TYPE_Ellipse":
            ellipse = curve["IGeCurveBase"]["GeEllipse3d"]
            center = ellipse["center"]["GePoint3d"]
            center = Vec3(center["x"], center["y"], center["z"])
            vector0 = ellipse["vector0"]["GeVec3d"]
            vector0 = Vec3(vector0["x"], vector0["y"], vector0["z"])
            vector90 = ellipse["vector90"]["GeVec3d"]
            vector90 = Vec3(vector90["x"], vector90["y"], vector90["z"])
            arc = Ellipse(center, vector0, vector90,
                          ellipse["start"], ellipse["sweep"])
            line.append(arc)
        # Spline
        elif curve["IGeCurveBase"]["CurveBaseType"] == "CURVE_BASE_TYPE_BsplineCurve":
            points = curve["IGeCurveBase"]["GeBsplineCurve"]["poles"]["pvector<GePoint3d>"]
            poles = []
            for point in points:
                poles.append(
                    Vec3(point["GePoint3d"]["x"], point["GePoint3d"]["y"], point["GePoint3d"]["z"]))
            order = curve["IGeCurveBase"]["GeBsplineCurve"]['params']['order']
            spline = SplineCurve(poles, 0, order)
            line.append(spline)
        elif curve["IGeCurveBase"]["CurveBaseType"] == "CURVE_BASE_TYPE_CurveArray":
            line+=_getLineFromGeCurveArray(curve["IGeCurveBase"]['GeCurveArray']["Curves"])
    return line


def _getGeCurveArrayParityRegion(curveArray):
    curves = curveArray["GeCurveArray"]["Curves"]
    sectionList = []
    # for i in range(len(curves)): #default only first is outer
    #     if (i==1):
    #         sectionI = Section(_getLineFromGeCurveArray(
    #                 curves[i]['IGeCurveBase']["GeCurveArray"]["Curves"]))
    #     else:
    #         sectionI = -Section(_getLineFromGeCurveArray(
    #                 curves[i]['IGeCurveBase']["GeCurveArray"]["Curves"]))
    # using outer and inner
    for iter in curves:
        if (iter['IGeCurveBase']["GeCurveArray"]["BoundaryType"] == 'BOUNDARY_TYPE_Outer'):  # outer is positive
            sectionI = Section(_getLineFromGeCurveArray(
                    iter['IGeCurveBase']["GeCurveArray"]["Curves"]))
        else:  # BOUNDARY_TYPE_Inner
            sectionI = -Section(_getLineFromGeCurveArray(
                iter['IGeCurveBase']["GeCurveArray"]["Curves"]))
        # create_geometry(sectionI)
        sectionList.append(sectionI)
    return sectionList


def _getGeSweptBodyInfo(jsonDict, isCode: bool):
    m_path = jsonDict['m_path']
    path = _getLineFromGeCurveArray(m_path["GeCurveArray"]["Curves"])
    m_profile = jsonDict['m_profile']
    if (m_profile["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Outer' or
            m_profile["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Open'):  # single
        profile = _getLineFromGeCurveArray(m_profile["GeCurveArray"]["Curves"])
        section = Section(profile)
        code = 'section=Section('
        code += _getLineCode(profile)+')\n'
    elif (m_profile["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_ParityRegion'):  # nest
        sectionList = _getGeCurveArrayParityRegion(m_profile)
        # create_geometry(Fusion(profiles))
        # for iter in profiles:
        #     create_geometry(iter)
        section = Fusion(sectionList)
        code = 'section=Fusion('
        for iter in sectionList:  # distinguish taiji
            taiji=iter._noumenon_data['\x07_taiji'].this
            code+='Section(' if taiji else '-Section('
            code += _getLineCode(iter.transformation*iter.parts)+'),'
        code += ')\n'
    # output code
    code += 'line=Line('
    code += _getLineCode(path)+')\n'
    global countNum
    code += 'sweep{}=Sweep(section, line)\n'.format(countNum)
    code += 'combine.append(sweep{})\n\n'.format(countNum)
    countNum += 1
    if isCode:
        return code
    else:
        return Sweep(section, Line(path))


def _getGeRotationalSweepInfo(jsonDict, isCode: bool):
    m_baseCurve = jsonDict['m_baseCurve']
    m_axisOfRotation = jsonDict['m_axisOfRotation']
    pos = m_axisOfRotation['GeRay3d']['origin']
    posi = Vec3(pos["GePoint3d"]["x"], pos["GePoint3d"]
                ["y"], pos["GePoint3d"]["z"])
    vec = m_axisOfRotation['GeRay3d']['direction']
    vect = Vec3(vec["GeVec3d"]["x"], vec["GeVec3d"]["y"], vec["GeVec3d"]["z"])
    m_sweepAngle = jsonDict['m_sweepAngle']
    if (m_baseCurve["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Outer'):  # single
        baseCurve = _getLineFromGeCurveArray(
            m_baseCurve["GeCurveArray"]["Curves"])
        section = Section(baseCurve)
        code = 'section=Section('
        code += _getLineCode(baseCurve)+')\n'
    elif (m_baseCurve["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_ParityRegion'):  # nest
        sectionList = _getGeCurveArrayParityRegion(m_baseCurve)
        section = Fusion(sectionList)
        code = 'section=Fusion('
        for iter in sectionList:  # distinguish taiji
            taiji=iter._noumenon_data['\x07_taiji'].this
            code+='Section(' if taiji else '-Section('
            code += _getLineCode(iter.transformation*iter.parts)+'),'
        code += ')\n'
    arc = trans(posi)*get_matrix_from_one_vector(vect)*Arc(m_sweepAngle)
    code += 'line=Line('
    code += _getLineCode([arc])+')\n'
    global countNum
    code += 'swept{}=Swept(section, line)\n'.format(countNum)
    code += 'combine.append(swept{})\n\n'.format(countNum)
    countNum += 1
    if isCode:
        return code
    else:
        return Swept(section, Line(trans(posi)*get_matrix_from_one_vector(vect)*Arc(m_sweepAngle)))


def _getGeLoftedBodyInfo(jsonDict, isCode: bool): # only single section
    m_bottomProfile = jsonDict['m_bottomProfile']
    m_topProfile = jsonDict['m_topProfile']
    m_guidePathGroups = jsonDict['m_guidePathGroups']
    bottomProfile = _getLineFromGeCurveArray(
        m_bottomProfile["GeCurveArray"]["Curves"])
    topProfile = _getLineFromGeCurveArray(
        m_topProfile["GeCurveArray"]["Curves"])
    if (isinstance(bottomProfile[0], GeVec3d) and isinstance(bottomProfile[-1], GeVec3d) and
            is_coincident(bottomProfile[0], bottomProfile[-1])):
        bottomProfile.pop()
    if (isinstance(topProfile[0], GeVec3d) and isinstance(topProfile[-1], GeVec3d) and
            is_coincident(topProfile[0], topProfile[-1])):
        topProfile.pop()
    guideLine = []
    for iter in m_guidePathGroups[0]:  # default single
        guideLine.append(
            Line(_getLineFromGeCurveArray(iter["GeCurveArray"]["Curves"])))
    # code write
    code = ''
    code += 'secBot=Section('
    code += _getLineCode(bottomProfile)+')\n'
    code += 'secTop=Section('
    code += _getLineCode(topProfile)+')\n'
    code += 'guideLine=[\n'
    for iter in guideLine:
        code += '    Line('
        code += _getLineCode(iter.parts)+'),\n'
    code += '    ]\n'
    global countNum
    code += 'lofted{}=Lofted(secBot, secTop, guideLine)\n'.format(countNum)
    code += 'combine.append(lofted{})\n\n'.format(countNum)
    countNum += 1
    if isCode:
        return code
    else:
        # create_geometry(Section(bottomProfile))
        loft = Lofted(Section(bottomProfile), Section(topProfile), guideLine)
        loft.showTest = True
        # create_geometry(loft)
        # print(code)
        return Lofted(Section(bottomProfile), Section(topProfile), guideLine)


def _getGeExtrusionInfo(jsonDict, isCode: bool):
    m_vector = jsonDict['m_extrusionVector']['GeVec3d']
    vector = Vec3(m_vector['x'], m_vector['y'], m_vector['z'])
    m_baseCurve = jsonDict['m_baseCurve']
    if (m_baseCurve["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Outer' or \
            m_baseCurve["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Open'): # single
        baseCurve = _getLineFromGeCurveArray(
            m_baseCurve["GeCurveArray"]["Curves"])
        section = Section(baseCurve)
        code = 'section=Section('
        code += _getLineCode(baseCurve)+')\n'
    elif (m_baseCurve["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_ParityRegion'):  # nest
        if (len(m_baseCurve["GeCurveArray"]["Curves"])==1):
            baseCurve = _getLineFromGeCurveArray(
                m_baseCurve["GeCurveArray"]["Curves"])
            section = Section(baseCurve)
            code = 'section=Section('
            code += _getLineCode(baseCurve)+')\n'
        else:
            sectionList = _getGeCurveArrayParityRegion(m_baseCurve)
            section = Fusion(sectionList)
            code = 'section=Fusion('
            for iter in sectionList:
                taiji=iter._noumenon_data['\x07_taiji'].this
                code+='Section(' if taiji else '-Section('
                code += _getLineCode(iter.transformation*iter.parts)+'),'
            code += ')\n'
    # output code
    global countNum
    vec = _getLineCode([vector])
    code += 'swept{}=Swept(section, {})\n'.format(countNum, vec)
    code += 'combine.append(swept{})\n\n'.format(countNum)
    countNum += 1
    if isCode:
        return code
    else:
        return Swept(section, vector)

def _getGeRuledSweepInfo(jsonDict, isCode: bool):
    m_capped = jsonDict['m_capped']
    m_sectionCurves = jsonDict['m_sectionCurves']
    sectionList=[]
    code = 'sectionList=[\n'
    for iter in m_sectionCurves:
        if (iter["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Outer' or
            iter["GeCurveArray"]['BoundaryType'] == 'BOUNDARY_TYPE_Open'):  # single
            curve = _getLineFromGeCurveArray(iter["GeCurveArray"]["Curves"])
            section = Section(curve)
            sectionList.append(section)
            code += '    Section('
            code += _getLineCode(curve)+'),\n'          
    code+='    ]\n'
    # output code
    global countNum
    code += 'loft{}=Loft(sectionList)\n'.format(countNum)
    code += 'combine.append(loft{})\n\n'.format(countNum)
    countNum += 1
    if isCode:
        return code
    else:
        return Loft(sectionList)

def _getPolyfaceHandleInfo(jsonDict, isCode: bool):
    m_point=jsonDict['m_point']["TemplateVectorGePoint3d"]
    m_pointIndex=jsonDict['m_pointIndex']["TemplateVectorInt"]
    global countNum
    if isCode:
        code=''
        code += 'polyface{}=Polyface()\n'.format(countNum)
        code += 'vertexListO = [\n'
        for iter in m_point:
            code += '    '+_getGePoint(iter,True)+'\n'
        code += ']\n'
        code += 'faceListO = [\n'
        countI=0
        for iter in m_pointIndex:
            code += '    '+str(iter)+','
            countI+=1
            if countI%4==0:
                code+='\n'
        code += ']\n'
        code += 'polyface{}.vertexList = vertexListO\n'.format(countNum)
        code += 'polyface{}.faceList = faceListO\n'.format(countNum)
        code += 'combine.append(polyface{})\n\n'.format(countNum)
        countNum += 1
        return code
    else:
        polyface=Polyface()
        vertexListO = []
        faceListO = []
        for iter in m_point:
            vertexListO.append(_getGePoint(iter,False))
        for iter in m_pointIndex:
            faceListO.append(int(iter))   
        polyface.vertexList = vertexListO
        polyface.faceList = faceListO
        return polyface


# -------------------------------------------------------------------------------------------
#                           main
# -------------------------------------------------------------------------------------------


def _read_json_file(filename: str, isCode: bool) -> Combine:
    combine = Combine()
    lineParts=[]
    code = 'combine=Combine()\n'
    if not os.path.isfile(filename):
        return 
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        graphics_list = data["agenda"]["P3DGraphics"]
        for graphics in graphics_list:
            primitive_list = graphics["P3DGraphic"]
            for primitive in primitive_list:
                entry_type = primitive['EntryType']
                if (entry_type == 'SolidPrimitive'):
                    if (primitive['IGeSolidBase']['GeSolidBaseType'] == 'GeSolidBaseType_SweptBody'):
                        if isCode:
                            code += _getGeSweptBodyInfo(
                                primitive['IGeSolidBase']["GeSweptBodyInfo"], True)
                        else:
                            combine.append(_getGeSweptBodyInfo(
                                primitive['IGeSolidBase']["GeSweptBodyInfo"], False))
                    elif (primitive['IGeSolidBase']['GeSolidBaseType'] == 'GeSolidBaseType_RotationalSweep'):
                        if isCode:
                            code += _getGeRotationalSweepInfo(
                                primitive['IGeSolidBase']["GeRotationalSweepInfo"], True)
                        else:
                            combine.append(_getGeRotationalSweepInfo(
                                primitive['IGeSolidBase']["GeRotationalSweepInfo"], False))
                    elif (primitive['IGeSolidBase']['GeSolidBaseType'] == 'GeSolidBaseType_LoftedBody'):
                        if isCode:
                            code += _getGeLoftedBodyInfo(
                                primitive['IGeSolidBase']["GeLoftedBodyInfo"], True)
                        else:
                            combine.append(_getGeLoftedBodyInfo(
                                primitive['IGeSolidBase']["GeLoftedBodyInfo"], False))
                    elif (primitive['IGeSolidBase']['GeSolidBaseType'] == 'GeSolidBaseType_Extrusion'):
                        if isCode:
                            code += _getGeExtrusionInfo(
                                primitive['IGeSolidBase']["GeExtrusionInfo"], True)
                        else:
                            combine.append(_getGeExtrusionInfo(
                                primitive['IGeSolidBase']["GeExtrusionInfo"], False))
                    # Loft
                    elif (primitive['IGeSolidBase']['GeSolidBaseType'] == 'GeSolidBaseType_RuledSweep'):
                        if isCode:
                            code += _getGeRuledSweepInfo(
                                primitive['IGeSolidBase']["GeRuledSweepInfo"], True)
                        else:
                            combine.append(_getGeRuledSweepInfo(
                                primitive['IGeSolidBase']["GeRuledSweepInfo"], False))
                elif (entry_type == 'GeCurveArray'):
                    curve_data = primitive["GeCurveArray"]["Curves"]
                    if isCode:
                        global countNum
                        code += 'line{}=Line('.format(countNum)
                        code += _getLineCode(_getLineFromGeCurveArray(curve_data))+')\n'
                        code += 'combine.append(line{})\n\n'.format(countNum)
                        countNum += 1
                    else:
                        lineParts+=_getLineFromGeCurveArray(curve_data)
                elif (entry_type == 'Polyface'):
                    curve_data = primitive["PolyfaceHandle"]
                    if isCode:
                        code += _getPolyfaceHandleInfo(curve_data, True)
                    else:
                        combine.append(_getPolyfaceHandleInfo(curve_data, False))

    # create_geometry(geo)
    # for iter in geo.parts:
    #     create_geometry(iter.colorRand())
    if isCode:
        res = "import sys\nimport os\n" + \
            "sys.path.append(os.path.join(os.path.dirname(__file__), '..\\\\'))\n" + \
            "from pyp3d import *"+"\n\n"
        res += code
        res += 'create_geometry(combine)\n# for i in range(len(combine.parts)):\n'
        res += '#     create_geometry(combine.parts[i].colorRand())\n#     print(i)\n\n'
        return res
    else:
        if len(lineParts)!=0:
            combine.append(Line(lineParts))
        return combine


class JsonRead():
    global numReserve
    def __init__(self, filePath: str=""):
        self.representation = 'JsonRead'
        self.filename = filePath
        self.keepDec=numReserve

    def get_geometry(self):
        return _read_json_file(self.filename, False)

    def write_python_code(self, outputPath: str = ''):
        global countNum
        countNum = 0
        code = _read_json_file(self.filename, True)
        if (outputPath == ''):
            addr = self.filename.split('\\')
            addr = addr[-1].split('.')
            if not os.path.isdir('OutputJsonToPython'):
                os.makedirs('OutputJsonToPython')
            with open("OutputJsonToPython\\"+addr[0]+'.py', "w", encoding="UTF8") as file:
                file.write(code)
        else:
            with open(outputPath, "w", encoding="UTF8") as file:
                file.write(code)

    def get_python_code(self):
        return _read_json_file(self.filename, True)


# section=sectionSegmentsToPoints(section)
def sectionSegmentsToPoints(section:Section)->Section:
    if (isinstance(section,Section)):
        sectionList=[]
        for iter in section.parts:
            if (not isinstance(iter, Segment)):
                continue
            sectionList.append(iter.start)
        return Section(section.transformation*sectionList)
    if (isinstance(section,list)):
        sectionList=[]
        for iter in section:
            if (not isinstance(iter, Segment)):
                continue
            sectionList.append(iter.start)
        return sectionList

def show_points_line2(posvec: list, radius=0,length=2):
    geo = Combine()
    if len(posvec) != 2:
        return geo
    if radius == 0:
        radius = 10  
    geo.append(Cone(posvec[0], posvec[0]+length/2*posvec[1], radius/2, radius/2).colorOrange())  # the cyclinder of line.
    mat = get_matrix_from_two_points(posvec[0]+length/2*posvec[1], posvec[0]+length*posvec[1])
    # the Conus arrow of direction.
    geo.append(mat*conus_diameter_height(1.5 * radius, 2*radius).colorCyan())
    create_geometry(geo)
    return geo


    