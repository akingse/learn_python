# Copyright (C),  2019-2028,  Beijing GLory PKPM Tech. Co.,  Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: YouQi,YanYinji
# Date: 2021/11

from .pyp3d_component import *
from .pyp3d_compat import *
import copy
import math
import sys
import time
from math import *


# ------------------------------------------------------------------------------------------
# |                                         PLACE                                          |
# ------------------------------------------------------------------------------------------

Tempfilter = ['replace','interact','Guid', 'DesignPhase', 'PBCode', 'Duration','DataSource','UserLabel', 'ClassVersion',
 'UserDescription','Domain','UpdatedTime','PBServerData','GraphicsDisplayType','Placement','BaseTransform','BaseProperty','ExtendProperty','SecondaryDevelopmentProperty',
 'ParaCmptProperty','GraphicsDisplay']
class TwoPointPlace:
    def linearize(data,  paramStr):
        data['LinearComponentLengthKey'] = paramStr
        # data[PARACMPT_KEYWORD_INTERACT] = interactLiner
        data[PARACMPT_KEYWORD_INTERACT] = Attr(UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_INTERACT_LINER),  member=True)


class RotationPlace:
    def RotationFunction(data):
        data[PARACMPT_KEYWORD_INTERACT] = Attr(UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_INTERACT_ROTATE),  member=True)
        # data[PARACMPT_KEYWORD_INTERACT] = interactRotate


class MultiPointPlace:
    def MultiPointFunction(data,  paramStr):
        data['MultiPointComponentKey'] = paramStr
        # data[PARACMPT_KEYWORD_INTERACT] = interactMultiPoint
        data[PARACMPT_KEYWORD_INTERACT] = Attr(UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_INTERACT_MULTIPOINT),  member=True)


class BoardPlace:
    def BoardPlaceFunction(data,  paramStr):
        data['boardplaceComponentKey'] = paramStr
        data[PARACMPT_KEYWORD_INTERACT] = Attr(UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_INTERACT_BOARDPLACE),  member=True)


class CombineLinePlace:
    def CombineLinePlaceFunction(data,  paramStr):
        data['CombineLinePlaceComponentKey'] = paramStr
        data[PARACMPT_KEYWORD_INTERACT] = Attr(UnifiedFunction(
            PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_INTERACT_COMBINELINEPLACE),  member=True)

def create_component(data:Noumenon):
    pyPath = sys.modules[data.__module__].__file__
    filePath = os.path.dirname(pyPath)
    fileName = os.path.splitext(os.path.basename(pyPath))[0]
    className = data.__class__.__name__
    data[PARACMPT_KEYWORD_REPLACE] = Attr(UnifiedFunction('{}/{}'.format(filePath, fileName), '{}.replace'.format(className)), member = True)
    data[PARACMPT_KEYWORD_REPRESENTATION] = '{}.{}'.format(fileName, className)
    data[PARACMPT_KEYWORD_SOURCE] = filePath
    data[PARACMTP_PLACE_CUSTOM_TOOL] = Attr(True, obvious=False, readonly=True)
    depend = DependentFile()
    depend.readFile(pyPath)
    data[PARACMPT_KEYWORD_DEPENDENT_FILE] = depend
    return data

def get_bfa_component():
    if not isinside_global_variable('bfa_component_data'):
        if not isinside_global_variable('bfa_cache_component_data'):
            nou = UnifiedFunction('BPParametricComponent', 'get_bfa_component_data_by_tool')(sys.argv[0])
            set_global_variable('bfa_cache_component_data', {sys.argv[0], nou})
            return copy.deepcopy(nou)
        else:
            cacheData = get_global_variable('bfa_cache_component_data')
            if cacheData[0] != sys.argv[0]:
                nou = UnifiedFunction('BPParametricComponent', 'get_bfa_component_data_by_tool')(sys.argv[0])
                set_global_variable('bfa_cache_component_data', {sys.argv[0], nou})
                return copy.deepcopy(nou)
            else:
                return copy.deepcopy(cacheData[1])
    else:
        return copy.deepcopy(get_global_variable('bfa_component_data'))

def place(noumenon: Noumenon):  # 通过布置工具放置组件
    if get_global_variable('is_script_to_josn'):
        set_global_variable('script_to_josn', noumenon)
    else:
        if PARACMPT_KEYWORD_DEPENDENT_FILE not in noumenon:
            depend = DependentFile()
            depend.readFile(sys.argv[0])
            noumenon[PARACMPT_KEYWORD_DEPENDENT_FILE] = depend
        UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                        PARACMPT_PLACE_INSTANCE)(noumenon)

def execute_command(str=""):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_EXECUTE_COMMAND)(str)

def get_boxselect_flag() :
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_BOXSELECT_FLAG)()
def get_entityid_from_marquee():
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ENTITYID_FROM_MARQUEE)()
def get_element_from_boxselect(str = "PyMarqueeTool") :
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ELEMENT_FROM_BOXSELECT)(str)
    while True:
            if(get_boxselect_flag()):
                return get_entityid_from_marquee()
def get_dynamic_point():
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_DYNAMIC_POINT)()
def get_pointselect_flag() :
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_POINTSELECT_FLAG)()
def get_current_point():
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_CURRENT_POINT)()
def get_point_from_pointselect() :
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_POINT_FROM_POINTSELECT)()
    while True:
            if(get_pointselect_flag()):
                return get_current_point()
def get_sub_entityid(entityid: P3DEntityId):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,PARACMPT_GET_SUB_ENTITYID)(entityid)
def get_current_entityId():
     return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_CURRENT_ENTITYID)()
def get_close_point(point,eneityId: P3DEntityId) :
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_CLOSE_POINT)(point,eneityId)
def entityid_isvaid(entityid: P3DEntityId):
    if entityid._ModelId <= -2 or entityid._ElementId < 0:return False
    return True
def entityid_isequal(entityid1: P3DEntityId,entityid2: P3DEntityId):
    if entityid1._ModelId == entityid2._ModelId and entityid1._ElementId == entityid2._ElementId:return True 
    return False
  
def Transparent(eneityId: P3DEntityId,judge:bool):  
    if not isinstance(eneityId, P3DEntityId):
        raise TypeError('input parameter error,  please input "P3DEntityId"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_TRANSPARENT)(eneityId,judge)     


def place_to(noumenon: Noumenon, transform: GeTransform = GeTransform()):  # 在特定位置布置几何体
    '''
    appoint position where geometry place to
    '''
    if PARACMPT_KEYWORD_DEPENDENT_FILE not in noumenon:
        depend = DependentFile()
        if isinside_global_variable('\a_path'):
            toolpath = get_global_variable('\a_path')
            division = ''
            if '/' in toolpath:
                division = '/'
            if '\\' in toolpath:
                division = '\\'
            pos = toolpath.rfind(division)
            modelpath = toolpath[:pos]+division+noumenon.__module__+'.py'
            noumenon[PARACMPT_KEYWORD_SOURCE] = modelpath
            noumenon[PARACMPT_KEYWORD_REPRESENTATION] = '{0}.{1}'.format(
                os.path.splitext(os.path.split(modelpath)[1])[0], type(noumenon).__name__)
            if isinside_global_variable('interface'):
                noumenon[PARACMPT_KEYWORD_TOOL] = toolpath[pos+1:] + \
                    '.py'+'.interface'
                set_global_variable('interface', False)
            else:
                noumenon[PARACMPT_KEYWORD_TOOL] = toolpath[pos+1:]+'.py'
            depend.readFile(toolpath[:pos], modelpath, toolpath+'.py')

        else:
            depend.readFile(sys.argv[0])
        noumenon[PARACMPT_KEYWORD_DEPENDENT_FILE] = depend
    noumenon[PARACMPT_KEYWORD_TRANSFORMATION] = transform
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    "BPParametricComponentManager::create")(noumenon)


def get_place_to_entityId():
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                           PARACMPT_GET_PLACE_TO_ENTITYID)()


def create_preview(noumenon: Noumenon):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, "create_preview")(noumenon)


def launch_tool(path: str):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_LAUNCH_TOOL)(path)
def launch_Marquee_tool(path: str):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_LAUNCH_MARQUEE_TOOL)(path)
def show_Input_Dlg(isshow: bool):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_SHOW_INPUT_DLG)(isshow)

def get_noumKV_from_instancekey(instancekey: P3DInstanceKey):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMKV_FROM_INSTANCEKEY)(instancekey)
    
def python_transformation_operation(entityid1: P3DEntityId,transform: GeTransform):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_PYTHON_TRANSFORMATION_OPERATION)(entityid1,transform)

def python_Copy_operation(entityid1: P3DEntityId,transform: GeTransform):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_PYTHON_COPY_OPERATION)(entityid1,transform)

def pack_bfa(noumenon: Noumenon, previewFile: str = None):
    if get_global_variable('is_script_to_josn'):
        set_global_variable('script_to_josn', noumenon)
    else:
        depend = DependentFile()
        depend.readFile(sys.argv[0])
        noumenon[PARACMPT_KEYWORD_DEPENDENT_FILE] = depend
        buffer = BufferStack()
        buffer += struct.pack('q', 0x0639242205534809)  # 0
        buffer += struct.pack('q', 0x0115410424290115)  # 1
        buffer += struct.pack('q', 0x0000000000000000)  # 2
        buffer += struct.pack('q', 0x0000000000000000)  # 3
        if previewFile is None:  # 默认生成
            previewFile = create_preview(noumenon)
        elif isinstance(previewFile, str):  # 给图片了 bmp
            with open(previewFile, 'rb') as f:
                previewFile = f.read()

        buffer.push({
            'version information': 0,
            'component data': noumenon,
            'resource data': None,
            'compatible file': None,
            'preview file': previewFile,
        })
        with open('{0}.bfa'.format(os.path.splitext(os.path.split(sys.argv[0])[1])[0]), 'wb') as f:
            f.write(buffer._imp)


def BPDataKey_isvaid(DataKey: P3DInstanceKey):
    if DataKey._PClassId > 0 and DataKey._P3DInstanceId >= 0:
        return True
    else:
        return False


def replace_noumenon(noumenon: Noumenon, instancekey: P3DInstanceKey):  # 重生成本体
    '''
    replace noumenon
    '''
    if not isinstance(noumenon,  Noumenon):
        raise TypeError('input parameter error,  please input "Noumenon"!')
    if not isinstance(instancekey,  P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_REPLACE_NOUMENON)(noumenon, instancekey)


def replace_noumenon_python(temp: dict, instancekey: P3DInstanceKey):
    if not isinstance(instancekey,  P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_REPLACE_NOUMENON_PYTHON)(temp, instancekey)

def replace_noumenon_python_new(temp: dict, instancekey: P3DInstanceKey):
    if not isinstance(instancekey,  P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_REPLACE_NOUMENON_PYTHON_NEW)(temp, instancekey)
# ------------------------------------------------------------------------------------------
# |                                        ENTITY                                          |
# ------------------------------------------------------------------------------------------


def delete_entity(**kwargs):  # 删除当前工程中符合条件的entity
    '''
    delete all "entity" in present project which meet the conditions
    '''
    if len(kwargs) == 0:
        raise ValueError('please input the range of "entityid"!\n')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_DELETE_ENTITY)(kwargs)


def delete_one_entity(entityid: P3DEntityId):  # 删除当前工程中的某一个entity
    '''
    delete someone "entity" in present project which meet the conditions
    '''
    if not (isinstance(entityid,  P3DEntityId)):
        raise TypeError(
            'input parameter error,  please input type of "_P3DEntityId"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_DELETE_ONE_ENTITY)(entityid)


def get_entity_property(**kwargs) -> list:  # 返回包含当前工程符合条件的entityid的列表
    '''
    return list of "entityid" in current project which meet the condition
    '''
    res = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                          PARACMPT_GET_ENTITY_PROPERTY)(kwargs)
    if len(res) == 0:
        raise ValueError(
            'there is no proper "entity",  please revise the condition\n')
        # return res
    else:
        return res


def get_entityid_from_boxselection() -> list:  # 返回当前工程中框选的entityid的列表
    '''
    return the boxselected "entityid" list in current project 
    '''
    res = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                          PARACMPT_GET_ENTITYID_FROM_BOXSELECTION)()
    if len(res) == 0:
        raise ValueError('No entity is selected,please choice again\n')

    else:
        return res


def clear_assist() -> list:  # 清空当前工程中辅助面/线的entityid的列表
    '''
    clear the auxiliary plane/line "entityid" list in current project 
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_CLEAR_ASSIST)()


def clear_entity():  # 删除当前工程中的所有entity
    '''
    delete all "entity" in present project 
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_CLEAR_ENTITY)()


def set_entity_property(**kwargs) -> list:  # 把当前工程符合条件的所有entity的属性修改为传入的条件
    '''
    change the attributes of all entities that meet the conditions of the current project to the passed in conditions
    '''
    for k, v in kwargs.items():
        if k == 'schemaname' or k == 'classname':
            raise TypeError(
                'you can not change "schemaname" and "classname"!\n')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_SET_ENTITY_PROPERTY)(kwargs)

# 根据schemaname 和 classname创建instance并返回instancekey


def create_data_datakey(schemaName: str, className: str) -> P3DInstanceKey:
    '''
    using schemaname and classname genetate 'instance',  return instancekey
    '''
    if not(isinstance(schemaName,  str) or isinstance(className, str)):
        raise TypeError('input parameter error,  please input string!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_CREATE_INSTANCE_INSTANCEKEY)(schemaName, className)

# 根据关键点返回离散后的的点


def create_bsplinepoints(controlPoints: list, curveOrder: int, discreteNum: int) -> list:
    '''
    using control points, return BsplinePoints points
    '''
    # for i in controlPoints:
    #     if not isinstance(i,GeVec2d):
    #         raise ValueError('Bspline control points must in XoY plane!')
    if curveOrder > len(controlPoints):
        raise ValueError(
            'curveOrder\'s parameter is the count of max control-points, please input proper parameter!')
    else:
        return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_CREATE_BSPLINEPOINTS)(controlPoints, curveOrder, discreteNum)

def get_bsplinepoints(*args) -> list:
    # controlPoints: list, curveOrder: int, discreteNum: int, close:bool
    if (len(args)==4):
        controlPoints=args[0]
        curveOrder=args[1]
        discreteNum=args[2]
        close=args[3]
    elif (len(args)==1) and isinstance(args[0],SplineCurve):
        controlPoints=args[0].transformation*args[0].points
        curveOrder=args[0].k
        discreteNum=args[0].num
        close=args[0].closed
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_BSPLINEPOINTS)(controlPoints, curveOrder, discreteNum, close)


def delete_data_bydatakey(instancekey: P3DInstanceKey):  # 根据instancekey删除instance
    '''
    delete 'Instance',  using instancekey
    '''
    if not isinstance(instancekey,  P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_DELETE_INSTANCE_BYINSTANCEKEY)(instancekey)


def bind_entity_data(entityid: P3DEntityId, instancekey: P3DInstanceKey):  # 将entity和instance进行绑定
    '''
    binding Entity and Instance
    '''
    if not (isinstance(entityid,  P3DEntityId) or isinstance(instancekey, P3DInstanceKey)):
        raise TypeError(
            'input parameter error,  please input "_P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_BIND_ENTITY_INSTANCE)(entityid, instancekey)

# 将entity和instance的绑定关系解绑


def removebind_entity_data(entityid: P3DEntityId, instancekey: P3DInstanceKey):
    '''
    remove binding Entity and Instance
    '''
    if not (isinstance(entityid,  P3DEntityId) or isinstance(instancekey, P3DInstanceKey)):
        raise TypeError(
            'input parameter error,  please input "_P3DEntityId" "_P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_REMOVEBIND_ENTITY_INSTANCE)(entityid, instancekey)

# 查询与instance绑定的所有entity


def get_allbinding_entity_from_data(instancekey: P3DInstanceKey):
    '''
    query all entity that binding instance
    '''
    if not isinstance(instancekey, P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ALLBINDING_ENTITY_FROM_INSTANCE)(instancekey)


def get_all_datakey() -> list:  # 获取当前工程中所有的instance，返回包含P3DInstanceKey的列表
    '''
    lookup all instance in current project,  return P3DInstanceKey list
    '''
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ALL_INSTANCEKEY)()


def get_all_entityid() -> list:  # 获取当前工程中所有的entityid，返回包含entityid的列表
    '''
    lookup all entityid in current project,  return entityid list
    '''
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ALL_ENTITYID)()
# 获取与P3DInstance绑定的Entity所在的Model，返回modelid


def get_modelid_from_data(instancekey: P3DInstanceKey) -> P3DModelId:
    '''
    get the model of the entity which is bound to instance, return modelid
    '''
    if not isinstance(instancekey, P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_MODELID_FROM_INSTANCE)(instancekey)

# 查询与entity绑定的instance,  并返回instancekey


def get_datakey_from_entity(entityid: P3DEntityId) -> P3DInstanceKey:
    '''
    get the instance bound to entity and return instancekey
    '''
    if not isinstance(entityid, P3DEntityId):
        raise TypeError('input parameter error,  please input "P3DEntityId"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_INSTANCEKEY_FROM_ENTITY)(entityid)

# 根据instancekey返回noumenon

def get_noumenon_on_entityid(entityid: P3DEntityId) -> Noumenon:
    datakey = get_datakey_from_entity(entityid)
    noumenon= get_noumenon_from_datakey(datakey)
    return noumenon

def get_active_modelId() -> P3DModelId:
    
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ACTIVE_MODELID)()
def get_entityid_by_modelid(modelid: P3DModelId) -> P3DEntityId:
    
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_ENTITYID_BY_MODELID)(modelid)

def get_entityid_by_activemodel():
    a = get_active_modelId()
    return get_entityid_by_modelid(a)
def get_noumenon_from_datakey(instancekey: P3DInstanceKey) -> Noumenon:
    '''
    get noumenon from instancekey
    '''
    if not isinstance(instancekey, P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_NOUMENON_FROM_INSTANCEKEY)(instancekey)
def get_extended_property_json(instancekey: P3DInstanceKey):
    '''
    get noumenon from instancekey
    '''
    if not isinstance(instancekey, P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_EXTENDED_PROPERTY_JSON)(instancekey)

def update_extended_property_json(json:str,instancekey: P3DInstanceKey):
    '''
    get noumenon from instancekey
    '''
    if not isinstance(instancekey, P3DInstanceKey):
        raise TypeError(
            'input parameter error,  please input "P3DInstanceKey"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_UPDATE_EXTENDED_PROPERTY_JSON)(json,instancekey)
# 返回当前的工程中AssociateModel_modelid中对应的entityid, ModelInfo_modelid中对应的entityid


def get_modelid_entityid_relation() -> dict:
    # 以及ModelInfo_modelid 与AssociateModel_modelid的对应关系
    '''
    return the dict of  relationship of ModelInfo_modelid and entityid, 
    relationship of AssociateModel_modelid and entityid, 
    relationship of ModelInfo_modelid and AssociateModel_modelid,  in present project
    '''
    res = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                          PARACMPT_GET_MODELID_ENTITYID_RELATION)()
    return {'ModelInfo_modelid_AssociateModel_modelid': res[0],
            'ModelInfo_modelid_entityid': res[1],
            'AssociateModel_modelid_entityid': res[2]}


def create_geometry(noumenon: Noumenon):  # 在全局坐标系的原点创建一个几何体
    '''
    create a geometry at the origin of the global coordinate system
    '''
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_CREATE_GEOMETRY)(noumenon)
def snapshoot_control(hide:list,show:list):
    '''
    control shapshoot show or hide time
    '''
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_SNAPSHOOT_CONTROL)(hide,show)
def snapshoot_control_turbo(hideframe:list,showframe:list,interval:int = 0):
    '''
    turbo! control shapshoot show or hide time 
    '''
    hideByteArray = []
    for hideset in hideframe:
        bs = BufferStack()
        bs.push(hideset)
        hideByteArray.append(bs._imp)
    showByteArray = []
    for showset in showframe:
        bs = BufferStack()
        bs.push(showset)
        showByteArray.append(bs._imp)
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_SNAPSHOOT_CONTROL_TURBO)(hideByteArray,showByteArray,interval)

def create_material(name: str,  **kw) -> P3DMaterial:  # 创建材质库, 返回P3DMateria对象
    '''
    create a material library and return the P3DMaterial object
    '''
    kw['Name'] = name
    mat = P3DMaterial(kw)
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_CREATE_MATERIAL)(mat)
    return mat


def update_material(name: str,  **kw) -> P3DMaterial:  #
    '''
    update a material library and return the P3DMaterial object
    '''
    kw['Name'] = name
    mat = P3DMaterial(kw)
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_UPDATE_MATERIAL)(mat)
    return mat


def exit_tool():  # 退出布置工具
    '''

    exit layout tools
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMTP_PLACE_TOOL_EXIT)()


def aaa():

    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  AAA)()


def get_tempcontext():

    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_GET_TEMPCONTEXT)()

def get_Entity_Area(entityid: P3DEntityId):

    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_GET_ENTITY_AREA)(entityid)

def get_Entity_Volume(entityid: P3DEntityId):

    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  PARACMPT_GET_ENTITY_VOLUME)(entityid)
def bbb():

    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  BBB)()


def model_show_switch(ModelId: P3DModelId, switch: bool):  # 一个model里面所有构件的可见性开关
    '''

    '''
    if not isinstance(ModelId, P3DModelId):
        raise TypeError('input parameter error,  please input "P3DModelId"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_MODEL_SHOW_SWITCH)(ModelId, switch)


def entity_show_switch(entityid: P3DEntityId, switch: bool):

    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_ENTITY_SHOW_SWITCH)(entityid, switch)


def grid_show_switch(switch: bool):  #

    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_GRID_SHOW_SWITCH)(switch)


def get_modelid_from_entityid(entityid: P3DEntityId):  # 根据entityid获取modelid
    '''

    '''
    if not isinstance(entityid, P3DEntityId):
        raise TypeError('input parameter error,  please input "P3DModelId"!')
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_GET_MODELID_FROM_ENTITYID)(entityid)

# 导出当前显示视图成为图片文件


def export_view_to_photograph(bmpPath: str, num1: int, num2: int, num3: int, num4: int):
    '''

    '''
    if not isinstance(bmpPath, str):
        raise TypeError('input parameter error,  please input "string"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT, PARACMPT_EXPORT_VIEW_TO_PHOTOGRAPH)(
        bmpPath, num1, num2, num3, num4)


def set_view_direction_by_index(num: int):  # 通过索引改变视图相机视角
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_SET_VIEW_DIRECTION_BY_INDEX)(num)


def set_view_direction_by_rotMatrix(transform: GeTransform):  # 通过旋转矩阵改变视图相机视角
    if not isinstance(transform, GeTransform):
        raise TypeError('input parameter error,  please input "GeTransform"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_SET_VIEW_DIRECTION_BY_ROTMATRIX)(transform)


def set_ucs_rotation(transform: GeTransform):
    if not isinstance(transform, GeTransform):
        raise TypeError('input parameter error,  please input "GeTransform"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_SET_UCS_ROTATION)(transform)


def get_view_scale(point: GeVec3d):  # 获取视口旋转矩阵，世界坐标转视口坐标，视口比例
    '''
    get_view_scale
    '''
    res = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                          PARACMPT_GET_VIEW_SCALE)(point)
    return res


def get_current_view_rotmatrix():  # 获取视口旋转矩阵，世界坐标转视口坐标，视口比例
    '''
    get_current_view_rotmatrix
    '''
    res = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                          PARACMPT_GET_CURRENT_VIEW_ROTMATRIX)()
    return res


def dynamic_preview(noumenon: Noumenon):  # 动态预览显示
    '''
    dynamic preview display
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMTP_PLACE_TOOL_DYNAMIC)(noumenon)


def zoom_all_view():  # 全充满显示
    '''
    zoom_all_view display
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMTP_ZOOM_ALL_VIEW)()


def create_new_view():  # 创建新窗口
    '''
    create_new_view
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_CREATE_NEW_VIEW)()


def pack_to_bfa(path: str,  noumenon: Noumenon,  files: list = []):  # 打包bfa文件
    '''
    package BFA files
    '''
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_PACK_BFA)(path,  noumenon,  files)


def interact_liner(data: P3DData,  context: dict):  # 两点布置工具（也称线性布置工具）
    '''
    two point layout tool (also known as linear layout tool)
    '''
    if 'interact_status' not in context:
        context['interact_status'] = 'firstButton'
    data = copy.deepcopy(data)
    if context['action'] == 'left down':
        if context['interact_status'] == 'firstButton':
            context['interact_status'] = 'secondButton'
            context['\tplace_1'] = context['point']
        elif context['interact_status'] == 'secondButton':
            p1 = context['\tplace_1']
            p2 = context['point']
            v12 = p2 - p1
            # v12_norm=rotation_to(v12) #带入函数
            v12_norm = norm(v12)
            if v12_norm != 0.0:
                angle_z = acos(v12.z/v12_norm)
                # if angle_z == 0.0:
                if abs(angle_z) < PL_A:
                    data.transformation *= rotate(GeVec3d(0, 1, 0),  -pi/2)
                # elif angle_z == pi:
                elif abs(abs(angle_z)-pi) < PL_A:
                    data.transformation *= rotate(GeVec3d(0, 1, 0),  pi/2)
                else:
                    r_xy = sqrt(v12.x**2 + v12.y**2)
                    angle_xy = acos(v12.x/r_xy)
                    if v12.y < 0.0:
                        angle_xy = -angle_xy
                    data.transformation *= rotate(GeVec3d(0, 0, 1),  angle_xy) * rotate(
                        GeVec3d(0, 1, 0),  angle_z-pi/2)
            data[data['LinearComponentLengthKey']] = v12_norm
            data.replace()
            place_to(data,  trans(context['\tplace_1']))
            context['interact_status'] = 'firstButton'
        else:
            pass
    elif context['action'] == 'right down':
        exit_tool()
    elif context['action'] == 'mouse movement':
        if context['interact_status'] == 'firstButton':
            dynamic_preview(trans(context['point']) * data)
        elif context['interact_status'] == 'secondButton':
            dynamic_preview(Line(context['\tplace_1'], context['point']))
        else:
            pass
    else:
        print(context)
    return context


def interact_multi_point(data: P3DData,  context: dict):  # 多点布置工具
    '''
    multipoint layout tool
    '''
    if 'interact_status' not in context:
        context['interact_status'] = 'firstButton'
    data = copy.deepcopy(data)
    if context['action'] == 'left down':
        if context['interact_status'] == 'firstButton':
            context['interact_status'] = 'secondButton'
            context['MultiPointComponentKey'] = [context['point']]
            data[data['MultiPointComponentKey']
                 ] = context['MultiPointComponentKey']
        elif context['interact_status'] == 'secondButton':
            context['MultiPointComponentKey'].append(context['point'])
        else:
            pass
    elif context['action'] == 'right down':
        data[data['MultiPointComponentKey']] = context['MultiPointComponentKey']
        data.replace()
        place_to(data,  GeTransform())
        exit_tool()
    elif context['action'] == 'mouse movement':
        if not data['MultiPointComponentKey'] in data:
            return context
        if not 'MultiPointComponentKey' in context:
            return context
        context['MultiPointComponentKey'].append(context['point'])
        data[data['MultiPointComponentKey']] = context['MultiPointComponentKey']
        data.replace()
        dynamic_preview(data)
        del context['MultiPointComponentKey'][-1]
        data[data['MultiPointComponentKey']] = context['MultiPointComponentKey']
    else:
        print(context)
    return context


def interact_rotate(data: P3DData,  context: dict):  # 旋转布置工具
    '''
    rotate layout tool
    '''
    if 'interact_status' not in context:
        context['interact_status'] = 'firstButton'
    data = copy.deepcopy(data)
    if context['action'] == 'left down':
        if context['interact_status'] == 'firstButton':
            context['interact_status'] = 'secondButton'
            context['\tplace_1'] = context['point']
        elif context['interact_status'] == 'secondButton':
            p1 = context['\tplace_1']
            p2 = context['point']
            v12 = p2 - p1
            v12_norm = norm(v12)
            if v12_norm != 0.0:
                angle_z = acos(v12.z/v12_norm)
                # if angle_z == 0.0:
                if abs(angle_z) < PL_A:
                    data.transformation *= rotate(GeVec3d(0, 1, 0),  -pi/2)
                # elif angle_z == pi:
                elif abs(abs(angle_z)-pi) < PL_A:
                    data.transformation *= rotate(GeVec3d(0, 1, 0),  pi/2)
                else:
                    r_xy = sqrt(v12.x**2 + v12.y**2)
                    angle_xy = acos(v12.x/r_xy)
                    if v12.y < 0.0:
                        angle_xy = -angle_xy
                    data.transformation *= rotate(GeVec3d(0, 0, 1),  angle_xy) * rotate(
                        GeVec3d(0, 1, 0),  angle_z-pi/2)
            data.replace()
            place_to(data,  trans(context['\tplace_1']))
            context['interact_status'] = 'firstButton'
        else:
            pass
    elif context['action'] == 'right down':
        exit_tool()
    elif context['action'] == 'mouse movement':
        if context['interact_status'] == 'firstButton':
            dynamic_preview(trans(context['point']) * data)
        elif context['interact_status'] == 'secondButton':
            dynamic_preview(Line(context['\tplace_1'], context['point']))
        else:
            pass
    else:
        print(context)
    return context


# 通过entityid返回curvearray转换的line
def get_line_from_curvearray(entityid: P3DEntityId):
    '''
    get line from entityid, only apply to curvearray
    '''
    if not isinstance(entityid, P3DEntityId):
        # if not isinstance(entityid, int):
        raise TypeError('input parameter error,  please input "entityid"!')
    para = UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                           PARACMPT_GET_LINE_FROM_CURVEARRAY)(entityid)
    if len(para) >0:
        relatedLine = para[0]
    if relatedLine.representation== "Segment":
        res=Segment(relatedLine.m_start,relatedLine.m_end)
    if relatedLine.representation== "Arc":#椭圆线
        res= relatedLine.transformation*Arc()
    if relatedLine.representation== "Line":#多段线
        res= Line(relatedLine.parts)
    if relatedLine.representation== "SplineCurve":#b样条
        res= relatedLine
    return res
def get_line_from_curvearraies(entityids: List):
    result = []
    for iter  in  entityids:
        line = get_line_from_curvearray(iter)
        result.append(line)
    return result
    


def messages(message: str):
    if not isinstance(message, str):
        raise TypeError('input parameter error,  please input "str"!')
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_MESSAGES)(message)


def boxes_selected(start: Vec3, end: Vec3):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    'boxes_selected')(start, end)


def force_refresh_screen():
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_FORCE_REFRESH_SCREEN)()


def get_terminal_port(datakey: P3DInstanceKey):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                           PARACMPT_GET_TERMINAL_PORT)(datakey)


def calculation_terminal_port(datakey: P3DInstanceKey, mousepoint: GeVec3d):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                           PARACMPT_CALCULATION_TERMINAL_PORT)(datakey, mousepoint)


def get_near_terminal_port(datakey: P3DInstanceKey, mousepoint: GeVec3d, num: int, angleMode: int):
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                           PARACMPT_NEAR_TERMINAL_PORT)(datakey, mousepoint, num, angleMode)


def set_terminal_port_point(noumenon: Noumenon, name: str, center: GeVec3d):
    noumenon[name + "连接点"] = Attr(TerminalPort(center, center))


def set_terminal_port_point_direction(noumenon: Noumenon, name: str, center: GeVec3d, direction: GeVec3d):
    noumenon[name + "连接点"] = Attr(TerminalPort(center, center, direction))


def set_terminal_port_line(noumenon: Noumenon, name: str, center: GeVec3d, second: GeVec3d):
    noumenon[name + "连接点"] = Attr(TerminalPort(center, second))


def set_terminal_port_line_direction(noumenon: Noumenon, name: str, center: GeVec3d, second: GeVec3d, direction: GeVec3d):
    noumenon[name + "连接点"] = Attr(TerminalPort(center, second, direction))

def BIMBase_command(str:str):
    UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,
                    PARACMPT_BIMBASE_COMMAND)(str)

# pyp3d_api synonym
launchData = place
createGeometry = create_geometry

create_instance_instancekey = create_data_datakey
delete_instance_byinstancekey = delete_data_bydatakey
bind_entity_instance = bind_entity_data
removebind_entity_instance = removebind_entity_data
get_allbinding_entity_from_instance = get_allbinding_entity_from_data
get_all_instancekey = get_all_datakey
get_modelid_from_instance = get_modelid_from_data
get_instancekey_from_entity = get_datakey_from_entity
get_noumenon_from_instancekey = get_noumenon_from_datakey
