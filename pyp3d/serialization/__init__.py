# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: 持久化标准
# Author: YouQi
# Date: 2021/05/10
import os
import struct
from typing import List, overload
MARKER_LENGTH, INFOR_LENGTH, ULL, ERROR_INOFR = 8, 16, 'Q', '[serialization]: deserialization error.'
class BufferStack:
    '''
    缓存区栈对象，用于数据传输承载数据对象。
    '''
    type2push, tid2pop = {}, {}
    def __init__(self, bs=bytearray()): 
        self._imp = bytearray(bs)
        self._offset = 0
    @property
    def data(self) -> bytearray: return (self._imp if self._offset==0 else self._imp[:-self._offset])
    def __add__(self, other) -> bytearray: return (self._imp if self._offset==0 else self._imp[:-self._offset]) + other
    def __radd__(self, other) -> bytearray: return other + self._imp if self._offset==0 else self._imp[:-self._offset]
    def __iadd__(self, other):
        self._imp = (self._imp if self._offset==0 else self._imp[:-self._offset]) + other
        self._offset = 0
        return self
    def push(self, *args) -> None:
        '''
        将对象序列化后，压栈缓存区栈对象。
        '''
        for arg in args:
            T = type(arg)
            while not T in BufferStack.type2push: 
                T = T.__base__
                if T == object: raise TypeError('该类型尚未注册序列化方法[{0}]\n{1}'.format(T.__name__, arg))                
            infor = BufferStack.type2push[T]
            temp = infor[1](arg)
            content = temp + struct.pack(ULL, len(temp)) + struct.pack(ULL, infor[0])
            if self._offset==0:
                self._imp += content
            else:
                self._imp = self._imp[:-self._offset] + content
                self._offset = 0
        return self
    def pop(self) -> object:
        '''
        出栈缓存区对象后，执行反序列化。
        '''
        infor = self._imp[-self._offset-INFOR_LENGTH:] if self._offset==0 else self._imp[-self._offset-INFOR_LENGTH:-self._offset]
        if len(infor) != INFOR_LENGTH: raise RuntimeError(ERROR_INOFR)
        size = struct.unpack(ULL, infor[:MARKER_LENGTH])[0]
        tid = struct.unpack(ULL, infor[-MARKER_LENGTH:])[0]
        temp_buffer = self._imp[-self._offset-size-INFOR_LENGTH:-self._offset-INFOR_LENGTH]
        if len(temp_buffer) != size: raise RuntimeError(ERROR_INOFR)
        if not tid in BufferStack.tid2pop: raise TypeError(ERROR_INOFR)
        obj = BufferStack.tid2pop[tid](BufferStack(temp_buffer))
        self._offset += size + INFOR_LENGTH
        return obj
    def clear(self):
        '''
        清空缓存区栈对象。
        '''
        self._imp.clear()
        self._offset = 0
@overload
def enrol(tid:int, tp:type) -> None:...
@overload
def enrol(tid:int, tp:type, push, pop) -> None:...
def enrol(*args):
    '''
    注册类型以用于支持数据传输。
    '''
    BufferStack.type2push[args[1]] = (args[0],  _PushBufferStackBase() if len(args) == 2 else args[2])
    BufferStack.tid2pop[args[0]] = _PopBufferStackBase(args[1]) if len(args) == 2 else args[3]
class _PushBufferStackBase:
    def __call__(self, obj):
        bs = BufferStack()
        obj._push_to(bs)
        return bs.data
class _PopBufferStackBase:
    def __init__(self, tp): self._type = tp
    def __call__(self, bs):
        obj = self._type()
        result = obj._pop_from(bs)
        return obj if (result is None) else result
class BufferStackBase:
    '''
    可传输对象基类，子类需重写两个方法
    _push_to 序列化方法，需根据自身填充BufferStack
    _pop_from 反序列化方法，需根据BufferStack内容初始化自身，无需返回值（不可变对象需使用返回值）
    '''
    def _push_to(self, bs:BufferStack)->None: raise NotImplementedError()
    def _pop_from(self, bs:BufferStack)->None: raise NotImplementedError()
class DependentFile(BufferStackBase):
    '''
    依赖文件
    '''
    def __init__(self):
        self.fildor = []
    def readFile(self, path:str):
        self.fildor = self._getAllFile(path)
    def _getAllFile(self, path:str):
        if path == "":
            return
        if os.path.isdir(path):
            pathList = []
            dirs = os.listdir(path)
            for dir in dirs:
                dirPath = os.path.join(path, dir)
                res = self._getAllFile(dirPath)
                if len(res) != 0:
                    pathList.append(res)
            if len(pathList) == 0:
                return []
            else:
                return [pathList, True, os.path.split(path)[1]]
        else:
            f = open(path, 'rb')
            content = f.read()
            f.close()
            return [bytearray(content), False, os.path.split(path)[1]]
    def _readFromFolder(self, pathList:list, bs):
        for path in pathList:
            if path[1]:
                if not isinstance(path[0], bool):
                    self._readFromFolder(path[0], bs)
            else:
                bs.push(path[0])
            bs.push(path[1])
            bs.push(path[2])
        bs.push(Size_t(len(pathList)))
    def _resetToFolder(self, pathList:list, bs):
        for _ in range(bs.pop()):
            fileName = bs.pop()
            if bs.pop():
                filelist = []
                self._resetToFolder(filelist, bs)
                if len(filelist) == 1 & filelist[0][1]:
                    filelist = filelist[0]
                else:
                    filelist.reverse()
                pathList.append([filelist, True, fileName])
            else:
                pathList.append([bs.pop(), False, fileName])
    def _push_to(self, bs):
        if len(self.fildor) == 0:
            return
        if isinstance(self.fildor[0], bytearray):
            self._readFromFolder([self.fildor], bs)
        else:
            self._readFromFolder(self.fildor[0], bs)
            bs.push(self.fildor[1])
            bs.push(self.fildor[2])
            bs.push(Size_t(1))
    def _pop_from(self, bs):
        self._resetToFolder(self.fildor, bs)
        self.fildor = self.fildor[0]
class Size_t(BufferStackBase, int):
    '''
    C++类型。
    size_t, unsigned long long.
    '''
    def __new__(cls, *args, **kw): return int.__new__(cls, *args, **kw)
    def _push_to(self, bs): bs += struct.pack(ULL, self)
    def _pop_from(self, bs): return Size_t(struct.unpack(ULL, bs.data)[0])
def _push_list(value: list):
    bs = BufferStack()
    bs.push(*value[::-1])
    return bs.push(Size_t(len(value))).data
def _push_dict(value: dict):
    bs = BufferStack()
    for k,v in value.items(): bs.push(v, k)
    return bs.push(Size_t(len(value))).data
def _pop_dict(bs:BufferStack):
    element = [bs.pop() for _ in range(bs.pop()*2)]
    return dict(zip(element[0::2], element[1::2]))
enrol(0x4500450011720048, type(None), lambda x: b'', lambda x: None)
enrol(0x1580142273520992, bool, lambda x: struct.pack('?', x), lambda x: struct.unpack('?', x.data)[0])
enrol(0x7175318778202422, float, lambda x: struct.pack('d', x), lambda x: struct.unpack('d', x.data)[0])
enrol(0x4569571470222419, int, lambda x: struct.pack('q', x), lambda x: struct.unpack('q', x.data)[0])
enrol(0x0181635124290115, DependentFile)
enrol(0x2477702224190092, Size_t)
enrol(0x1316456973520092, str, lambda x: x.encode(encoding='GBK'), lambda x: x.data.decode(encoding='GBK'))
enrol(0x0059665104550025, bytearray, lambda x: x, lambda x: x.data)
enrol(0x0059665104550025, bytes, lambda x: x, lambda x: x.data)
enrol(0x3131099213160368, dict, _push_dict, _pop_dict)
enrol(0x3131099204415903, list, _push_list, lambda x:[x.pop() for _ in range(x.pop())])


if __name__ == "__main__":
    '''
    效率测试
    '''
    if False:
        bs = BufferStack()
        depend = DependentFile()
        depend.readFile("C:\\Users\\wuguoliang\\Desktop\\a")
        print(depend.fildor)
        bs.push(depend)
        # bs.push(Size_t(123456))
        # bs.push(-123456)
        # bs.push('sdf')
        # bs.push([1,3,'1abb'])
        # bs.push(1, {'k1':'v1','k2':'v2','k3':'v3'})
        # print(bs.pop())
        # print(bs.pop())
        # print(bs.pop())
        # print(bs.pop())
        # print(bs.pop())
        # print(bs.data)
        bs.pop()
    if False:
        import time
        for num in [10000, 100000, 1000000, 10000000]:
            start = time.time()
            bs = BufferStack()
            for _ in range(num):
                bs.push(1234)
            print(time.time() - start)
            start = time.time()
            for _ in range(num):
                bs.pop()
            print(time.time() - start)
    if False:
        import time
        string = '0123456789'*10
        for num in [10000, 100000, 1000000, 10000000]:
            print(num)
            start = time.time()
            bs = BufferStack()
            for _ in range(num):
                bs.push(string)
            print(time.time() - start)
            start = time.time()
            for _ in range(num):
                bs.pop()
            print(time.time() - start)
    if True:
        import time
        obj = {str(i):i for i in range(100)}
        for num in [100, 1000, 10000, 100000]:
            print(num)
            start = time.time()
            bs = BufferStack()
            for _ in range(num):
                bs.push(obj)
            print(time.time() - start)
            start = time.time()
            for _ in range(num):
                bs.pop()
            print(time.time() - start)


# 序列化与反序列化性能测试
# 
# 测试对象：int
#       1w      10w     100w    1000w
# push  0.0518  0.5400  6.1451  58.200
# pop   0.1093  1.0478  11.906  108.50
# 
# 测试对象：str  长度=100
#       1w      10w     100w    1000w
# push  0.0830  0.7177  7.0268  72.846
# pop   0.1289  1.1718  12.184  122.32
# 
# 测试对象：map<str, int>  数量=100 倍率=200
#       0.01w   0.1w    1w      10w
# push  0.1132  0.9736  9.1283  98.212
# pop   0.2090  2.3468  22.032  231.05
# 