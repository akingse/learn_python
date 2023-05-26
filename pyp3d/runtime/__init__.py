# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: 运行时服务，具体包括函数静动态调用，模块动态加卸载，动态对象申请释放。
# Author: YouQi
# Date: 2021/05/10

from asyncio import subprocess
from ..serialization import *
from ._communication import *
import re, sys, os, imp, threading, queue, multiprocessing
from types import FunctionType, MethodType
class _SingletonClassParent:
    _ins = {}
    def __new__(cls, *args):
        if not cls in cls._ins: cls._ins[cls] = cls.__bases__[0](*args)
        return cls._ins[cls]
def singleton(T): return type(T.__name__, (T, _SingletonClassParent), {})
@singleton
class _UnifiedModule:
    def __init__(self):
        self._name2module = {}
    def _import(self, name, reimport=False):
        part = re.findall(r'([a-zA-Z]:.*[\\/]+)*([\w\-\s（）()\.]+)', name)
        if len(part)==0:
            raise RuntimeError('[_import] format error!')
        if part[0][0] == '':
            isPathAppend = False
        else:
            isPathAppend = True
            sys.path.append(part[0][0])
        try:
            self._name2module[name] = __import__(part[0][1])
            if reimport: imp.reload(self._name2module[name])
        except Exception as e: 
            raise RuntimeError("[_import][{0}][{1}][{2}][{3}]".format(sys.path[-1], part[0][1], type(e).__name__, e))
        except: 
            raise RuntimeError('[_import] unknown error!')
        finally:
            if isPathAppend: sys.path.pop()
    def _getattr(self, module, attr):
        parts = attr.split('.')
        res = self._name2module[module]
        for part in parts :
            names = dir(res)
            if part in names:
                res = getattr(res, part)
            else:
                for name in names:
                    if name[0:2] == '__':
                        continue  
                    temp = getattr(res, name)
                    if part in dir(temp):
                        res = getattr(temp, part)
                        break
        return res
    def __call__(self, moduleName, methodName, *args):
        if moduleName == 'pyp3d' or moduleName == 'builtins':
            return eval(methodName)(*args)
        else:
            self._import(moduleName, True)
            return self._getattr(moduleName, methodName)(*args)
_sysPathSet = set()
_globalScript = os.path.splitext(sys.argv[0])[0]
# _globalSource = os.path.split(sys.argv[0])[0]
_globalSource = sys.argv[0]
def get_core_source(): 
    global _globalSource
    return _globalSource
def set_core_source(src): 
    global _globalSource, _sysPathSet
    if not src in _sysPathSet:
        sys.path.append(src)
        _sysPathSet.add(src)
        print(sys.path)
    _globalSource = src
_globalData = {}
def set_global_variable(key:str, val):
    global _globalData
    _globalData[key] = val
def get_global_variable(key:str):
    if key in _globalData:
        return _globalData[key]
    else:
        return ''
def isinside_global_variable(key:str):
    if key in _globalData.keys():
        return True
    return False
# import pyp3d as p3d
def run_script(scriptPath:str):
    global __name__, _globalSource, _globalScript
    name = __name__
    __name__ = '__main__'
    # execfile(scriptPath)
    with open(scriptPath, encoding='UTF-8') as f:
        _globalScript = os.path.splitext(scriptPath)[0]
        _globalSource = os.path.split(scriptPath)[0]
        code = compile(f.read(), scriptPath, 'exec')
        exec(code, globals(), globals())
    __name__ = name
def start_service():
    UnifiedFunction('BPParametricComponent', 'set_path')([os.path.dirname(os.path.dirname(os.path.dirname(__file__)))])
    UnifiedFunction('BPParametricComponent', 'callback_release')()
_isService = None
def runtime_is_service():
    return _isService
@singleton
class _Core(threading.Thread):
    def __init__(self, name, daemon):
        if get_global_variable('__mannerOfImport') == 'Subprocess':
            raise RuntimeError('The subprocess is prohibited from communicating with the BIMBase main process.')
        global _isService
        _isService = name == b'service'
        self._buffer = None
        self._calling = 0
        self._error = None
        self._depth = 0
        self._port = Port(name, lambda x: self._run(x))
        self._dynmap = {}
        self._deal = {
            Size_t(0x0646068661483938):self._0x0646068661483938,
            Size_t(0x6604093248142654):self._0x6604093248142654,
            Size_t(0x7234196661483938):self._0x7234196661483938,
            Size_t(0x4099393283811603):self._0x4099393283811603,
            Size_t(0x0520196661483938):self._0x0520196661483938}
        threading.Thread.__init__(self)
        self.setDaemon(daemon)
        self.start()
    def run(self):
        while True:
            self._port.send(self._deal_return(BufferStack(self._port.recv())).data)
            if not self._error is None:
                self._port = None
                self._calling = 3
                return
    def __del__(self):
        self.join()
    def __call__(self, mode, func, *args):
        self._depth += 1
        self._buffer = BufferStack()
        self._buffer.push(list(args), func, mode)
        if self._calling == 0: # 外部调用
            self._calling = 1
            while self._calling!=3:
                time.sleep(0.1)
            if not self._error is None:
                raise self._error
            self._calling = 0
        else: # -1内部调用
            outbs = BufferStack()
            outbs._imp = self._buffer.data
            self._buffer = None
            outbs.push(Size_t(0x0730002268691311)) # 命中钩子
            self._port.send(outbs.data)
            while True:
                rebs = self._deal_return(BufferStack(self._port.recv()))
                if self._calling==3:
                    break
                self._port.send(rebs.data)
        return self._buffer.pop()
    def _0x0646068661483938(self, inbs): # 反向调用
        outbs = BufferStack()
        if self._calling == 1:
            self._calling = 2
            outbs._imp = self._buffer.data
            outbs.push(Size_t(0x0730002268691311)) # 命中钩子
            self._buffer = None
        else:
            outbs.push(Size_t(0x6604093248142654)) # 返回结果
        return outbs
    def _0x6604093248142654(self, inbs): # 返回结果
        self._depth -= 1
        outbs = BufferStack()
        self._buffer = inbs
        self._calling = 3
        return outbs.push(Size_t(0x6604093248142654)) 
    def _0x7234196661483938(self, inbs): # 静态调用
        self._depth += 1
        outbs = BufferStack()
        try:
            self._calling = -1
            moduleName, methodName, args = inbs.pop(), inbs.pop(), inbs.pop()
            result = _UnifiedModule()(moduleName, methodName, *args)
            outbs.push(list(result) if isinstance(result, tuple) else result, Size_t(0x6604093248142654)) # 返回结果
        except Exception as e:
            print(e)
            outbs.clear()
            outbs.push("{0}.{1}".format(type(e).__name__, e), Size_t(0x4099393283811603)) # 发生异常
        except:
            outbs.clear()
            outbs.push("Unknown error from internal!", Size_t(0x4099393283811603)) # 发生异常
        finally:
            self._calling = 0
        return outbs
    def _0x0520196661483938(self, inbs): # 动态调用
        self._depth += 1
        outbs = BufferStack()
        try:
            self._calling = -1
            name, args = inbs.pop(), inbs.pop()
            result = self._dynmap[name](*args)
            outbs.push(list(result) if isinstance(result, tuple) else result, Size_t(0x6604093248142654)) # 返回结果
        except Exception as e: 
            outbs.clear()
            outbs.push("{0}.{1}".format(type(e).__name__, e), Size_t(0x4099393283811603)) # 发生异常
        except:
            outbs.clear()
            outbs.push("Unknown error from internal!", Size_t(0x4099393283811603)) # 发生异常
        finally:
            self._calling = 0
        return outbs
    def _0x4099393283811603(self, inbs): # 发送异常
        self._depth -= 1
        raise RuntimeError(inbs.pop())
    def _deal_return(self, inbs):
        outbs = BufferStack()
        try:
            outbs = self._deal[inbs.pop()](inbs)
        except Exception as e:
            if self._depth == 0:
                self._error = e
                outbs.push(Size_t(0x6604093248142654))
            else:
                outbs.push("{0}: {1}".format(type(e).__name__, e) , Size_t(0x4099393283811603))
        except: 
            if self._depth == 0:
                self._error = RuntimeError("Unknown error")
                outbs.push(Size_t(0x6604093248142654))
            else:
                outbs.push("Unknown error from internal!" , Size_t(0x4099393283811603))
        finally:
            return outbs
def start_runtime_service(): _Core(b'service', False)
class UnifiedFunction(BufferStackBase):
    def __init__(self, *args):
        if len(args)==0:
            self._moduleName, self._methodName = '', ''
        elif len(args)==1:
            if isinstance(args[0], FunctionType):
                self._methodName = args[0].__qualname__
                self._moduleName = args[0].__module__
                if self._moduleName == "__main__":
                    self._moduleName = _globalScript
                if len(_globalSource)==0:
                    return
                if self._moduleName[:len(_globalSource)] == _globalSource:
                    self._moduleName = '{0}'.format(self._moduleName[len(_globalSource)+1:])
            else:
                raise TypeError('')
        elif len(args)==2:
            if not isinstance(args[0], str) or not isinstance(args[0], str): raise TypeError('')
            self._moduleName, self._methodName = args[0], args[1]
        else:
            raise ValueError('')
    def __call__(self, *args):  # 全局调用
        return _Core(b'actively', True)(self._moduleName, self._methodName, *args)
    def call(self, *args):      # 本地调用
        return _UnifiedModule()(self._moduleName, self._methodName, *args)
    def _push_to(self, buf:BufferStack):
        buf.push(self._methodName, self._moduleName)
    def _pop_from(self, buf:BufferStack):
        self._moduleName = buf.pop()
        self._methodName = buf.pop()
enrol(0x4827000104282422, UnifiedFunction) # 统一函数
class UnifiedModule:
    def __init__(self, name):
        object.__setattr__(self, "name", name)
    def __getattribute__(self, name):
        return UnifiedFunction(object.__getattribute__(self, "name"), name)
class _Export: #namespace
    _export_method = {}
    inheritList=[]
    @ staticmethod # 静态方法
    def _export(fun:FunctionType):
        if not isinstance(fun, FunctionType): raise TypeError()
        if fun.__qualname__ == fun.__name__: 
            _Core(b'actively', True)._dynmap[fun.__name__] = fun #单例类
        else:
            name = '{0}.{1}'.format(fun.__module__, fun.__qualname__[0:-1-len(fun.__name__)])
            basesName=fun.__qualname__[0:-1-len(fun.__name__)]
            if(basesName not in _Export.inheritList):
                _Export.inheritList.append(fun.__qualname__[0:-1-len(fun.__name__)])
            if name in _Export._export_method:
                _Export._export_method[name].append(fun.__name__)
            else: 
                _Export._export_method[name] = [fun.__name__]
        return fun
export = _Export._export
def get_export_method(name,baseNameList): #nameClass
    if name in _Export._export_method:
        return _Export._export_method[name]
    else:
        for i in baseNameList: # has been baseNameList.reverse()
            if i in _Export._export_method:
                return _Export._export_method[i]
        return []

def import_module(name, reimport=False): return _UnifiedModule()._import(name, reimport)
def getattr_from(name, attr): return _UnifiedModule()._getattr(name, attr)
def nonstatic_call_forwarding(uf, this, args):
    res = _UnifiedModule()(uf._moduleName, uf._methodName, this, *args)
    return [this, res]
def toolevent_call_forwarding(uf, this, args):
    parts = uf._methodName.split('.')
    part = re.findall(r'([a-zA-Z]:.*[\\/]+)*([\w\-\s（）()\.]+)', uf._moduleName)
    if len(part)==0:
        raise RuntimeError('[_import] format error!')
    sys.path.append(part[0][0])
    tmpres = __import__(part[0][1])
    for part in parts :
        names = dir(tmpres)
        if part in names:
           res = _UnifiedModule()(uf._moduleName, uf._methodName, this, *args)
           return [this, res]
PARACMPT_PARAMETRIC_COMPONENT = 'BPParametricComponent'
def exe_command(command:str):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, "exe_command")(command)

import threading, multiprocessing, queue

class _Consignee(threading.Thread):
    '''
    收货方
    '''
    def __init__(self, processQueue=None):
        threading.Thread.__init__(self)
        self._processQueue = multiprocessing.Queue() if processQueue is None else processQueue
        self._localQueue = queue.Queue()
        self._threadLife = True
        self.start()
    def __del__(self):
        self._processQueue.close()
        self.join()
        self.close()
    def run(self):
        while self._threadLife:
            obj = self._processQueue.get()
            if obj is None:
                break
            self._localQueue.put(obj)
        self._threadLife = False
    def close(self):
        if self._threadLife:
            self._processQueue.put(None)
            self._threadLife = False
    def get(self, _block):
        '''
        取货
        '''
        while True:
            try:
                return self._localQueue.get(False)
            except queue.Empty: 
                if _block:
                    continue
                else:
                    break
        return None
g_mainConsignee = None
def main_consignee()->_Consignee:
    global g_mainConsignee
    if g_mainConsignee is None:
        g_mainConsignee = _Consignee() 
    return g_mainConsignee
def clear_main_consignee():
    global g_mainConsignee
    if g_mainConsignee is None:
        return
    g_mainConsignee.close()
    g_mainConsignee = None
class MainProcessPort:
    def __init__(self, mainProcessQueue:multiprocessing.Queue, subprocessQueue:multiprocessing.Queue):
        self._mainProcessQueue = mainProcessQueue
        self._consignee = _Consignee(subprocessQueue)
    def __del__(self):
        self._consignee.close()
        self._mainProcessQueue.close()
    def send(self, *args):
        self._mainProcessQueue.put(args)
    def recv(self, _block=False):
        return self._consignee.get(_block)

class Pyp3dSubprocess(multiprocessing.Process):
    def __init__(self, targe,args):
        multiprocessing.Process.__init__(self, target=self.run, args=(self,))
        self._targe = targe
        self._args = args
        self._mainProcessQueue = main_consignee()._processQueue
        self._subprocessQueue = multiprocessing.Queue()
        sys.path.append('*'+str(get_global_variable('__version')))
        self.start()
    def __del__(self):
        self._subprocessQueue.close()
        time.sleep(1)
        self._mainProcessQueue.close()
    def run(self):
        mainProcessPort = MainProcessPort(self._mainProcessQueue, self._subprocessQueue)
        self._targe(mainProcessPort,self._args)
        mainProcessPort._consignee.close()
        print("run exit")
    def send(self, *args):
        self._subprocessQueue.put(args)
    def recv(self, _block=False):
        return main_consignee().get(_block)
    def suicide(self):
        self.join()
        self.close()

g_subprocess = dict()
def setPyp3dSubprocess(process:Pyp3dSubprocess, index=0):
    global g_subprocess
    if process is None and g_subprocess[index] is not None:
        g_subprocess[index].suicide()
    g_subprocess[index] = process
def getPyp3dSubprocess(index=0):
    return g_subprocess[index]