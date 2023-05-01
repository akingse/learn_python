# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: Windows版本接口
# Author: YouQi
# Date: 2021/05/06
import ctypes, time, os, signal, struct, sys
kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32
NULL = 0
FALSE = 0
HANDLE = ctypes.c_void_p
DWORD = ctypes.c_ulong
LPDWORD = ctypes.POINTER(DWORD)
CHAR = ctypes.c_char
ULONG_PTR = ctypes.c_ulonglong
PROCESS_QUERY_INFROMATION = 0x00001000
TH32CS_SNAPPROCESS = 0x00000002
GW_HWNDNEXT = 0x00000002
SYNCHRONIZE = 0x00000400
MUTEX_ALL_ACCESS = 0x000F0000 | 0x00100000 | 0x0001
MAX_PATH = 260
PIPE_ACCESS_DUPLEX = 0x00000003
PIPE_WAIT = 0x00000000
PIPE_UNLIMITED_INSTANCES = 255
NMPWAIT_WAIT_FOREVER = 0xffffffff
GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x00000080
INVALID_HANDLE_VALUE = -1
WAIT_OBJECT_0 = 0x00000000
WAIT_TIMEOUT = 258
WAIT_ABANDONED = 0x00000080
WAIT_FAILED = 0xffffffff
TRUE = 1
class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", DWORD), 
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", ULONG_PTR),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", DWORD),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * MAX_PATH)]
class ExitCodeProcess(ctypes.Structure):
    _fields_ = [ 
        ('hProcess', HANDLE),
        ('lpExitCode', LPDWORD)]
def _is_debug():
    return b'' if len(sys.argv) > 1 else b'D'
def kaishaku(pid):
    mutexName = b"PYP3DMUTEX" + str(pid).encode(encoding='GBK')
    while True:
        time.sleep(1)
        process = kernel32.OpenProcess(PROCESS_QUERY_INFROMATION, 0, int(pid))
        if process == 0: os.kill(os.getpid(), signal.SIGILL)
        ec = ExitCodeProcess()
        out = kernel32.GetExitCodeProcess(process, ctypes.byref(ec))
        kernel32.CloseHandle(process)
        if bool(ec.lpExitCode): os.kill(os.getpid(), signal.SIGILL)
        mutex = kernel32.OpenMutexA(MUTEX_ALL_ACCESS, FALSE, mutexName)
        if mutex == 0: os.kill(os.getpid(), signal.SIGILL)
        kernel32.CloseHandle(mutex)
def find_porcess(name):
    pids = []
    hProcessSnap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
    if kernel32.Process32First(hProcessSnap,ctypes.byref(pe32)) == False: return pids
    while True:
        while name == pe32.szExeFile:
            process = kernel32.OpenProcess(SYNCHRONIZE, 0, pe32.th32ProcessID)
            if not process: break
            ec = ExitCodeProcess()
            out = kernel32.GetExitCodeProcess(process, ctypes.byref(ec))
            if not out:
                print('find_porcess error : GetLastError{0}'.format(kernel32.GetLastError()))
                kernel32.CloseHandle(process)
                break
            if bool(ec.lpExitCode):
                kernel32.CloseHandle(process)
                break
            kernel32.CloseHandle(process)
            pids.append(pe32.th32ProcessID)
            break
        if kernel32.Process32Next(hProcessSnap,ctypes.byref(pe32)) == False: break
        pe32.szExeFile
    kernel32.CloseHandle(hProcessSnap)
    return pids
def get_foreground_pid():
    lpdw_process_id = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), ctypes.byref(lpdw_process_id))
    return lpdw_process_id.value
def wait_named_pipe(pid, name):
    name = b"\\\\.\\Pipe\\PYP3D\\PIPE" + str(pid).encode(encoding='GBK') + name
    if TRUE != kernel32.WaitNamedPipeA(name, NMPWAIT_WAIT_FOREVER):
        print('wait_named_pipe error : GetLastError{0}'.format(kernel32.GetLastError()))
        return None
    handle = kernel32.CreateFileA(name, GENERIC_WRITE | GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL)
    if INVALID_HANDLE_VALUE == handle:
        kernel32.CloseHandle(handle)
        print('wait_named_pipe error : GetLastError{0}'.format(kernel32.GetLastError()))
        return None
    return handle
def create_named_pipe(pid, name):
    name = b"\\\\.\\Pipe\\PYP3D\\PIPE" + str(pid).encode(encoding='GBK') + name
    handle = kernel32.CreateNamedPipeA(name, PIPE_ACCESS_DUPLEX, PIPE_WAIT, PIPE_UNLIMITED_INSTANCES, 0, 0, 1000, NULL)
    if INVALID_HANDLE_VALUE == handle:
        print('create_named_pipe : GetLastError{0}'.format(kernel32.GetLastError()))
        return None
    return handle
def connect_named_pipe(handle):
    if not kernel32.ConnectNamedPipe(handle, NULL):
        print('connect_named_pipe : GetLastError{0}'.format(kernel32.GetLastError()))
        return False
    return True
def disconnect_named_pipe(handle):
    if not handle is None:
        kernel32.DisconnectNamedPipe(handle)
def close_named_pipe(handle):
    if not handle is None:
        kernel32.DisconnectNamedPipe(handle)
        kernel32.CloseHandle(handle)
def recv(handle):
    if INVALID_HANDLE_VALUE == handle: return None
    buffSize = ctypes.c_ulonglong()
    readSize = DWORD()
    if (FALSE == kernel32.ReadFile(handle, ctypes.byref(buffSize), 8, ctypes.byref(readSize), NULL)):
        err = kernel32.GetLastError()
        if err == 233: return None
        print('recv error : GetLastError{0}'.format(err))
        return None
    if (8 != readSize.value):
        print('recv error : Failed to read message length.')
        return None
    if (0 == buffSize.value): return b''
    buf = (ctypes.c_char*buffSize.value)()
    if (FALSE == kernel32.ReadFile(handle, ctypes.byref(buf), buffSize, ctypes.byref(readSize), NULL)):
        print('recv error : GetLastError{0}'.format(kernel32.GetLastError()))
        return None
    if (buffSize.value != readSize.value):
        print('recv error : Failed to read message.')
        return None
    return buf.raw
def send(handle, data):
    if INVALID_HANDLE_VALUE == handle: return False
    content = struct.pack('Q', len(data)) + data
    buf = (ctypes.c_char*len(content))()
    buf.value = content
    writeSize = DWORD()
    result= kernel32.WriteFile(handle, ctypes.byref(buf), len(buf), ctypes.byref(writeSize), NULL)
    if writeSize.value != len(buf):
        print('send error : GetLastError{0}'.format(kernel32.GetLastError()))
        return False
    return True
def create_mutex(pid, name):
    handle = kernel32.CreateMutexA(NULL, FALSE, b'PYP3DPPSYNC'+str(pid).encode(encoding='GBK') + name)
    if handle == 0:
        print('create_mutex error : GetLastError{0}'.format(kernel32.GetLastError()))
        return None
    return handle
def open_mutex(pid, name):
    handle = kernel32.OpenMutexA(MUTEX_ALL_ACCESS, FALSE, b'PYP3DPPSYNC'+str(pid).encode(encoding='GBK') + name)
    if handle == 0:
        print('open_mutex error : GetLastError{0}'.format(kernel32.GetLastError()))
        return None
    return handle
def close_mutex(handle):
    kernel32.CloseHandle(handle)
def lock(handle, timeout:int) -> bool:
    while True:
        reSing = kernel32.WaitForSingleObject(handle, timeout)
        if reSing == WAIT_OBJECT_0: return True
        elif reSing == WAIT_TIMEOUT: print('lock error : timeout.')
        elif reSing == WAIT_ABANDONED: continue
        else: print('lock error : GetLastError{0}'.format(kernel32.GetLastError()))
        return False
def unlock(handle) -> bool:
    return kernel32.ReleaseMutex(handle)
