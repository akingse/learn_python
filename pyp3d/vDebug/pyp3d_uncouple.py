# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: YouQi
# Date: 2021/10

from .pyp3d_component import *
from .pyp3d_compat import *


def _push_noumenon(value):
    bs = BufferStack()
    # 自动装载表象名
    if not runtime_is_service() and issubclass(type(value), Component) and type(value).__name__ != 'Component':
        value.at(PARACMPT_KEYWORD_SOURCE).setup(obvious=False, readonly=True)
        value.at(PARACMPT_KEYWORD_REPRESENTATION).setup(
            obvious=False, readonly=True)
        value[PARACMPT_KEYWORD_SOURCE] = get_core_source()
        value[PARACMPT_KEYWORD_REPRESENTATION] = '{0}.{1}'.format(
            os.path.splitext(os.path.split(sys.argv[0])[1])[0], type(value).__name__)
    # 导出函数UF化
    baseNameList = []  # class inherite list
    # if issubclass(value.__class__,Component) and (value.__class__.__name__ !='Component'): #make sure itis subclass of Component
    if issubclass(type(value), Component) and type(value).__name__ != 'Component':
        if len(value.__class__.__bases__) >= 1:
            baseClassName = value.__class__.__bases__[0]
            baseName = '{0}.{1}'.format(
                baseClassName.__module__, baseClassName.__name__)
            # while(baseName!='pyp3d.v18446497929133883392.pyp3d_component.Component'):
            while (baseClassName.__name__ != 'Component'):
                baseNameList.append(baseName)
                if len(baseClassName.__bases__) >= 1:
                    baseClassName = baseClassName.__bases__[0]
                    baseName = '{0}.{1}'.format(
                        baseClassName.__module__, baseClassName.__name__)
    for methodName in get_export_method('{0}.{1}'.format(type(value).__module__, type(value).__name__), baseNameList):
        value[methodName] = Attr(UnifiedFunction(
            getattr(type(value), methodName)), member=True)
    for key in value._noumenon_order[::-1]:
        bs.push(value._noumenon_data[key], key)
    return bs.push(Size_t(len(value._noumenon_order))).data


def _pop_noumenon(bs: BufferStack):
    value = Noumenon()
    element = [bs.pop() for _ in range(bs.pop()*2)]
    data = dict(zip(element[0::2], element[1::2]))
    order = list(element[0::2])
    if not PARACMPT_KEYWORD_REPRESENTATION in order:
        value._noumenon_data = data
        value._noumenon_order = order
        return value
    temp = os.path.splitext(data[PARACMPT_KEYWORD_REPRESENTATION].this)
    if temp[1] == '':
        cla = eval(temp[0])
    else:
        import_module(temp[0], True)
        cla = getattr_from(temp[0], temp[1][1:])
    if cla is None:
        return value
    obj = cla()
    obj._noumenon_data = data
    obj._noumenon_order = order
    return obj


enrol(0x260975554222207, Noumenon, _push_noumenon, _pop_noumenon)
