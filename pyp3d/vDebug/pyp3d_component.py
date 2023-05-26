# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: YouQi akingse
# Date: 2021/08/07
from .pyp3d_point_set import *
set_global_variable('is_script_to_josn', False)


def create_geometry(noumenon: Noumenon):  # 在全局坐标系的原点创建一个几何体
    '''
    create a geometry at the origin of the global coordinate system
    '''
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_CREATE_GEOMETRY)(noumenon)


# ------------------------------------------------------------------------------------------
# |                                         STYLE                                          |
# ------------------------------------------------------------------------------------------


class Style(Noumenon):
    def __init__(self):
        Noumenon.__init__(self)
        self.transformation = GeTransform()
        self.version = '0'
        self.representation = 'Style'

    @property
    def representation(self):
        return self[PARACMPT_KEYWORD_REPRESENTATION]

    @representation.setter
    def representation(self, name):
        if not isinstance(name, str):
            raise TypeError('improper type!')
        self[PARACMPT_KEYWORD_REPRESENTATION] = name

    @property
    def version(self):
        return self[PARACMPT_KEYWORD_REPRESENTATION]

    @version.setter
    def version(self, name):
        if not isinstance(name, str):
            raise TypeError('improper type!')
        self[PARACMPT_STYLE_VERSION] = name


class Symbology(Style):
    def __init__(self, color=P3DColorDef(0.5, 0.5, 0.5, 1.0), weight=1, style=0):
        Style.__init__(self)
        self.representation = 'Symbology'
        self.color = color
        self.weight = weight
        self.style = style

    @property
    def color(self):
        return self[PARACMPT_SYMBOLOGY_COLOR]

    @color.setter
    def color(self, clr):
        self[PARACMPT_SYMBOLOGY_COLOR] = clr

    @property
    def weight(self):
        return self[PARACMPT_SYMBOLOGY_WEIGHT]

    @weight.setter
    def weight(self, wei):
        self[PARACMPT_SYMBOLOGY_WEIGHT] = wei

    @property
    def style(self):
        return self[PARACMPT_SYMBOLOGY_STYLE]

    @style.setter
    def style(self, sty):
        if not isinstance(sty, int):
            raise TypeError('input error type, input int')
        if sty < 0 or sty > 7:
            raise TypeError(
                'input error value, input 0:实线,1:点线,2:短虚线,3:虚线（比短虚线长）,4:点画线（稀疏一点，线长一点）,\
                     5:虚线，比2短虚线更短一点, 6:双点画线, 7:点画线（密集一点，线短一点）')
        self[PARACMPT_SYMBOLOGY_STYLE] = sty


class Material(Style):
    def __init__(self, name=''):
        Style.__init__(self)
        self.representation = 'Material'
        self.name = name

    @property
    def name(self):
        return self[PARACMPT_MATERIAL_NAME]

    @name.setter
    def name(self, name):
        self[PARACMPT_MATERIAL_NAME] = name


class Font(Style):
    def __init__(self):
        Style.__init__(self)
        self.representation = 'Font'
        self.size = 1
        self.horzscale = 1
        self.vertscale = 1

    @property
    def size(self):
        return self[PARACMPT_FONT_SIZE]

    @size.setter
    def size(self, size):
        self[PARACMPT_FONT_SIZE] = float(size)

    @property
    def horzscale(self):
        return self[PARACMPT_FONT_HORZ_SCALE]

    @horzscale.setter
    def horzscale(self, size):
        self[PARACMPT_FONT_HORZ_SCALE] = float(size)

    @property
    def vertscale(self):
        return self[PARACMPT_FONT_VERT_SCALE]

    @vertscale.setter
    def vertscale(self, size):
        self[PARACMPT_FONT_VERT_SCALE] = float(size)

    @property
    def font_name(self):
        return self[PARACMPT_FONT_NAME]

    @font_name.setter
    def font_name(self, name):
        self[PARACMPT_FONT_NAME] = str(name)
        self[PARACMPT_FONT_TYPE] = "TrueType"

    @property
    def font_big_name(self):
        return self[PARACMPT_FONT_NAME_BIG]

    @font_big_name.setter
    def font_big_name(self, name):
        self[PARACMPT_FONT_NAME_BIG] = str(name)
        self[PARACMPT_FONT_TYPE_BIG] = "TrueType"

# ------------------------------------------------------------------------------------------
# |                                       NOUMENON                                         |
# ------------------------------------------------------------------------------------------


class Graphics(Noumenon):
    def __init__(self):
        Noumenon.__init__(self)
        self.transformation = GeTransform()
        self[PARACMPT_KEYWORD_TAIJI] = True
        self.representation = 'Graphics'

    def __rmul__(self, a):
        if not isinstance(a, GeTransform):
            raise TypeError('improper type!')
        c = copy.deepcopy(self)
        c.transformation = a * self.transformation
        return c

    def __neg__(self):
        c = copy.deepcopy(self)
        c[PARACMPT_KEYWORD_TAIJI] = not self[PARACMPT_KEYWORD_TAIJI]
        return c

    def __abs__(self):
        c = copy.deepcopy(self)
        c[PARACMPT_KEYWORD_TAIJI] = True
        return c

    def __add__(self, other): return other.__radd__(self)
    def __radd__(self, other): return Fusion(
        copy.deepcopy(other), copy.deepcopy(self))

    def __sub__(self, other): return other.__rsub__(self)

    def __rsub__(self, other): return Fusion(
        copy.deepcopy(other), -copy.deepcopy(self))

    def rmul(self, mat: GeTransform):  # right multiply matrix
        self.transformation = self.transformation*mat

    @property
    def representation(self):
        return self[PARACMPT_KEYWORD_REPRESENTATION]

    @representation.setter
    def representation(self, name):
        if not isinstance(name, str):
            raise TypeError('improper type!')
        self[PARACMPT_KEYWORD_REPRESENTATION] = name

    @property
    def transformation(self):
        return self[PARACMPT_KEYWORD_TRANSFORMATION]

    @transformation.setter
    def transformation(self, val):
        if not isinstance(val, GeTransform):
            raise TypeError('improper type!')
        self[PARACMPT_KEYWORD_TRANSFORMATION] = Attr(val)


class NonComponent(Noumenon):
    def __init__(self):
        Noumenon.__init__(self)
        self[PARACMPT_KEYWORD_SOURCE] = ''
        self.schemaName, self.className, self.representation = 'PBM_CoreModel', 'BPGraphicElementParametricComponent', 'NonComponent'

    def replace(self):
        if not PARACMPT_KEYWORD_REPLACE in self:
            return
        if isinstance(self[PARACMPT_KEYWORD_REPLACE], UnifiedFunction):
            self[PARACMPT_KEYWORD_REPLACE].call(self)
        elif isinstance(self[PARACMPT_KEYWORD_REPLACE], FunctionType):
            self[PARACMPT_KEYWORD_REPLACE](self)
        else:
            raise TypeError('Type Error!')

    def interact(self): ...

    def __abs__(self):
        c = copy.deepcopy(self)
        c[PARACMPT_KEYWORD_TAIJI] = True
        return c

    def __add__(self, other): return other.__radd__(self)
    def __radd__(self, other): return Fusion(
        copy.deepcopy(other), copy.deepcopy(self))

    def __sub__(self, other): return other.__rsub__(self)

    def __rsub__(self, other): return Fusion(
        copy.deepcopy(other), -copy.deepcopy(self))

    @property
    def schemaName(self):
        return self[PARACMPT_KEYWORD_SCHEMA_NAME]

    @schemaName.setter
    def schemaName(self, val):
        self[PARACMPT_KEYWORD_SCHEMA_NAME] = val

    @property
    def className(self):
        return self[PARACMPT_KEYWORD_CLASS_NAME]

    @className.setter
    def className(self, val):
        self[PARACMPT_KEYWORD_CLASS_NAME] = val

    @property
    def name(self):
        return self[PARACMPT_KEYWORD_NAME]

    @name.setter
    def name(self, val):
        self[PARACMPT_KEYWORD_NAME] = val

    @property
    def representation(self):
        return self[PARACMPT_KEYWORD_REPRESENTATION]

    @representation.setter
    def representation(self, name):
        if not isinstance(name, str):
            raise TypeError('improper type!')
        self[PARACMPT_KEYWORD_REPRESENTATION] = name


class Component(Graphics):
    def __init__(self):
        Graphics.__init__(self)
        self[PARACMPT_KEYWORD_SOURCE] = ''
        self.schemaName, self.className, self.representation = 'PBM_CoreModel', 'BPGraphicElementParametricComponent', 'Component'

    def replace(self):
        if not PARACMPT_KEYWORD_REPLACE in self:
            return
        if isinstance(self[PARACMPT_KEYWORD_REPLACE], UnifiedFunction):
            self[PARACMPT_KEYWORD_REPLACE].call(self)
        elif isinstance(self[PARACMPT_KEYWORD_REPLACE], FunctionType):
            self[PARACMPT_KEYWORD_REPLACE](self)
        else:
            raise TypeError('Type Error!')

    def interact(self): ...

    @property
    def schemaName(self):
        return self[PARACMPT_KEYWORD_SCHEMA_NAME]

    @schemaName.setter
    def schemaName(self, val):
        self[PARACMPT_KEYWORD_SCHEMA_NAME] = val

    @property
    def className(self):
        return self[PARACMPT_KEYWORD_CLASS_NAME]

    @className.setter
    def className(self, val):
        self[PARACMPT_KEYWORD_CLASS_NAME] = val

    @property
    def name(self):
        return self[PARACMPT_KEYWORD_NAME]

    @name.setter
    def name(self, val):
        self[PARACMPT_KEYWORD_NAME] = val


class Primitives(Graphics):
    def __init__(self):
        Graphics.__init__(self)
        self[PARACMPT_KEYWORD_STYLE], self.extractGraphics, self.representation = Symbology(
        ), UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_CUSTOM_TO_GRAPHICS), 'Primitives'

    def material(self, name):
        self[PARACMPT_KEYWORD_STYLE] = Material(name)
        return self

    def color(self, *args):
        if len(args) == 0:
            color = P3DColorDef(0.5, 0.5, 0.5, 1)
        elif len(args) == 1 and isinstance(args[0], (list, tuple)):
            if len(args[0]) == 4:
                color = P3DColorDef(
                    args[0][0], args[0][1], args[0][2], args[0][3])
            elif len(args[0]) == 3:
                color = P3DColorDef(args[0][0], args[0][1], args[0][2], 1)
        elif len(args) == 2 and isinstance(args[0], (list, tuple)) and isinstance(args[1], (int, float)):
            color = P3DColorDef(args[0][0], args[0][1], args[0][2], args[1])
        elif len(args) == 3 and isinstance(args[0]+args[1]+args[2], (int, float)):
            color = P3DColorDef(args[0], args[1], args[2], 1)
        elif len(args) == 4 and isinstance(args[0]+args[1]+args[2]+args[3], (int, float)):
            color = P3DColorDef(args[0], args[1], args[2], args[3])
        else:
            raise TypeError('please input proper RGBA value!')
        self[PARACMPT_KEYWORD_STYLE].color = color
        return self

    @property
    def extractGraphics(self):
        return self[PARACMPT_KEYWORD_EXTRACT_GRAPHICS]

    @extractGraphics.setter
    def extractGraphics(self, val):
        if not isinstance(val, UnifiedFunction):
            raise TypeError('improper type!')
        self[PARACMPT_KEYWORD_EXTRACT_GRAPHICS] = val

    def colorRed(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(1, 0, 0, A)
        return self

    def colorGreen(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(0, 1, 0, A)
        return self

    def colorBlue(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(0, 0, 1, A)
        return self

    def colorYellow(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(1, 1, 0, A)
        return self

    def colorMagenta(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(1, 0, 1, A)
        return self

    def colorCyan(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(0, 1, 1, A)
        return self

    def colorPurple(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(0.5, 0, 0.5, A)
        return self

    def colorOrange(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(1, 0.5, 0, A)
        return self

    def colorBlack(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(0, 0, 0, A)
        return self

    def colorWhite(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(1, 1, 1, A)
        return self

    def colorGray(self, A=1):
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(0.5, 0.5, 0.5, A)
        return self

    def colorRand(self, A=1, isOutput=False):  # 随机颜色
        colored = (random(), random(), random())
        if isOutput:
            print("current_color_rgb=", colored)  # to record
        self[PARACMPT_KEYWORD_STYLE].color = P3DColorDef(
            colored[0], colored[1], colored[2], A)
        return self


# ------------------------------------------------------------------------------------------
# |                                       PRIMITIVE                                        |
# ------------------------------------------------------------------------------------------


class GePoint(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Point'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_POINT_TO_GRAPHICS)
        if len(args) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
        elif len(args) == 1:
            if len(args[0]) == 2:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = 0
            elif len(args[0]) == 3:
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            else:
                raise ValueError('Point parameter error!')
        elif len(args) == 2:
            self.x = float(args[0])
            self.y = float(args[1])
        elif len(args) == 3:
            self.x = float(args[0])
            self.y = float(args[1])
            self.z = float(args[2])
        else:
            raise ValueError('Point parameter error!')

    @property
    def x(self): return self[PARACMPT_KEYWORD_TRANSFORMATION]._mat[0][3]

    @x.setter
    def x(self, val): self[PARACMPT_KEYWORD_TRANSFORMATION]._mat[0][3] = float(
        val)

    @property
    def y(self): return self[PARACMPT_KEYWORD_TRANSFORMATION]._mat[1][3]

    @y.setter
    def y(self, val): self[PARACMPT_KEYWORD_TRANSFORMATION]._mat[1][3] = float(
        val)

    @property
    def z(self): return self[PARACMPT_KEYWORD_TRANSFORMATION]._mat[2][3]

    @z.setter
    def z(self, val): self[PARACMPT_KEYWORD_TRANSFORMATION]._mat[2][3] = float(
        val)


class Arc(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Arc'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_ARC_TO_GRAPHICS)
        if len(args) == 0:
            self.scope = 2.0 * pi
        elif len(args) == 1 and is_all_num(args):
            self.scope = float(args[0])
        # three points arc, default on XoY plane.
        elif (len(args) == 1 or len(args) == 3) and is_all_vec(args):
            if len(args) == 1:
                args = args[0]
            if norm(args[2]-args[0]) < PL_A and norm(args[1]-args[0]) > PL_A:  # coincident
                self.scope = 2*pi
                R = norm(args[1]-args[0])/2
                self.transformation = trans(
                    0.5*(args[0]+args[1]))*scale(R)  # nonsupport division
            elif is_parallel(args[2]-args[0], args[1]-args[0]):
                raise ValueError('improper parallel parameters!')
            else:
                transArc, scopeArc = get_arc_from_three_points(args)
                self.transformation = transArc
                self.scope = scopeArc
        else:
            raise ValueError('improper parameters!')

    def scale_center(self, sca: float = 1):
        pos = get_translate_matrix(self.transformation)
        rot = get_matrixs_rotation(self.transformation)
        self.transformation = pos*scale(sca)*rot
        # self.transformation = self.transformation * \
        #     scale(sca)*inverse(self.transformation) * self.transformation

    def symbology(self, color, weight, style):
        self[PARACMPT_KEYWORD_STYLE] = Symbology(color, weight, style)
        return self

    @property
    def scope(self):
        return self[PARACMPT_ARC_SCOPE]

    @scope.setter
    def scope(self, val):
        self[PARACMPT_ARC_SCOPE] = float(val)

    @property
    def pointCenter(self):
        return get_matrixs_position(self.transformation)

    @property
    def pointStart(self):
        return self.transformation*GeVec3d(1, 0, 0)

    @property
    def pointEnd(self):
        return self.transformation*GeVec3d(cos(self.scope), sin(self.scope), 0)

    @property
    def vectorTangentS(self):  # the tangent vector of start point.
        vectorZ = get_matrixs_axisz(get_orthogonal_matrix(self.transformation))
        vectorStart = self.pointStart-self.pointCenter
        return math_sign(self.scope)*unitize(cross(vectorZ, vectorStart))

    @property
    def vectorTangentE(self):  # the tangent vector of end point.
        vectorZ = get_matrixs_axisz(get_orthogonal_matrix(self.transformation))
        vectorEnd = self.pointEnd-self.pointCenter
        return math_sign(self.scope)*unitize(cross(vectorZ, vectorEnd))

    @property
    def vectorNormalC(self):  # donot change normal direciton
        vectorZ = get_matrixs_axisz(get_orthogonal_matrix(self.transformation))
        return unitize(vectorZ)  # math_sign(self.scope)

    @property
    def isCircle(self):
        axisx = get_matrixs_axisx(self.transformation)
        axisy = get_matrixs_axisy(self.transformation)
        return abs(norm(axisx)-norm(axisy)) < PL_A and abs(dot(axisx, axisy)) < PL_A

    @property
    def isFull(self):
        return abs(abs(self.scope)-2*pi) < PL_A


class Line(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Line'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_LINE_TO_GRAPHICS)
        self.parts = get_nested_parts_from_list(args)

    def append(self, value):
        self[PARACMPT_LINE_PARTS].append(value)

    def symbology(self, color, weight, style):
        self[PARACMPT_KEYWORD_STYLE] = Symbology(color, weight, style)
        return self

    @property
    def parts(self):
        return self[PARACMPT_LINE_PARTS]

    @parts.setter
    def parts(self, val):
        if not isinstance(val, list):
            raise TypeError('Line parameter error!')

        def idf(x): return isinstance(x, (GeVec2d, GeVec3d)) or (
            isinstance(x, Noumenon) and PARACMPT_KEYWORD_TRANSFORMATION in x)
        if not all(map(idf, val)):
            raise TypeError('Line parameter error!')
        self[PARACMPT_LINE_PARTS] = val


class Section(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Section'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SECTION_TO_GRAPHICS)
        self.parts = get_nested_parts_from_list(args)
        self.close = True
        self.transformation = self._get_first_matrix_from_line(self.parts)
        if is_two_dimensional_matrix(self.transformation):
            self.transformation = GeTransform()
        if not self._is_parts_on_same_plane(self.parts):
            raise TypeError('Section parts must locate on same plane!')
        self.parts = inverse_orth(self.transformation)*self.parts

    def append(self, value):
        if not (len(self.parts) == 2 and is_all_vec(self.parts)):  # cannot judge locate plane
            plane = self._get_first_matrix_from_line(self.parts)
            if not self._is_parts_locate_on_plane(value, plane):
                raise TypeError('Section parts must locate on same plane!')
        self[PARACMPT_SECTION_PARTS].append(value)

    # coplanar judge member funciton.
    def _is_parts_on_same_plane(self, param) -> bool:
        for part in self.parts:
            if (not self._is_parts_locate_on_plane(part, self.transformation)):
                return False
        return True

    def _is_parts_locate_on_plane(self, param, plane: GeTransform) -> bool:
        if isinstance(param, (GeVec2d, GeVec3d)):
            return is_point_on_plane(to_vec3(param), plane)
        elif isinstance(param, Arc):
            return is_two_dimensional_matrix(inverse_orth(plane)*get_orthogonal_matrix(param.transformation, True))
        elif isinstance(param, SplineCurve):
            for point in param.points:
                if not is_point_on_plane(param.transformation*point, plane):
                    return False
            return True
        elif isinstance(param, Segment):
            if is_point_on_plane(param.start, plane) and is_point_on_plane(param.end, plane):
                return True
            else:
                return False
        elif isinstance(param, Line):
            for part in param.parts:
                if not self._is_parts_locate_on_plane(param.transformation*part, plane):
                    return False
            return True
        else:
            raise TypeError('Line parameter error!')

    def _get_first_matrix_from_line(self, param: list) -> GeTransform:
        pointParts = self._get_points_parts_from_segment(param)
        if is_all_vec(pointParts):
            return get_matrix_from_points(pointParts)
        for iter in param:
            if isinstance(iter, (GeVec2d, GeVec3d)):
                continue
            elif isinstance(iter, Arc):
                return get_orthogonal_matrix(iter.transformation, True)
            elif isinstance(iter, SplineCurve):
                return get_orthogonal_matrix(iter.transformation)*get_matrix_from_points(iter.points)
            elif isinstance(iter, Line):
                return iter.transformation*self._get_first_matrix_from_line(iter.parts)
            elif isinstance(iter, list):
                return self._get_first_matrix_from_line(iter)
            else:
                raise ValueError('get_first_matrix_from_line param error!')

    def _get_points_parts_from_segment(self, param: list) -> list:
        pointParts = []
        for iter in param:
            if isinstance(iter, Segment):
                pointParts.append(iter.start)
                pointParts.append(iter.end)
            else:
                pointParts.append(iter)
        return pointParts

    @ property
    def parts(self):
        return self[PARACMPT_SECTION_PARTS]

    @ parts.setter
    def parts(self, val):
        if not isinstance(val, list):
            raise TypeError('Section parameter error!')

        def idf(x): return isinstance(x, (GeVec2d, GeVec3d)) or (
            isinstance(x, Noumenon) and PARACMPT_KEYWORD_TRANSFORMATION in x)
        if not all(map(idf, val)):
            raise TypeError('')
        self[PARACMPT_SECTION_PARTS] = val

    @ property
    def close(self):
        return self[PARACMPT_SECTION_COLSE]

    @ close.setter
    def close(self, val):
        if not isinstance(val, bool):
            raise TypeError('improper type!')
        self[PARACMPT_SECTION_COLSE] = val


class Sphere(Primitives):
    def __init__(self, center: GeVec3d = GeVec3d(0, 0, 0), radius: float = 1.0):
        Primitives.__init__(self)
        self.representation = 'Sphere'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SPHERE_TO_GRAPHICS)
        self.transformation = trans(center) * scale(radius)
        self.lower = 0.0  # zenith angle
        self.upper = pi

    @ property
    def center(self):
        return GeVec3d(self.transformation._mat[0][3], self.transformation._mat[1][3], self.transformation._mat[2][3])

    @ center.setter
    def center(self, value: GeVec3d):
        self.transformation._mat[0][3] = value.x
        self.transformation._mat[1][3] = value.y
        self.transformation._mat[2][3] = value.z

    @ property
    def radius(self):
        return self.transformation._mat[0][0]

    @ radius.setter
    def radius(self, value):
        self.transformation._mat[0][0] = value
        self.transformation._mat[1][1] = value
        self.transformation._mat[2][2] = value

    @ property
    def upper(self):
        return self[PARACMPT_SPHERE_UPPER]

    @ upper.setter
    def upper(self, value):
        self[PARACMPT_SPHERE_UPPER] = float(value)

    @ property
    def lower(self):
        return self[PARACMPT_SPHERE_LOWER]

    @ lower.setter
    def lower(self, value):
        self[PARACMPT_SPHERE_LOWER] = float(value)


class Cube(Primitives):
    def __init__(self):
        Primitives.__init__(self)
        self.representation = 'Cube'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_CUBE_TO_GRAPHICS)


class Loft(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Loft'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_LOFT_TO_GRAPHICS)
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            self.parts = list(args[0])
        else:
            self.parts = list(args)
        self.smooth = False

    @ property
    def parts(self):
        return self[PARACMPT_LOFT_PARTS]

    @ parts.setter
    def parts(self, val):
        if not isinstance(val, list):
            raise TypeError('Loft improper type!')
        if not all(map(lambda x: isinstance(x, (Section, Fusion, Intersect)), val)):
            raise TypeError('Loft improper type!')
        self[PARACMPT_LOFT_PARTS] = val

    @ property
    def smooth(self):
        return self[PARACMPT_LOFT_SMOOTH]

    @ smooth.setter
    def smooth(self, val):
        if not isinstance(val, bool):
            raise TypeError('improper type!')
        self[PARACMPT_LOFT_SMOOTH] = val


class Sweep(Primitives):
    def __init__(self, section=Section(), trajectory=Line()):
        Primitives.__init__(self)
        self.representation = 'Sweep'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SWEEP_TO_GRAPHICS)
        self.section = section
        if isinstance(trajectory, Line):
            self.trajectory = trajectory
        elif isinstance(trajectory, GeVec3d):
            self.trajectory = Line(GeVec3d(), trajectory)
        else:
            raise TypeError('Sweep trajectory TypeError!')
        self.smooth = False

    @ property
    def section(self):
        return self[PARACMPT_SWEEP_SECTION]

    @ section.setter
    def section(self, val):
        if not isinstance(val, (Section, Fusion, Intersect, Text)):
            raise TypeError('Sweep improper type!')
        self[PARACMPT_SWEEP_SECTION] = val

    @ property
    def trajectory(self):
        return self[PARACMPT_SWEEP_TRAJECTORY]

    @ trajectory.setter
    def trajectory(self, val):
        if not isinstance(val, Line):
            raise TypeError('Sweep improper type!')
        self[PARACMPT_SWEEP_TRAJECTORY] = val

    @ property
    def smooth(self):
        return self[PARACMPT_SWEEP_SMOOTH]

    @ smooth.setter
    def smooth(self, val):
        if not isinstance(val, bool):
            raise TypeError('improper type!')
        self[PARACMPT_SWEEP_SMOOTH] = val


class Text(Primitives):
    def __init__(self, text='', *args):
        Primitives.__init__(self)
        self.representation = 'Text'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_TEXT_TO_GRAPHICS)
        self.text = text
        self.font = Font() * Symbology()
        self.font.size = 1
        if len(args) == 0:
            self.horzscale = 1.0
            self.vertscale = 1.0
        elif len(args) == 1:
            if(isinstance(args[0], (int, float))):
                self.horzscale = float(args[0])
            elif isinstance(args[0], str):
                self.font_name = args[0]
            else:
                raise ValueError(
                    'the input value isnot number or "fontName" isnot string')
        elif len(args) == 2 and (isinstance(args[0], (int, float)) and isinstance(args[1], (int, float))):
            self.horzscale = float(args[0])
            self.vertscale = float(args[1])
        elif len(args) == 3 and (isinstance(args[0], (int, float))) and isinstance(args[1], (int, float)) and isinstance(args[2], str):
            self.horzscale = float(args[0])
            self.vertscale = float(args[1])
            self.font_name = str(args[2])
        elif len(args) == 4 and ((isinstance(args[0], int) or isinstance(args[0], float)) and (isinstance(args[1], int) or isinstance(args[1], float))) and isinstance(args[2], str) and isinstance(args[3], str):
            self.horzscale = float(args[0])
            self.vertscale = float(args[1])
            self.font_name = str(args[2])
            self.font_big_name = str(args[3])
        else:
            raise ValueError(
                'the input value isnot number or "fontName" isnot string')

    @ property
    def text(self):
        return self[PARACMPT_TEXT_TEXT]

    @ text.setter
    def text(self, val):
        self[PARACMPT_TEXT_TEXT] = val

    @ property
    def font(self):
        return self[PARACMPT_KEYWORD_STYLE]

    @ font.setter
    def font(self, val):
        self[PARACMPT_KEYWORD_STYLE] = val

    @ property
    def size(self):
        return self.font[PARACMPT_FONT_SIZE]

    @ size.setter
    def size(self, size):
        self.font[PARACMPT_FONT_SIZE] = float(size)

    @ property
    def horzscale(self):
        return self.font[PARACMPT_FONT_HORZ_SCALE]

    @ horzscale.setter
    def horzscale(self, size):
        self.font[PARACMPT_FONT_HORZ_SCALE] = float(size)

    @ property
    def vertscale(self):
        return self.font[PARACMPT_FONT_VERT_SCALE]

    @ vertscale.setter
    def vertscale(self, size):
        self.font[PARACMPT_FONT_VERT_SCALE] = float(size)

    @ property
    def font_name(self):
        return self.font[PARACMPT_FONT_NAME]

    @ font_name.setter
    def font_name(self, name):
        self.font[PARACMPT_FONT_NAME] = str(name)
        self.font[PARACMPT_FONT_TYPE] = "TrueType"

    @ property
    def font_big_name(self):
        return self.font[PARACMPT_FONT_NAME_BIG]

    @ font_big_name.setter
    def font_big_name(self, name):
        self.font[PARACMPT_FONT_NAME_BIG] = str(name)
        self.font[PARACMPT_FONT_TYPE_BIG] = "Shx"


class nest(Component):
    def __init__(self, *argv):
        Component.__init__(self)
        self.representation = 'nest'
        self.schemaName = 'GimPlatform'
        self.className = ''

        # self.internal=internal()
        # self.external=external()
        # if issubclass(type(internal),Component) and issubclass(type(external),Component):


class Combine(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Combine'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_COMBINE_TO_GRAPHICS)  # 可提取的几何体，primitive的表象类都有这个属性
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], (list, tuple)):
                args[i] = Combine(*args[i])  # using recursion
            elif not issubclass(type(args[i]), Graphics):  # Primitives
                raise TypeError('please input proper "Combine(Graphics)"')
        self.parts = list(args)

    def color(self, *argscolor):
        if len(argscolor) == 0:
            color = P3DColorDef(0.5, 0.5, 0.5, 1)
        elif len(argscolor) == 1 and isinstance(argscolor[0], (list, tuple)):
            if len(argscolor[0]) == 4:
                color = P3DColorDef(
                    argscolor[0][0], argscolor[0][1], argscolor[0][2], argscolor[0][3])
            elif len(argscolor[0]) == 3:
                color = P3DColorDef(
                    argscolor[0][0], argscolor[0][1], argscolor[0][2], 1)
        elif len(argscolor) == 2 and isinstance(argscolor[0], (list, tuple)) and (isinstance(argscolor[1], (int, float))):
            color = P3DColorDef(
                argscolor[0][0], argscolor[0][1], argscolor[0][2], argscolor[1])
        elif len(argscolor) == 3 and isinstance(argscolor[0]+argscolor[1]+argscolor[2], (int, float)):
            color = P3DColorDef(argscolor[0], argscolor[1], argscolor[2], 1)
        elif len(argscolor) == 4 and isinstance(argscolor[0]+argscolor[1]+argscolor[2]+argscolor[3], (int, float)):
            color = P3DColorDef(
                argscolor[0], argscolor[1], argscolor[2], argscolor[3])
        else:
            raise TypeError('please input proper RGBA value!')

        def combineColor(geo):
            if issubclass(type(geo), Primitives) and (not isinstance(geo, Combine)):
                geo[PARACMPT_KEYWORD_STYLE].color = color
            else:  # elif listGeo(geo):
                for i in geo.parts:
                    combineColor(i)
        # using recursion
        for i in self.parts:
            combineColor(i)
        return self

    @ property
    def parts(self):
        return self[PARACMPT_COMBINE_PARTS]

    @ parts.setter
    def parts(self, val):
        self[PARACMPT_COMBINE_PARTS] = val

    def append(self, other):
        self.parts.append(other)

    def pop(self, index: int = ...):
        self.parts.pop(index)


class Fusion(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Fusion'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_FUSION_TO_GRAPHICS)
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], (list, tuple)):
                args[i] = Combine(*args[i])
        self.parts = list(args)

    def __add__(self, other):
        res = copy.deepcopy(self)
        for i in res.parts:
            i.transformation = res.transformation * i.transformation
        res.transformation = GeTransform()
        res.parts.append(other)
        return res

    def __sub__(self, other):
        res = copy.deepcopy(self)
        for i in res.parts:
            i.transformation = res.transformation * i.transformation
        res.transformation = GeTransform()
        res.parts.append(-other)
        return res

    @ property
    def parts(self):
        return self[PARACMPT_FUSION_PARTS]

    @ parts.setter
    def parts(self, val):
        # limited boolean section,inclued front and back
        if len(val) >= 1 and isinstance(val[0], Section):
            baseM = val[0].transformation
            for i in range(1, len(val)):
                mat = val[i].transformation
                matRela = inverse(baseM)*mat
                # if is_two_matrices_coplanar(baseM,mat)!="PLANES_COPLANAR":
                if not is_two_dimensional_matrix(matRela):
                    raise ValueError(
                        'the boolean sections must on same plane!')
        self[PARACMPT_FUSION_PARTS] = val


class Intersect(Primitives):
    def __init__(self, *args):
        Primitives.__init__(self)
        self.representation = 'Intersect'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_INTERSECT_TO_GRAPHICS)
        args = list(args)
        for i in range(len(args)):
            if isinstance(args[i], (list, tuple)):
                args[i] = Combine(*args[i])
        self.parts = list(args)

    @ property
    def parts(self):
        return self[PARACMPT_INTERSECT_PARTS]

    @ parts.setter
    def parts(self, val):
        self[PARACMPT_INTERSECT_PARTS] = val


class Array(Primitives):
    def __init__(self, ontology=None, *args):
        Primitives.__init__(self)
        self.representation = 'Array'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_ARRAY_TO_GRAPHICS)
        self.ontology = ontology
        self.parts = list(args)

    @ property
    def ontology(self):
        return self[PARACMPT_ARRAY_ONTOLOGY]

    @ ontology.setter
    def ontology(self, val):
        self[PARACMPT_ARRAY_ONTOLOGY] = val

    @ property
    def parts(self):
        return self[PARACMPT_ARRAY_PARTS]

    @ parts.setter
    def parts(self, val):
        if not isinstance(val, list):
            raise TypeError('')
        self[PARACMPT_ARRAY_PARTS] = val

    def append(self, other):
        self.parts.append(other)

    def pop(self, index: int = ...):
        self.parts.pop(index)

# ------------------------------------------------------------------------------------------
# |                                          NEW                                           |
# ------------------------------------------------------------------------------------------


class SplineCurve(Primitives):
    def __init__(self, ctrlPoints=[], discNum=0, orderK=2, splineType='quasi'):
        '''
        splineType      类型:        quasi           准均匀B样条
        '''
        Primitives.__init__(self)
        self.representation = 'SplineCurve'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SPLINECURVE_TO_GRAPHICS)
        self.points = ctrlPoints
        self.num = discNum
        self.k = orderK
        self.type = splineType

    def symbology(self, color, weight, style):
        self[PARACMPT_KEYWORD_STYLE] = Symbology(color, weight, style)
        return self

    @ property
    def num(self):
        return self[PARACMPT_SPLINECURVE_NUM]

    @ num.setter
    def num(self, val):
        self[PARACMPT_SPLINECURVE_NUM] = val

    @ property
    def k(self):
        return self[PARACMPT_SPLINECURVE_K]

    @ k.setter
    def k(self, val):
        self[PARACMPT_SPLINECURVE_K] = val

    @ property
    def type(self):
        return self[PARACMPT_SPLINECURVE_TYPE]

    @ type.setter
    def type(self, val):
        self[PARACMPT_SPLINECURVE_TYPE] = val

    @ property
    def points(self):
        return self[PARACMPT_SPLINECURVE_POINTS]

    @ points.setter
    def points(self, val):
        if not isinstance(val, list):
            raise TypeError('SplineCurve parameter error!')
        if not all(isinstance(i, (GeVec2d, GeVec3d)) for i in val):
            raise TypeError('SplineCurve parameter error!')
        self[PARACMPT_SPLINECURVE_POINTS] = val

    @ property
    def get_points(self):  # get control points of multiply transform
        return self.transformation*self.points


class ParametricEquation(Primitives):  # Parametric Equation
    def __init__(self, stepList: list, func: FunctionType):  # : function
        Primitives.__init__(self)
        self.representation = 'ParametricEquation'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_PARAMETRICEQUATION_TO_GRAPHICS)

        # def spiral_line_out(t, k=0.1)a;asldjlk;

        self.fun = UnifiedFunction(func)
        self.t = stepList

    @ property
    def fun(self):
        return self[PARACMPT_PARAMETRICEQUATION_FUN]

    @ fun.setter
    def fun(self, val):
        # if not isinstance(val, FunctionType):
        #     raise TypeError('ParametricEquation function!')
        self[PARACMPT_PARAMETRICEQUATION_FUN] = val

    @ property
    def t(self):
        return self[PARACMPT_PARAMETRICEQUATION_T]

    @ t.setter
    def t(self, val):
        if not isinstance(val, list):
            raise TypeError('ParametricEquation parameter error!')
        if not all(isinstance(i, (int, float)) for i in val):
            raise TypeError('ParametricEquation parameter error!')
        self[PARACMPT_PARAMETRICEQUATION_T] = val


class Polyface(Primitives):  # 三角面片
    def __init__(self, filePath):
        Primitives.__init__(self)
        self.representation = 'Polyface'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_POLYFACE_TO_GRAPHICS)
        vertexListO = []
        faceListO = []
        with open(filePath) as file:
            line = file.readline()
            while line:
                line = line.replace('\n', '')
                strs = line.split(" ")
                if strs[0] == "v":
                    vertexListO.append(
                        10000*GeVec3d(float(strs[1]), float(strs[2]), float(strs[3])))
                if strs[0] == "f":
                    for i in range(1, len(strs)):
                        faces = strs[i].split("/")
                        faceListO.append(int(faces[0]))
                    faceListO.append(int(0))
                line = file.readline()
        self.vertexList = vertexListO
        self.faceList = faceListO

    @ property
    def vertexList(self):
        return self[PARACMPT_POLYFACE_VERTEX_LIST]

    @ vertexList.setter
    def vertexList(self, val):
        self[PARACMPT_POLYFACE_VERTEX_LIST] = val

    @ property
    def faceList(self):
        return self[PARACMPT_POLYFACE_FACE_LIST]

    @ faceList.setter
    def faceList(self, val):
        self[PARACMPT_POLYFACE_FACE_LIST] = val


class CrossBody(Primitives):  # 交叉布尔交体
    def __init__(self, frontSection=Section(), leftSection=Section(), isXoY=False):
        Primitives.__init__(self)
        self.representation = 'CrossBody'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_CROSS_BODY_TO_GRAPHICS)
        if isXoY:
            self.secFront = rotx(pi/2)*frontSection
            self.secLeft = rotz(pi/2)*rotx(pi/2)*leftSection
        else:
            self.secFront = frontSection
            self.secLeft = leftSection
        self.smooth = False

    @ property
    def secFront(self):
        return self[PARACMPT_CROSS_BODY_FRONT_SECTION]

    @ secFront.setter
    def secFront(self, val):
        self[PARACMPT_CROSS_BODY_FRONT_SECTION] = val

    @ property
    def secLeft(self):
        return self[PARACMPT_CROSS_BODY_LEFT_SECTION]

    @ secLeft.setter
    def secLeft(self, val):
        self[PARACMPT_CROSS_BODY_LEFT_SECTION] = val

    @ property
    def smooth(self):
        return self[PARACMPT_CROSS_BODY_SMOOTH]

    @ smooth.setter
    def smooth(self, val):
        if not isinstance(val, bool):
            raise TypeError('improper type!')
        self[PARACMPT_CROSS_BODY_SMOOTH] = val


# ------------------------------------------------------------------------------------------
# |                                          INNER                                         |
# ------------------------------------------------------------------------------------------


class Segment(Primitives):  # 线段类（几何计算专用）
    def __init__(self, pointStart, pointEnd):
        Primitives.__init__(self)
        if (not isinstance(pointStart, (GeVec2d, GeVec3d))) or (not isinstance(pointEnd, (GeVec2d, GeVec3d))):
            raise TypeError('Segment parameter error!')
        # if norm(pointEnd-pointStart) < PL_A:
        #     raise TypeError('segment is nonzero vector!')  # nonzero vector
        self.representation = 'Segment'
        self.extractGraphics = UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SEGMENT_TO_GRAPHICS)
        # self.transformation = GeTransform()
        self.m_start = pointStart
        self.m_end = pointEnd

    # def __getitem__(self, index):  # to support index
    #     if index == 0:
    #         return self.transformation*self.m_start
    #     elif index == 1:
    #         return self.transformation*self.m_end
    # def __rmul__(self, mat: GeTransform):
    #     if isinstance(mat, GeTransform):
    #         self.transform = mat*self.transform
    #     return self
    @ property
    def m_start(self):
        return self[PARACMPT_SEGMENT_START]

    @ m_start.setter
    def m_start(self, val):
        self[PARACMPT_SEGMENT_START] = val

    @ property
    def m_end(self):
        return self[PARACMPT_SEGMENT_END]

    @ m_end.setter
    def m_end(self, val):
        self[PARACMPT_SEGMENT_END] = val

    @ property
    def start(self):
        return self.transformation*self.m_start

    @ start.setter  # value check
    def start(self, val):
        if not isinstance(val, (GeVec2d, GeVec3d)):
            raise TypeError('Segment parameter error!')
        if norm(val-self.m_end) < PL_A:
            raise TypeError('segment is nonzero vector!')
        self.m_start = val

    @ property
    def end(self):
        return self.transformation*self.m_end

    @ end.setter
    def end(self, val):
        if not isinstance(val, (GeVec2d, GeVec3d)):
            raise TypeError('Segment parameter error!')
        if norm(val-self.m_start) < PL_A:
            raise TypeError('segment is nonzero vector!')
        self.m_end = val

    @ property
    def norm(self):
        return norm(self.transformation*self.m_end - self.transformation*self.m_start)

    @ property
    def vector(self):
        return get_matrixs_rotation(self.transformation)*(self.m_end - self.m_start)

    @ property
    def vectorU(self):
        return get_matrixs_rotation(self.transformation)*unitize(self.m_end - self.m_start)

    @ property
    def list(self):
        return [self.transformation*self.m_start, self.transformation*self.m_end]

    def isCoincident(self):
        pos = get_translate_matrix(self.transformation)


class PosVec(Primitives):  # 位矢类（几何计算专用）
    def __init__(self, position, vector):  # position, vector
        if not isinstance(position, (GeVec2d, GeVec3d)):
            raise TypeError('PosVec parameter error!')
        if not isinstance(vector, (GeVec2d, GeVec3d)):
            raise TypeError('PosVec parameter error!')
        if norm(vector) < PL_A:
            raise TypeError('vector is nonzero!')  # nonzero vector
        Primitives.__init__(self)
        self.representation = 'PosVec'
        self.m_position = position
        self.m_vector = vector
        # self.transform = GeTransform()

    # def __getitem__(self, index):  # to support index
    #     if index == 0:
    #         return self.transform*self.m_position
    #     elif index == 1:
    #         return self.transform*self.m_vector
    # def __rmul__(self, mat: GeTransform):
    #     if isinstance(mat, GeTransform):
    #         self.transform = mat*self.transform
    #     return self

    @ property
    def pos(self):
        return self.transformation*self.m_position

    @ pos.setter
    def pos(self, val):
        if not isinstance(val, (GeVec2d, GeVec3d)):
            raise TypeError('PosVec parameter error!')
        self.m_position = val

    @ property
    def vec(self):
        return get_matrixs_rotation(self.transformation)*unitize(self.m_vector)

    @ vec.setter
    def vec(self, val):
        if not isinstance(val, (GeVec2d, GeVec3d)):
            raise TypeError('PosVec parameter error!')
        if norm(val) < PL_A:
            raise TypeError('vector is nonzero!')
        self.m_vector = unitize(val)


# 从两点中获取位矢
def to_pos_vec(*args) -> PosVec:
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    else:
        args = list(args)
    if len(args) == 1:
        if isinstance(args[0], Segment):
            position = args[0].start
            vector = unitize(args[0].vectorU)
        elif isinstance(args[0], list):
            position = args[0][0]
            vector = unitize(args[0][1]-args[0][0])
    elif len(args) == 2:
        position = args[0]
        vector = unitize(args[1]-args[0])
    return PosVec(position, vector)


# 从点的列表获取Segment
def to_segment(points: list) -> Segment:
    if len(points) != 2:
        raise ValueError('parameter number error!')
    return Segment(points[0], points[1])


'''
class Plane():  # 几何概念-平面
    # 几种默认构造
    # 1 三点式（两个向量）
    # 2 一般式 # Ax+By+Cz+D=0
    # 3 平面法向量（点法式）
    # 4 矩阵形式（默认XoY面）
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], GeTransform):
            self.m_mat = args[0]
        elif len(args) == 3 and is_all_vec(args):
            self.m_mat = get_matrix_from_three_points(args)
        elif len(args) == 4 and is_all_num(args):
            # Ax+By+Cz+D=0
            A = args[0]
            B = args[1]
            C = args[2]
            D = args[3]
            if is_zero(A) and is_zero(B) and is_zero(C):
                raise ValueError('parameter error!')
            if not is_zero(C):
                p1 = GeVec3d(0, 0, -D/C)
            else:
                if not is_zero(B):
                    p2 = GeVec3d(0, -D/B, 0)
                    if not is_zero(A):
                        p3 = GeVec3d(-D/A, 0, 0)
                    else:
                        ...
                else:
                    ...

            self.m_mat = get_matrix_from_three_points([p1, p2, p3])



'''
