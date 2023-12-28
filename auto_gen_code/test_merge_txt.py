import os

# 指定要读取的文本文档所在的文件夹路径
folder_path = "D:/Browser/1-49-bib"

# 指定要写入合并内容的文档路径
output_file = "D:/Browser/output.bib"


# 获取文件夹中的所有文本文档，并按文件名排序
file_list = sorted([filename for filename in os.listdir(folder_path) if filename.endswith(".bib")])

# 遍历排序后的文件列表
for filename in file_list:
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        # 将读取到的内容写入合并文档中
        with open(output_file, "a", encoding="utf-8") as output:
            output.write(content)
            output.write("\n")  # 可选：在每个文件的内容之间添加换行符

print("合并完成！")
# 遍历文件夹中的所有文本文档
# for filename in os.listdir(folder_path):
#     if filename.endswith(".bib"):
#         file_path = os.path.join(folder_path, filename)
#         with open(file_path, "r", encoding="utf-8") as file:
#             content = file.read()
#             # 将读取到的内容写入合并文档中
#             with open(output_file, "a", encoding="utf-8") as output:
#                 output.write(content)
#                 output.write("\n")  # 可选：在每个文件的内容之间添加换行符
