# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: YouQi
# Date: 2021/05/06
from .serialization import *
from .runtime import *
path = sys.path[-1]
if len(sys.path[-1]) > 1 and sys.path[-1][0] == '?':
    version = Size_t(sys.path[-1][1:])
    sys.path.pop()
    isService = True
else:
    version = UnifiedFunction('BPParametricComponent', 'get_version')()
    isService = False
print(version)
versionInformation = 'Internal debug version.'
from .vDebug import *

# if version > Size_t(18446497929134014464):
#     raise RuntimeError('current pyp3d version is outdated, please get update!')
# if version == Size_t(0):
#     from .vDebug import *
#     versionInformation = 'Internal debug version.'
# elif version == Size_t(18446497929134014464):
#     from .vDebug import *
#     versionInformation = 'Release in 2022.03!'
# elif version == Size_t(18446497929133948928):
#     from .vDebug import *
#     versionInformation = 'Release in 2022.03!'
# elif version == Size_t(18446497929133883392):
#     from .vDebug import *
#     versionInformation = 'Release in 2021.12!'
# elif version == Size_t(18446497929133817856):
#     from .vDebug import *
#     versionInformation = 'Release in 2021.09!'
# else:
#     raise RuntimeError(
#         'there is no matched pyp3d version, please install the pyp3d that correspond BIMBase!')

if isService:
    start_runtime_service()
print('[PYP3D] : Version {0} loaded.'.format(version))
print('[PYP3D] : {0}'.format(versionInformation))
