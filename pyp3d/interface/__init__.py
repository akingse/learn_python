import inspect
from pyp3d import *
import os
import sys

path = sys.argv[0]
if get_global_variable('__mannerOfImport') == 'Subprocess':
    def setcontext(context: dict):send_msg_to_tool('setcontext',context)
    #轮询分发函数
    def toolevents(self):
        tool = get_global_variable("Handle")
        res = tool.recv()
        if res == None:...
        elif res[0]=='context':
            set_global_variable("context",res[1])
        elif res[0] in dir(self):
            result = getattr(self,res[0])()
            if isinstance(result,dict):
                setcontext(result)
        else:...
    def getcontext():
        return get_global_variable("context")
    #判断有效性
    def entityid_isvaid(entityid:P3DEntityId):
        if entityid._ModelId<=-2 or entityid._ElementId <0:
            return False
        else:
            return True
    def BPDataKey_isvaid(DataKey:P3DInstanceKey):
        if DataKey._PClassId>0 and  DataKey._P3DInstanceId >=0:
            return True
        else:
            return False
   
    #向工具发送消息
    def send_msg_to_tool(name,args):
        tool = get_global_variable("Handle")
        tool.send(name,args)
    #不带返回值的函数
    def exit_tool():send_msg_to_tool('exit_tool',None)
    def messages(msg):send_msg_to_tool('messages',msg)
    def place_to(noumenon: Noumenon, transform: GeTransform):send_msg_to_tool('place_to',[noumenon,transform])
    def set_ucs_rotation( transform: GeTransform):send_msg_to_tool('set_ucs_rotation',transform)
    def delete_one_entity(entityid: P3DEntityId):send_msg_to_tool('delete_one_entity',entityid)
    def clear_entity():send_msg_to_tool('clear_entity',None)
    def model_show_switch(ModelId: P3DModelId, switch: bool):send_msg_to_tool('model_show_switch',[ModelId,switch])
    def entity_show_switch(entityid:P3DEntityId, switch: bool):send_msg_to_tool('entity_show_switch',[entityid,switch])
    def export_view_to_photograph(bmpPath: str, num1: int, num2: int, num3: int, num4: int):send_msg_to_tool('export_view_to_photograph',[bmpPath,num1,num2,num3,num4])
    def set_view_direction_by_index(num: int):send_msg_to_tool('set_view_direction_by_index',num)
    def set_view_direction_by_rotMatrix(transform: GeTransform):send_msg_to_tool('set_view_direction_by_rotMatrix',transform)
    def dynamic_preview(noumenon: Noumenon):send_msg_to_tool('dynamic_preview',noumenon)
    def delete_data_bydatakey(instancekey: P3DInstanceKey):send_msg_to_tool('delete_data_bydatakey',instancekey)
    def zoom_all_view():send_msg_to_tool('zoom_all_view',None)
    def create_new_view():send_msg_to_tool('create_new_view',None)
    def replace_noumenon(noumenon: Noumenon, instancekey: P3DInstanceKey):send_msg_to_tool('replace_noumenon',[noumenon,instancekey])
    def bind_entity_data(entityid: P3DEntityId, instancekey: P3DInstanceKey):send_msg_to_tool('bind_entity_data',[entityid,instancekey])
    def removebind_entity_data(entityid: P3DEntityId, instancekey: P3DInstanceKey):send_msg_to_tool('removebind_entity_data',[entityid,instancekey])
    
    #带返回值的函数
    #根据关键点返回离散后的的点
    def create_bsplinepoints(controlPoints: list, curveOrder: int, discreteNum: int):
        tool = get_global_variable("Handle")
        tool.send('create_bsplinepoints',controlPoints,curveOrder,discreteNum)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='create_bsplinepoints':
                return restmp[1]
    def get_datakey_from_entity(entityid: P3DEntityId):
        tool = get_global_variable("Handle")
        tool.send('get_datakey_from_entity',entityid)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_datakey_from_entity':
                return restmp[1]
    def get_place_to_entityId():
        tool = get_global_variable("Handle")
        tool.send('get_place_to_entityId',None)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_place_to_entityId':
                return restmp[1]
    def get_entityid_from_boxselection():
        tool = get_global_variable("Handle")
        tool.send('get_entityid_from_boxselection',None)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_entityid_from_boxselection':
                return restmp[1]           
    def create_data_datakey(schemaName: str, className: str):
        tool = get_global_variable("Handle")
        tool.send('create_data_datakey',schemaName, className)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='create_data_datakey':
                return restmp[1]    
    def get_allbinding_entity_from_data(instancekey: P3DInstanceKey):
        tool = get_global_variable("Handle")
        tool.send('get_allbinding_entity_from_data',instancekey)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_allbinding_entity_from_data':
                return restmp[1]   
    def get_all_datakey():
        tool = get_global_variable("Handle")
        tool.send('get_all_datakey',None)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_all_datakey':
                return restmp[1] 
    def get_all_entityid():
        tool = get_global_variable("Handle")
        tool.send('get_all_entityid',None)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_all_entityid':
                return restmp[1] 
    def get_modelid_from_data(instancekey: P3DInstanceKey):
        tool = get_global_variable("Handle")
        tool.send('get_modelid_from_data',instancekey)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_modelid_from_data':
                return restmp[1]  
    def get_noumenon_from_datakey(instancekey: P3DInstanceKey):
        tool = get_global_variable("Handle")
        tool.send('get_noumenon_from_datakey',instancekey)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_noumenon_from_datakey':
                return restmp[1]  
    def create_geometry(noumenon: Noumenon): 
        tool = get_global_variable("Handle")
        tool.send('create_geometry',noumenon)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='create_geometry':
                return restmp[1]  
    def get_modelid_from_entityid(entityid: P3DEntityId): 
        tool = get_global_variable("Handle")
        tool.send('get_modelid_from_entityid',entityid)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_modelid_from_entityid':
                return restmp[1]  
    def get_current_view_rotmatrix(): 
        tool = get_global_variable("Handle")
        tool.send('get_current_view_rotmatrix',None)
        while True:
            restmp = tool.recv(True)
            if restmp[0]=='get_current_view_rotmatrix':
                return restmp[1]  
    
def launch_interface(path):  
    path1 = inspect.getfile(inspect.currentframe())
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,PARACMPT_LAUNCH_INTERFACE)(path1,path)

def initPath(context):
    set_global_variable('\a_path',context['interfacepath']) 
    set_global_variable('interface',True)   

def init_ui(tool,path):
    set_global_variable("Handle",tool)
    set_global_variable("Events",set())
    set_global_variable("context",True)
    part = re.findall(r'([a-zA-Z]:.*[\\/]+)*([\w\-\s（）()\.]+)',path)
    if len(part)==0:
        raise RuntimeError('[_import] format error!')
    if '.py' in part[0][1]:
        temp = part[0][1].replace('.py','')
    __import__(temp)
    tool.send(None)
    set_global_variable('Handle', None)
    
def startInterface(context):
    if 'interfacepath' in context:
        setPyp3dSubprocess(Pyp3dSubprocess(init_ui,context['interfacepath']+'.py'))  # 传入函数
def receive_msg_from_interface():
    rec = getPyp3dSubprocess().recv()
    if rec == None:return '_'
    args = list(rec[1:])
    if rec[0] == 'setcontext':
        return args[0]
    elif len(args) == 1 and args[0] == None:
        tmp = rec[0] + '()'
        res = eval(tmp)
        getPyp3dSubprocess().send(rec[0], res)
        return '_'
    elif len(args) == 1 and isinstance(args[0], list):
        res = eval(rec[0])(*args[0])
        getPyp3dSubprocess().send(rec[0], res)
        return '_'
    else:
        if rec[0] is None:
            return '_'
        res = eval(rec[0])(*args)
        getPyp3dSubprocess().send(rec[0], res)
        return '_'
    
def onInit(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onInit')
    receive_msg_from_interface()
    
def onLeftDown(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onLeftDown')
    receive_msg_from_interface()

def onRightDown(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onRightDown')
    receive_msg_from_interface()

def onMouseMove(context):
    res = receive_msg_from_interface()
    if isinstance(res,dict):
        for k,j in res.items():
            context[k]= j
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onMouseMove')
    
    
def onKeyDown(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onKeyDown')
    receive_msg_from_interface() 
def onMouseWheel(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onMouseWheel')
    receive_msg_from_interface() 
def onStartDrag(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onStartDrag')
    receive_msg_from_interface() 
def onEndDrag(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onEndDrag')
    receive_msg_from_interface() 
def onDataButtonUp(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onDataButtonUp')
    receive_msg_from_interface() 
def onExit(context):
    getPyp3dSubprocess().send('context', context)
    getPyp3dSubprocess().send('onExit')
    receive_msg_from_interface() 
    clear_main_consignee()
    setPyp3dSubprocess(None)
if 'service0' not in path:
    if get_global_variable('__mannerOfImport') == 'Client':
        launch_interface(path)
        exit(0)
    