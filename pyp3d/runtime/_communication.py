# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: Python与Cpp之间的通信协议
# Author: YouQi
# Date: 2021/05/06
_EXE_NAME = b"BIMBASE.exe" #b'TestGeometryForPython.exe'
import time, platform, threading, types, struct, sys, os
from typing import overload
if "Windows" == platform.system(): from . import _windows_interface as _c_i
else: raise AssertionError()
class NamedPipe:
    def __init__(self, pid, name, is_create=False):
        self.handle = _c_i.create_named_pipe(pid, name) if is_create else _c_i.wait_named_pipe(pid, name)
        if self.handle is None: raise RuntimeError('wait error')
    def __del__(self):
        _c_i.close_named_pipe(self.handle)
    def recv(self):
        return _c_i.recv(self.handle)
    def send(self, data):
        return _c_i.send(self.handle, data)
class ConnectNamedPipe:
    def __init__(self, namedPipe):
        self._namedPipe = namedPipe
    def __enter__(self):
        _c_i.connect_named_pipe(self._namedPipe.handle)
    def __exit__(self, exc_type, exc_value, traceback):
        _c_i.disconnect_named_pipe(self._namedPipe.handle)
class Mutex:
    def __init__(self, pid, name, is_create=False):
        self.handle = _c_i.create_mutex(pid, name) if is_create else _c_i.open_mutex(pid, name)
    def __del__(self):
        _c_i.close_mutex(self.handle)
class LockMutex:
    def __init__(self, mutex, timeout=1000):
        self._mutex = mutex
        self._timeout = timeout
    def __enter__(self):
        if not _c_i.lock(self._mutex.handle, self._timeout):
            raise RuntimeError('lock error')
    def __exit__(self, exc_type, exc_value, traceback):
        if not _c_i.unlock(self._mutex.handle):
            print('unlock error')
class Kaishaku(threading.Thread):
    def __init__(self, pid):
        self.ck_pid = pid
        threading.Thread.__init__(self)
    def run(self): 
        _c_i.kaishaku(self.ck_pid)
class Port:
    def __init__(self, name, deal):
        self._portname = name
        self._deal = deal
        if len(sys.argv) > 1:
            self._pid = sys.argv[1]
        else:
            while True:
                pids = _c_i.find_porcess(_EXE_NAME)
                if len(pids) == 0: 
                    raise RuntimeError('{0} not found. Please start {0}.'.format(_EXE_NAME))
                elif len(pids) == 1: 
                    self._pid = pids[0]
                    break
                foreground_pid = _c_i.get_foreground_pid()
                if foreground_pid in pids:
                    self._pid = foreground_pid
                    break
                time.sleep(1)
        self._kaishaku = Kaishaku(self._pid)
        self._kaishaku.setDaemon(True)
        self._kaishaku.start()
        self._connect()
    def _connect(self):
        while True:
            try:
                self._pipe = NamedPipe(self._pid, self._portname)
                break
            except RuntimeError: time.sleep(1)
    def recv(self):
        while True:
            content = self._pipe.recv()
            if content != None: return content
            self._connect()
    def send(self, buffer):
        while True:
            if self._pipe.send(buffer): break
            self._connect()