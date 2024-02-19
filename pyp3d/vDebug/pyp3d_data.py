# Copyright (C),  2019-2028,  Beijing GLory PKPM Tech. Co.,  Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: YouQi,YanYinji
# Date: 2021/11
from .pyp3d_convention import *
import copy
from math import *


class Persistent(BufferStackBase):
    '''
    工程文件持久化数据集
    '''

    def __init__(self, identification=''):
        if not (isinstance(identification, int) or isinstance(identification, str)):
            raise TypeError('')
        self._identification = identification

    def _push_to(self, bs: BufferStack) -> None: bs.push(self._identification)

    def _pop_from(
        self, bs: BufferStack) -> None: self._identification = bs.pop()

    def get(self):
        res = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                              PARACMPT_UPDATE_MATERIAL)(self)
        if isinstance(res, list) and len(res) > 0:
            return res[0]
        return None

    def set(self, val):
        UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                        PARACMPT_UPDATE_MATERIAL)(self, [val])


class Attr(BufferStackBase):
    '''
    Attribute database, multi-fork tree structure with main node,to load parameter component attribute database
    '''

    def __init__(self, this=None, **kw): self._this, self._attr = this, {
        k: v if isinstance(v, Attr) else Attr(v) for k, v in kw.items()}

    def __getitem__(self, key): return self._attr[key].this
    def __setitem__(self, key, value): self._attr[key] = value if isinstance(
        value, Attr) else Attr(value)

    def __delitem__(self, key): del self._noumenon_data[key]
    def __contains__(self, item): return item in self._attr

    def __str__(self): return '{0}#{{{1}}}'.format(self._this, ', '.join(
        ['{0}={1}'.format(k, v) for k, v in self._attr.items()]))

    def _push_to(self, bs: BufferStack) -> None:
        for k, v in self._attr.items():
            bs.push(v, k)
        bs.push(Size_t(len(self._attr)), self._this)

    def _pop_from(self, bs: BufferStack) -> None:
        self._this, size, self._attr = bs.pop(), bs.pop(), {}
        for _ in range(size):
            k, v = bs.pop(), bs.pop()
            self._attr[k] = v

    def at(self, key): return self._attr[key]

    def setup(self, **args):
        for k, v in args.items():
            self._attr[k] = v if isinstance(v, Attr) else Attr(v)

    @property
    def this(self): return self._this
    @this.setter
    def this(self, value): self._this = value


class Noumenon():
    '''
    Noumenon database
    '''

    def __init__(self):
        self._noumenon_data = {}
        self._noumenon_order = []

    def __str__(self): return '\n'.join(['{0} = {1}'.format(
        key, self._noumenon_data[key]) for key in self._noumenon_order])

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._noumenon_data[self._noumenon_order[key]].this
        elif isinstance(key, str):
            return self._noumenon_data[key].this
        else:
            raise TypeError()

    def __setitem__(self, key, value):
        if isinstance(key, str):
            ...
        elif isinstance(key, int):
            if not key < len(self._noumenon_order):
                raise IndexError('OrderedDictionary index out of range')
            key = self._noumenon_order[key]
        else:
            raise TypeError()
        if key in self._noumenon_data:
            if isinstance(value, Attr):
                self._noumenon_data[key] = value
            elif isinstance(value, FunctionType):
                self._noumenon_data[key].this = UnifiedFunction(value)
                self._noumenon_data[key]['member'] = True
            else:
                self._noumenon_data[key].this = value
        else:
            if isinstance(value, Attr):
                self._noumenon_data[key] = value
            elif isinstance(value, FunctionType):
                self._noumenon_data[key] = Attr(
                    UnifiedFunction(value), member=True)
            else:
                self._noumenon_data[key] = Attr(value)
            self._noumenon_order.append(key)

    def __delitem__(self, key):
        if isinstance(key, int):
            if not key < len(self._noumenon_order):
                raise IndexError('OrderedDictionary index out of range')
            del self._noumenon_data[self._noumenon_order[key]]
            self._noumenon_order.remove(key)
        elif isinstance(key, str):
            del self._noumenon_data[key]
            self._noumenon_order.remove(key)
        else:
            raise TypeError()

    def at(self, key) -> Attr: return self._noumenon_data[key]

    def __mul__(self, other):
        if not issubclass(type(other), Noumenon):
            raise TypeError('object not inherited form Noumenon')
        c = copy.deepcopy(other)
        for k, v in self.items():
            c[k] = v
        return c

    def __len__(self): return len(self._noumenon_order)

    def __iter__(self):
        self._iter = 0
        return self

    def __next__(self):
        if self._iter >= len(self._noumenon_order):
            raise StopIteration
        key = self._noumenon_order[self._iter]
        self._iter += 1
        return self._noumenon_data[key]

    def __contains__(self, item): return item in self._noumenon_data
    def keys(self): return self._noumenon_order

    def values(self): return [self._noumenon_data[i]
                              for i in self._noumenon_order]

    def items(self): return [(i, self._noumenon_data[i])
                             for i in self._noumenon_order]

    def insert(self, key, value, position=None):
        if not isinstance(key, str):
            raise TypeError()
        self.set_object(key, value if isinstance(value, Attr) else Attr(value))
        if position is None:
            return
        self.adjust(key, position)

    def adjust(self, index, position):
        if isinstance(index, int):
            ...
        elif isinstance(index, str):
            index = self._noumenon_order.index(index)
        else:
            raise TypeError()
        if isinstance(position, int):
            ...
        elif isinstance(position, str):
            position = self._noumenon_order.index(position)
        else:
            raise TypeError()
        if not(index < len(self._noumenon_order) and position <= len(self._noumenon_order)):
            raise IndexError('OrderedDictionary index out of range')
        if index == position:
            return
        key = self._noumenon_order[index]
        del self._noumenon_order[index]
        self._noumenon_order.insert(
            position if position < index else position - 1, key)


class P3DEntityId(BufferStackBase):
    def __init__(self): self._ModelId, self._ElementId = 0, 0

    def _push_to(self, bs):
        bs.push(self._ModelId, self._ElementId)

    def _pop_from(
        self, bs): self._ElementId, self._ModelId = bs.pop(), bs.pop()


class P3DModelId(BufferStackBase):
    def __init__(self): self._ModelId = 0

    def _push_to(self, bs):
        bs.push(self._ModelId)

    def _pop_from(self, bs):  self._ModelId = bs.pop()


class P3DInstanceKey(BufferStackBase):
    def __init__(self): self._PClassId, self._P3DInstanceId = 0, 0
    def _push_to(self, bs): bs.push(self._PClassId, self._P3DInstanceId)

    def _pop_from(
        self, bs): self._P3DInstanceId, self._PClassId = bs.pop(), bs.pop()

    def __str__(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__str__()

    def __getitem__(self, key):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        self._data.__setitem__(key, value)

    def __delitem__(self, key):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        self._data.__delitem__(key)

    def at(self, key) -> Attr:
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.at(key)

    def __mul__(self, other):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__mul__(other)

    def __len__(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__len__()

    def __iter__(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__iter__()

    def __next__(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__next__()

    def __contains__(self, item):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.__contains__(item)

    def keys(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.keys()

    def values(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.values()

    def items(self):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.items()

    def insert(self, key, value, position=None):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.insert(key, value, position=None)

    def adjust(self, index, position):
        if self._data == None:
            self._data = UnifiedFunction(
                PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(self)
        return self._data.adjust(index, position)


class GeTransform(BufferStackBase):
    def __init__(self, mat=[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]):
        self._mat = [[float(mat[i][ii]) for ii in range(4)] for i in range(3)]

    def __str__(self): return str(self._mat)

    def __mul__(self, b):
        if isinstance(b, (list, tuple)):
            return [self * i for i in b]
        else:
            return b.__rmul__(self)

    def __rmul__(self, a):
        if isinstance(a, GeTransform):
            return GeTransform([[sum([a._mat[k][i]*self._mat[i][j] for i in range(3)]) + (a._mat[k][3] if j == 3 else 0.0) for j in range(4)] for k in range(3)])
        elif isinstance(a, (int, float)):
            return GeTransform([[a*self._mat[j][i] for i in range(4)] for j in range(3)])
        elif isinstance(a, (list, tuple)) and all(isinstance(i, GeVec2d)for i in a):
            vecList = []
            for iter in a:
                vecList.append(self*iter)
            return vecList
        else:
            raise TypeError('__mul__ error type!')

    def __add__(self, b):
        if isinstance(b, GeTransform):
            return GeTransform([[self._mat[j][i]+b._mat[j][i] for i in range(4)] for j in range(3)])
        else:
            raise TypeError('improper parameter!')

    def __sub__(self, b):
        if isinstance(b, GeTransform):
            return GeTransform([[self._mat[j][i]-b._mat[j][i] for i in range(4)] for j in range(3)])
        else:
            raise TypeError('improper parameter!')

    def __lt__(self, other):
        if isinstance(other, GeTransform):
            for i in range(3):
                for j in range(4):
                    if self._mat[i][j] < other._mat[i][j]:
                        return True
            return False
        else:
            raise TypeError('improper parameter!')

    def __eq__(self, other) -> bool:
        if isinstance(other, GeTransform):
            for i in range(3):
                for j in range(4):
                    if abs(self._mat[i][j]-other._mat[i][j]) > PL_A:
                        return False
            return True
        else:
            raise TypeError('improper parameter!')

    def _push_to(self, buf: BufferStack): [
        [buf.push(self._mat[2-i][3-j]) for j in range(4)] for i in range(3)]
    def _pop_from(self, buf: BufferStack): self._mat = [
        [buf.pop() for _ in range(4)] for _ in range(3)]


class GeVec3d(BufferStackBase):
    def __init__(self, *args):
        if len(args) == 0:
            self.x, self.y, self.z = 0.0, 0.0, 0.0
        elif len(args) == 3:
            self.x, self.y, self.z = float(
                args[0]), float(args[1]), float(args[2])
        elif len(args) == 2:
            self.x, self.y, self.z = float(args[0]), float(args[1]), 0.0
        elif len(args) == 1 and (isinstance(args[0], (list, tuple))) and len(args[0]) == 3:
            self.x, self.y, self.z = float(args[0][0]), float(
                args[0][1]), float(args[0][2])
        elif len(args) == 1 and (isinstance(args[0], (list, tuple))) and len(args[0]) == 2:
            self.x, self.y, self.z = float(args[0][0]), float(args[0][1]), 0.0
        else:
            raise TypeError('improper parameter!')

    def __str__(self): return '({0}, {1}, {2})'.format(self.x, self.y, self.z)

    def __rmul__(self, a):
        if isinstance(a, GeTransform):
            return GeVec3d(*[a._mat[i][0]*self.x + a._mat[i][1]*self.y + a._mat[i][2]*self.z + a._mat[i][3] for i in range(3)])
        elif isinstance(a, (float, int)):
            return GeVec3d(a*self.x, a*self.y, a*self.z)
        elif isinstance(a, GeVec3d):
            return a.x*self.x + a.y*self.y + a.z*self.z
        else:
            raise TypeError('`*` error type!')

    def __xor__(self, other):
        if isinstance(other, GeVec3d):
            return GeVec3d(self.y*other.z-self.z*other.y, self.z*other.x-self.x*other.z, self.x*other.y-self.y*other.x)
        else:
            raise TypeError('`^` error type!')

    def __neg__(self):
        c = copy.deepcopy(self)
        c.x, c.y, c.z = -self.x, -self.y, -self.z
        return c

    def __mul__(self, b):
        if isinstance(b, (float, int)):
            return GeVec3d(self.x * b, self.y * b, self.z * b)
        elif isinstance(b, GeVec3d):
            return b.x*self.x + b.y*self.y + b.z*self.z
        else:
            raise TypeError('improper parameter!')

    def __add__(self, b):
        if isinstance(b, GeVec3d):
            return GeVec3d(self.x+b.x, self.y+b.y, self.z+b.z)
        elif isinstance(b, GeVec2d):
            return GeVec3d(self.x+b.x, self.y+b.y, self.z)
        else:
            raise TypeError('improper parameter!')

    def __radd__(self, a):
        if isinstance(a, GeVec3d):
            return GeVec3d(a.x+self.x, a.y+self.y, a.z+self.z)
        elif isinstance(a, GeVec2d):
            return GeVec3d(a.x+self.x, a.y+self.y, self.z)
        else:
            raise TypeError('improper parameter!')

    def __sub__(self, b):
        if isinstance(b, GeVec3d):
            return GeVec3d(self.x-b.x, self.y-b.y, self.z-b.z)
        elif isinstance(b, GeVec2d):
            return GeVec3d(self.x-b.x, self.y-b.y, self.z)
        else:
            raise TypeError('improper parameter!')

    def __rsub__(self, a):
        if isinstance(a, GeVec3d):
            return GeVec3d(a.x-self.x, a.y-self.y, a.z-self.z)
        elif isinstance(a, GeVec2d):
            return GeVec3d(a.x-self.x, a.y-self.y, 0.0-self.z)
        else:
            raise TypeError('improper parameter!')

    def __lt__(self, a):
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z) < sqrt(a.x*a.x+a.y*a.y+a.z*a.z)

    def __eq__(self, other) -> bool:
        return (self - other).norm() < PL_E8

    def __hash__(self) -> int:
        return super().__hash__()

    def _push_to(self, buf: BufferStack): buf.push(self.x, self.y, self.z)

    def _pop_from(self, buf: BufferStack): self.z, self.y, self.x = buf.pop(
    ), buf.pop(), buf.pop()

    def __repr__(self):
        return 'GeVec3d({self.x},{self.y},{self.z})'.format(self=self)
    def __getitem__(self, index)->float:
        if (index==0):
            return self.x
        elif (index==1):
            return self.y
        elif (index==2):
            return self.z
        else:
            return float('nan')
    # def x(self): # same name error
    #     return self.x
    # def y(self): 
    #     return self.y
    # def z(self): 
    #     return self.z
    @property
    def x(self): return self._x
    @x.setter
    def x(self, val): self._x = float(val)
    @property
    def y(self): return self._y
    @y.setter
    def y(self, val): self._y = float(val)
    @property
    def z(self): return self._z
    @z.setter
    def z(self, val): self._z = float(val)

    def norm(self)->float:
        return sqrt(self.x*self.x+self.y*self.y+self.z*self.z)
    def norm2(self)->float:
        return self.x*self.x+self.y*self.y+self.z*self.z
    def squaredNorm(self)->float:
        return self.norm2()
    def unitize(self):
        n = self.norm()
        if n < PL_A:
            return GeVec3d(0, 0, 0)
        else:
            return GeVec3d(self.x/n, self.y/n, self.z/n)
    def normalize(self): #normalized self
        n = self.norm()
        if n > PL_A:
            self.x=self.x/n
            self.y=self.y/n
            self.z=self.z/n
    def normalized(self): # new normalize
        return self.unitize()
    def isOrigin(self):
        return self.norm() < PL_A
    def isZero(self, eps=1e-8)->bool:
        # return self.isOrigin()
        return fabs(self.x)<eps and fabs(self.y)<eps and fabs(self.z)<eps
    def isValid(self):
        if (isnan(self.x) or isnan(self.y) or isnan(self.z)):
            return False
        if (isinf(self.x) or isinf(self.y) or isinf(self.z)):
            return False
        return True
    def cross(self,val): #->GeVec3d
        return GeVec3d(self.y*val.z-self.z*val.y, self.z*val.x-self.x*val.z, self.x*val.y-self.y*val.x)
    def dot(self,val)->float:
        return self.x*val.x + self.y*val.y + self.z*val.z

class GeVec2d(BufferStackBase):
    def __init__(self, *args):  # self.x, self.y = x, y
        if len(args) == 0:
            self.x, self.y = 0.0, 0.0
        elif len(args) == 2:
            self.x, self.y = float(args[0]), float(args[1])
        elif len(args) == 1 and (isinstance(args[0], (list, tuple))) and len(args[0]) == 2:
            self.x, self.y = float(args[0][0]), float(args[0][1])
        else:
            raise TypeError('improper parameter!')

    def __str__(self): return '({0}, {1})'.format(self.x, self.y)

    def __rmul__(self, a):
        # if isinstance(a, GeTransform): return GeVec2d(*[a._mat[i][0]*self.x + a._mat[i][1]*self.y + a._mat[i][3] for i in range(2)])
        if isinstance(a, GeTransform):
            # 乘矩阵返回Vec3
            return GeVec3d(*[a._mat[i][0]*self.x + a._mat[i][1]*self.y + a._mat[i][2]*0 + a._mat[i][3] for i in range(3)])
        elif isinstance(a, (float, int)):
            return GeVec2d(a*self.x, a*self.y)
        else:
            raise TypeError('input error type!')

    def __neg__(self):
        c = copy.deepcopy(self)
        c.x, c.y = -self.x, -self.y
        return c

    def __mul__(self, b):
        if isinstance(b, (float, int)):
            return GeVec2d(self.x * b, self.y * b)
        else:
            raise TypeError('improper parameter!')

    def __add__(self, b):
        if isinstance(b, GeVec2d):
            return GeVec2d(self.x+b.x, self.y+b.y)
        elif isinstance(b, GeVec3d):
            return GeVec3d(self.x+b.x, self.y+b.y, b.z)
        else:
            raise TypeError('improper parameter!')

    def __radd__(self, a):
        if isinstance(a, GeVec2d):
            return GeVec2d(a.x+self.x, a.y+self.y)
        elif isinstance(a, GeVec3d):
            return GeVec3d(a.x+self.x, a.y+self.y, a.z)
        else:
            raise TypeError('improper parameter!')

    def __sub__(self, b):
        if isinstance(b, GeVec2d):
            return GeVec2d(self.x-b.x, self.y-b.y)
        elif isinstance(b, GeVec3d):
            return GeVec3d(self.x-b.x, self.y-b.y, 0.0-b.z)
        else:
            raise TypeError('improper parameter!')

    def __rsub__(self, a):
        if isinstance(a, GeVec2d):
            return GeVec2d(a.x-self.x, a.y-self.y)
        elif isinstance(a, GeVec3d):
            return GeVec3d(a.x-self.x, a.y-self.y, a.z)
        else:
            raise TypeError('improper parameter!')
    def dot(self,val)->float:
        return self.x*val.x + self.y*val.y
    
    def _push_to(self, buf: BufferStack): buf.push(self.x, self.y)
    def _pop_from(
        self, buf: BufferStack): self.y, self.x = buf.pop(), buf.pop()

    @property
    def x(self): return self._x
    @x.setter
    def x(self, val): self._x = float(val)
    @property
    def y(self): return self._y
    @y.setter
    def y(self, val): self._y = float(val)

    def norm(self) -> float:
        return sqrt(self.x*self.x+self.y*self.y)

    def unitize(self):
        n = self.norm()
        if n < PL_A:
            return GeVec2d(0, 0)
        else:
            return GeVec2d(self.x/n, self.y/n)


class P3DColorDef(BufferStackBase):
    def __init__(self, r=0, g=0, b=0,
                 a=0): self.r, self.g, self.b, self.a = r, g, b, a

    def _push_to(self, bs): bs.push(self.r, self.g, self.b, self.a)
    def _pop_from(self, bs): self.a, self.b, self.g, self.r = bs.pop(
    ), bs.pop(), bs.pop(), bs.pop()
    @property
    def r(self): return self._r

    @r.setter
    def r(self, val):
        if val < 0 or val > 1:
            raise ValueError('the value range of RGBA is in [0,1]!')
        self._r = float(val)

    @property
    def g(self): return self._g

    @g.setter
    def g(self, val):
        if val < 0 or val > 1:
            raise ValueError('the value range of RGBA is in [0,1]!')
        self._g = float(val)

    @property
    def b(self): return self._b

    @b.setter
    def b(self, val):
        if val < 0 or val > 1:
            raise ValueError('the value range of RGBA is in [0,1]!')
        self._b = float(val)

    @property
    def a(self): return self._a

    @a.setter
    def a(self, val):
        if val < 0 or val > 1:
            raise ValueError('the value range of RGBA is in [0,1]!')
        self._a = float(val)


class Entityattribute(BufferStackBase):
    def __init__(self, kw={}): ...
    #     self._Done = False
    #     self.model_id = kw['model_id'] if 'model_id' in kw else 0
    #     self.entity_id =kw['entity_id'] if 'entity_id' in kw else 0
    #     self.entity_color=kw['entity_color'] if 'entity_color' in kw else 0
    #     self.entity_weight=kw['entity_weight'] if 'entity_weight' in kw else 0
    #     self.entity_style=kw['entity_style'] if 'entity_style' in kw else 0
    #     self.levelname =kw['levelname'] if 'levelname' in kw else ''
    #     self.classname =kw['classname'] if 'classname' in kw else ''
    #     self.schemaname =kw['schemaname'] if 'schemaname' in kw else ''
    #     self._Done = True
    # @property
    # def model_id(self):return self._model_id
    # @model_id.setter
    # def model_id(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError('input error type, please input number(suggest  integer)!')
    #     self._model_id = value
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SET_MODEL_ENTITY)(self)

    # @property
    # def entity_id(self):return self._entity_id
    # @entity_id.setter
    # def entity_id(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError('input error type, please input number(suggest  integer)!')
    #     self._entity_id = value
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SET_MODEL_ENTITY)(self)
    # @property
    # def entity_color(self):return self._entity_color
    # @entity_color.setter
    # def entity_color(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError('input error type, please input number(suggest  integer)!')
    #     self._entity_color = value
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SET_MODEL_ENTITY)(self)
    # @property
    # def entity_weight(self):return self._entity_weight
    # @entity_weight.setter
    # def entity_weight(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError('input error type, please input number(suggest  integer)!')
    #     self._entity_weight = value
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SET_MODEL_ENTITY)(self)
    # @property
    # def entity_style(self):return self._entity_style
    # @entity_style.setter
    # def entity_style(self, value):
    #     if not isinstance(value, int):
    #         raise TypeError('input error type, please input number(suggest  integer)!')
    #     self._entity_style =value
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_SET_MODEL_ENTITY)(self)
    # @property
    # def levelname(self):return self._levelname
    # @levelname.setter
    # def levelname(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError('input error type, please input "string"!')
    #     self._levelname = value
    # @property
    # def classname(self):return self._classname
    # @classname.setter
    # def classname(self, value):
    #     if not isinstance(value, str):
    #         raise TypeError('input error type, please input "string"!')
    #     self._classname = value
    def _push_to(self, buf: BufferStack):
        buf.push(self.model_id)
        buf.push(self.entity_id)
        buf.push(self.entity_color)
        buf.push(self.entity_weight)
        buf.push(self.entity_style)
        buf.push(self.levelname)
        buf.push(self.classname)
        buf.push(self.schemaname)

    def _pop_from(self, buf: BufferStack):
        self._Done = False
        self.schemaname = buf.pop()
        self.classname = buf.pop()
        self.levelname = buf.pop()
        self.entity_style = buf.pop()
        self.entity_weight = buf.pop()
        self.entity_color = buf.pop()
        self.entity_id = buf.pop()
        self.model_id = buf.pop()
        self._Done = True


class P3DMaterial(BufferStackBase):
    def __init__(self, kw={}):
        self._Done = False
        self.hasAmbientFactor = True
        self.hasColor = True
        self.hasDiffuseFactor = True
        self.hasGlowColor = True
        self.hasGlowFactor = True
        self.hasMap = False
        self.hasReflectFactor = True
        self.hasRefractFactor = True
        self.hasRoughnessFactor = True
        self.hasSpecularColor = True
        self.hasSpecularFactor = True
        self.hasTransparency = True
        self.isValid = True
        self.name = kw['Name'] if 'Name' in kw else ''
        self.mapFile = kw['path'] if 'path' in kw else ''
        self.mapUnit = kw['mapUnit'] if 'mapUnit' in kw else 0
        self.mapMode = kw['mapMode'] if 'mapMode' in kw else 0
        self.uvScale = kw['uvScale'] if 'uvScale' in kw else [1.0, 1.0]
        self.uvOffset = kw['uvOffset'] if 'uvOffset' in kw else [0.0, 0.0]
        self.wRotation = kw['wRotation'] if 'wRotation' in kw else 0
        self.bumpFactor = kw['bumpFactor'] if 'bumpFactor' in kw else 0.0
        self.color = kw['color'] if 'color' in kw else [0, 245/255, 1]
        self.transparency = kw['transparency'] if 'transparency' in kw else 0.0
        self.specularColor = kw['specularColor'] if 'specularColor' in kw else [
            1.0, 1.0, 1.0]
        self.specularFactor = kw['specularFactor'] if 'specularFactor' in kw else 1.0
        self.glowColor = kw[' glowColor'] if ' glowColor' in kw else [
            1.0, 1.0, 1.0]
        self.glowFactor = kw['glowFactor'] if 'glowFactor' in kw else 55.0
        self.ambientFactor = kw['ambientFactor'] if 'ambientFactor' in kw else 0.6
        self.diffuseFactor = kw['diffuseFactor'] if 'diffuseFactor' in kw else 0.7
        self.roughnessFactor = kw['roughnessFactor'] if 'roughnessFactor' in kw else 0.4
        self.reflectFactor = kw['reflectFactor'] if 'reflectFactor' in kw else 0.4
        self.refractFactor = kw['refractFactor'] if 'refractFactor' in kw else 0.7
        self._Done = True

    @property
    def name(self): return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('input error type, please input "string"!')
        self._name = value

    @property
    def mapFile(self):
        return self._mapFile

    @mapFile.setter
    def mapFile(self, value):
        if value is None:
            self.hasMap = False
        else:
            if not isinstance(value, str):
                raise TypeError('input error type, please input "string"!')
            self._mapFile = value
            if self._mapFile != '':
                self.hasMap = True
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def mapUnit(self):
        return self._mapUnit

    @mapUnit.setter
    def mapUnit(self, value):
        if value != 3 and value != 0:
            raise TypeError(
                'input error type, input 0(mapping by scale) or 3(mapping by size)')
        self._mapUnit = int(value)
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def mapMode(self):
        return self._mapMode

    @mapMode.setter
    def mapMode(self, value):
        if not value in [0, 2, 4, 5, 6]:
            raise TypeError(
                'input error type, input 0(parametric geometry projection), 2(planar projection), 4(cube projection), 5(sphere projection), 6(cone projection)')

        self._mapMode = int(value)
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def uvScale(self):
        return self._uvScale

    @uvScale.setter
    def uvScale(self, value):
        if not(all(map(lambda x: isinstance(x, (float, int)), value))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._uvScale = list(map(float, value))
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def uvOffset(self):
        return self._uvOffset

    @uvOffset.setter
    def uvOffset(self, value):
        if not(all(map(lambda x: isinstance(x, (float, int)), value))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._uvOffset = list(map(float, value))
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def wRotation(self):
        return self._wRotation

    @wRotation.setter
    def wRotation(self, value):
        if not (isinstance(value, (int, float))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._wRotation = degrees(float(value))
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)
    # @property
    # def bumpFactor(self):
    #     return self._bumpFactor
    # @bumpFactor.setter
    # def bumpFactor(self, value):
    #     if not (isinstance(value, int) or isinstance(value, float)):
    #         raise TypeError('input error type, please input number(suggest float or integer)!')
    #     self._bumpFactor = float(value)
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            self.hascolor = False
        else:
            if not(all(map(lambda x: isinstance(x, (float, int)), value))):
                raise TypeError(
                    'input error type, please input number(suggest float)!')
            self._color = list(map(float, value))
            self.hascolor = True
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, value):
        if not(isinstance(value, (int, float))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._transparency = float(value)
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def specularColor(self):
        return self._specularColor

    @specularColor.setter
    def specularColor(self, value):
        if not(all(map(lambda x: isinstance(x, (float, int)), value))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._specularColor = list(map(float, value))
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def specularFactor(self):
        return self._specularFactor

    @specularFactor.setter
    def specularFactor(self, value):

        if not(isinstance(value, (int, float))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._specularFactor = float(value)
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def glowColor(self):
        return self._glowColor

    @glowColor.setter
    def glowColor(self, value):
        if not(all(map(lambda x: isinstance(x, (float, int)), value))):
            raise TypeError(
                'input error type, please input number(suggest float)!')
        self._glowColor = list(map(float, value))
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def glowFactor(self):
        return self._glowFactor

    @glowFactor.setter
    def glowFactor(self, value):
        if value < 0 or value > 100:
            raise TypeError(
                'input error value, please input number in (0-100) or decimal!')
        self._glowFactor = float(value)
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    @property
    def ambientFactor(self):
        return self._ambientFactor

    @ambientFactor.setter
    def ambientFactor(self, value):
        if value < 0 or value > 1:
            raise TypeError(
                'input error value, please input decimal in (0-1)!')
        self._ambientFactor = float(value)
        if self._Done:
            UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                            PARACMPT_UPDATE_MATERIAL)(self)

    # @property
    # def diffuseFactor(self):
    #     return self._diffuseFactor
    # @diffuseFactor.setter
    # def diffuseFactor(self, value):
    #     if value < 0 or value > 1:
    #         raise TypeError('input error value, please input decimal in (0-1)!')
    #     self._diffuseFactor = float(value)
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_UPDATE_MATERIAL)(self)
    # @property
    # def roughnessFactor(self):
    #     return self._roughnessFactor
    # @roughnessFactor.setter
    # def roughnessFactor(self, value):
    #     if value < 0 or value > 1:
    #         raise TypeError('input error value, please input decimal in (0-1)!')
    #     self._roughnessFactor = float(value)
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_UPDATE_MATERIAL)(self)
    # @property
    # def reflectFactor(self):
    #     return self._reflectFactor
    # @reflectFactor.setter
    # def reflectFactor(self, value):
    #     if value < 0 or value > 1:
    #         raise TypeError('input error value, please input decimal in (0-1)!')
    #     self._reflectFactor = float(value)
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_UPDATE_MATERIAL)(self)
    # @property
    # def refractFactor(self):
    #     return self._refractFactor
    # @refractFactor.setter
    # def refractFactor(self, value):
    #     if value < 0 or value > 1:
    #         raise TypeError('input error value, please input decimal in (0-1)!')
    #     self._reflectFactor = float(value)
    #     if self._Done:
    #         UnifiedFunction( PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_UPDATE_MATERIAL)(self)

    def texture(self, path, **kw):  # 要确保第二次传的参数全部和creatematerial一样
        self._Done = False
        self.mapFile = path
        if 'mapUnit' in kw:
            self.mapUnit = kw['mapUnit']
        if 'mapMode' in kw:
            self.mapMode = kw['mapMode']
        if 'uvScale' in kw:
            self.uvScale = kw['uvScale']
        if 'uvOffset' in kw:
            self.uvOffset = kw['uvOffset']
        if 'wRotation' in kw:
            self.wRotation = kw['wRotation']
        if 'bumpFactor' in kw:
            self.bumpFactor = kw['bumpFactor']
        if 'color' in kw:
            self.color = kw['color']
        if 'transparency' in kw:
            self.transparency = kw['transparency']
        if 'specularColor' in kw:
            self.specularColor = kw['specularColor']
        if 'specularFactor' in kw:
            self.specularFactor = kw['specularFactor']
        if ' glowColor' in kw:
            self.glowColor = kw[' glowColor']
        if 'glowFactor' in kw:
            self.glowFactor = kw['glowFactor']
        if 'ambientFactor' in kw:
            self.ambientFactor = kw['ambientFactor']
        if 'diffuseFactor' in kw:
            self.diffuseFactor = kw['diffuseFactor']
        if 'roughnessFactor' in kw:
            self.roughnessFactor = kw['roughnessFactor']
        if 'reflectFactor' in kw:
            self.reflectFactor = kw['reflectFactor']
        if 'refractFactor' in kw:
            self.refractFactor = kw['refractFactor']
        self._Done = True
        UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                        PARACMPT_UPDATE_MATERIAL)(self)

    def _push_to(self, buf: BufferStack):
        buf.push(self._transparency)
        buf.push(self.name)
        buf.push(self.mapFile)
        buf.push(self.mapUnit)
        buf.push(self.mapMode)
        buf.push(self.uvScale[1])
        buf.push(self.uvScale[0])
        buf.push(self.uvOffset[1])
        buf.push(self.uvOffset[0])
        buf.push(self.wRotation)
        buf.push(self.bumpFactor)
        buf.push(self.color[2])
        buf.push(self.color[1])
        buf.push(self.color[0])
        buf.push(self.transparency)
        buf.push(self.specularColor[2])
        buf.push(self.specularColor[1])
        buf.push(self.specularColor[0])
        buf.push(self.specularFactor)
        buf.push(self.glowColor[2])
        buf.push(self.glowColor[1])
        buf.push(self.glowColor[0])
        buf.push(self.glowFactor)
        buf.push(self.ambientFactor)
        buf.push(self.diffuseFactor)
        buf.push(self.roughnessFactor)
        buf.push(self.reflectFactor)
        buf.push(self.refractFactor)
        buf.push(self.hasAmbientFactor)
        buf.push(self.hasColor)
        buf.push(self.hasDiffuseFactor)
        buf.push(self.hasGlowColor)
        buf.push(self.hasGlowFactor)
        buf.push(self.hasMap)
        buf.push(self.hasReflectFactor)
        buf.push(self.hasRefractFactor)
        buf.push(self.hasRoughnessFactor)
        buf.push(self.hasSpecularColor)
        buf.push(self.hasSpecularFactor)
        buf.push(self.hasTransparency)
        buf.push(self.isValid)

    def _pop_from(self, buf: BufferStack):
        self._Done = False
        self.isValid = buf.pop()
        self.hasTransparency = buf.pop()
        self.hasSpecularFactor = buf.pop()
        self.hasSpecularColor = buf.pop()
        self.hasRoughnessFactor = buf.pop()
        self.hasRefractFactor = buf.pop()
        self.hasReflectFactor = buf.pop()
        self.hasMap = buf.pop()
        self.hasGlowFactor = buf.pop()
        self.hasGlowColor = buf.pop()
        self.hasDiffuseFactor = buf.pop()
        self.hasColor = buf.pop()
        self.hasAmbientFactor = buf.pop()
        self.refractFactor = buf.pop()
        self.reflectFactor = buf.pop()
        self.roughnessFactor = buf.pop()
        self.diffuseFactor = buf.pop()
        self.ambientFactor = buf.pop()
        self.glowFactor = buf.pop()
        self.glowColor = [buf.pop(), buf.pop(), buf.pop()]
        self.specularFactor = buf.pop()
        self.specularColor = [buf.pop(), buf.pop(), buf.pop()]
        self.transparency = buf.pop()
        self.color = [buf.pop(), buf.pop(), buf.pop()]
        self.bumpFactor = buf.pop()
        self.wRotation = buf.pop()
        self.uvOffset = [buf.pop(), buf.pop()]
        self.uvScale = [buf.pop(), buf.pop()]
        self.mapMode = buf.pop()
        self.mapUnit = buf.pop()
        self.mapFile = buf.pop()
        self.name = buf.pop()
        self._Done = True


class Intersection(BufferStackBase):
    def __init__(self):

        self.Astartpoint = GeVec3d()
        self.Aendpoint = GeVec3d()
        self.Bstartpoint = GeVec3d()
        self.Bendpoint = GeVec3d()
        self.crosspoint = GeVec3d()
        self.type = "None"

    def _push_to(self, buf: BufferStack):
        buf.push(self.Astartpoint.x)
        buf.push(self.Astartpoint.y)
        buf.push(self.Astartpoint.z)
        buf.push(self.Aendpoint.x)
        buf.push(self.Aendpoint.y)
        buf.push(self.Aendpoint.z)
        buf.push(self.Bstartpoint.x)
        buf.push(self.Bstartpoint.y)
        buf.push(self.Bstartpoint.z)
        buf.push(self.Bendpoint.x)
        buf.push(self.Bendpoint.y)
        buf.push(self.Bendpoint.z)
        buf.push(self.crosspoint.x)
        buf.push(self.crosspoint.y)
        buf.push(self.crosspoint.z)
        buf.push(self.type)

    def _pop_from(self, buf: BufferStack):
        self.type = buf.pop()
        self.crosspoint.z = buf.pop()
        self.crosspoint.y = buf.pop()
        self.crosspoint.x = buf.pop()
        self.Bendpoint.z = buf.pop()
        self.Bendpoint.y = buf.pop()
        self.Bendpoint.x = buf.pop()
        self.Bstartpoint.z = buf.pop()
        self.Bstartpoint.y = buf.pop()
        self.Bstartpoint.x = buf.pop()
        self.Aendpoint.z = buf.pop()
        self.Aendpoint.y = buf.pop()
        self.Aendpoint.x = buf.pop()
        self.Astartpoint.z = buf.pop()
        self.Astartpoint.y = buf.pop()
        self.Astartpoint.x = buf.pop()

    def __repr__(self):
        return 'Intersection({self.point},{self.type})'.format(self=self)


class TerminalPort(BufferStackBase):
    def __init__(self, wcenter=GeVec3d(), wsecond=GeVec3d(), wdirection=GeVec3d()):

        self.center = wcenter
        self.second = wsecond
        self.direction = wdirection

    def _push_to(self, buf: BufferStack):
        buf.push(self.center.x)
        buf.push(self.center.y)
        buf.push(self.center.z)
        buf.push(self.second.x)
        buf.push(self.second.y)
        buf.push(self.second.z)
        buf.push(self.direction.x)
        buf.push(self.direction.y)
        buf.push(self.direction.z)

    def _pop_from(self, buf: BufferStack):

        self.direction.z = buf.pop()
        self.direction.y = buf.pop()
        self.direction.x = buf.pop()
        self.second.z = buf.pop()
        self.second.y = buf.pop()
        self.second.x = buf.pop()
        self.center.z = buf.pop()
        self.center.y = buf.pop()
        self.center.x = buf.pop()


class CalloutLine(BufferStackBase):
    def __init__(self):

        self.center = GeVec3d()
        self.second = GeVec3d()
        self.direction = GeVec3d()

    def _push_to(self, buf: BufferStack):
        buf.push(self.center.x)
        buf.push(self.center.y)
        buf.push(self.center.z)
        buf.push(self.second.x)
        buf.push(self.second.y)
        buf.push(self.second.z)
        buf.push(self.direction.x)
        buf.push(self.direction.y)
        buf.push(self.direction.z)

    def _pop_from(self, buf: BufferStack):

        self.direction.z = buf.pop()
        self.direction.y = buf.pop()
        self.direction.x = buf.pop()
        self.second.z = buf.pop()
        self.second.y = buf.pop()
        self.second.x = buf.pop()
        self.center.z = buf.pop()
        self.center.y = buf.pop()
        self.center.x = buf.pop()


class TerminalPortInfo(BufferStackBase):
    def __init__(self):

        self.distance = 0.0
        self.depth = 0.0
        self.angle = 0.0

    def _push_to(self, buf: BufferStack):
        buf.push(self.distance)
        buf.push(self.depth)
        buf.push(self.angle)

    def _pop_from(self, buf: BufferStack):
        self.angle = buf.pop()
        self.depth = buf.pop()
        self.distance = buf.pop()


class ConnectingPort(BufferStackBase):
    def __init__(self):
        self.name = ''
        self.type = ''
        self.graphicsname = ''
        self.center = GeVec3d()
        self.direction = GeVec3d()

    def _push_to(self, buf: BufferStack):
        buf.push(self.name)
        buf.push(self.type)
        buf.push(self.graphicsname)
        buf.push(self.center.x)
        buf.push(self.center.y)
        buf.push(self.center.z)
        buf.push(self.direction.x)
        buf.push(self.direction.y)
        buf.push(self.direction.z)

    def _pop_from(self, buf: BufferStack):
        self.direction.z = buf.pop()
        self.direction.y = buf.pop()
        self.direction.x = buf.pop()
        self.center.z = buf.pop()
        self.center.y = buf.pop()
        self.center.x = buf.pop()
        self.graphicsname = buf.pop()
        self.type = buf.pop()
        self.name = buf.pop()


enrol(0x141762724222207, Attr)
enrol(0x1395755506582671, P3DEntityId)
enrol(0x0956146148825714, P3DModelId)
enrol(0x1395017306582671, P3DInstanceKey)
enrol(0x6239225542517109, GeTransform)
enrol(0x0005485042476852, GeVec3d)
enrol(0x0059485042476852, GeVec2d)
enrol(0x4767484556636631, P3DColorDef)
enrol(0x2624634702211655, P3DMaterial)
enrol(0x1395755514661840, Entityattribute)
enrol(0x2422220717143938, Persistent)
enrol(0x0074782073520992, Intersection)
enrol(0x6647782002071873, TerminalPort)
enrol(0x2871484802071873, CalloutLine)
enrol(0x6647782004452207, TerminalPortInfo)
enrol(0x6647223445510656, ConnectingPort)
