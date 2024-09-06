import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
mypath=r'C:\Users\Aking\source\repos\learn_python'
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402

file=r'C:\Users\Aking\source\repos\bimbase\Bin\Release\OutputGraphicsToJson\\'
# js=JsonRead(file+'Graphics2.Json')


js=JsonRead(r'D:\Commun\WXWork\1688853868786339\Cache\File\2024-08\3交通安全设施—收费码头2(1).Json')
js.write_python_code()


