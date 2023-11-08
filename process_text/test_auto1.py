import os


# 指定目录路径
directory = r'D:\Alluser\learn_python\process_text'

import json

filename=r'D:\Alluser\learn_python\process_text\收费码头1.Json'
# 读取原始 JSON 文件
with open(filename, 'r') as json_file:
    data = json.load(json_file)

P3DGraphicList=[]
allGra=data["agenda"]["P3DGraphics"][0]["P3DGraphic"]
for iter in data["agenda"]["P3DGraphics"][0]["P3DGraphic"]:
    if not 'GeExtrusionInfo' in iter["IGeSolidBase"]:
        # del iter["IGeSolidBase"]
        P3DGraphicList.append(iter)
data["agenda"]["P3DGraphics"][0]["P3DGraphic"]=P3DGraphicList


# 输出为新的 JSON 文件
with open(filename, 'w') as json_file:
    json.dump(data, json_file, indent=4)                                                                                                                              


exit()
# 遍历目录下的所有文件
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        # 生成新的文件名
        if filename.find('带钢筋')!=-1:
            # new_filename=filename
            new_filename=filename.replace('带钢筋','无钢筋')
            # new_filename = 'new_' + filename
            # 重命名文件
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            # print(f'Renamed {filename} to {new_filename}')