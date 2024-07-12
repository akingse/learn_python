import os
import shutil

def copy_folder(source_folder, destination_folder):
    if not os.path.exists(source_folder):
        print(f"源文件夹 '{source_folder}' 不存在")
        return
    os.makedirs(destination_folder, exist_ok=True)
    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(destination_folder, item)
        if os.path.isdir(source_item):
            copy_folder(source_item, destination_item)
        else:
            shutil.copy2(source_item, destination_item)
            print(f"已复制文件 '{source_item}' 到 '{destination_item}'")

source_folder = "/path/to/source/folder"
destination_folder = "/path/to/destination/folder"

copy_folder(source_folder, destination_folder)