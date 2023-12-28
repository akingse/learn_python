# Convolution卷积

# https://blog.51cto.com/u_4029519/6131859

import numpy as np
from PIL import Image
def convolve(image, kernel):    # 获取图像和卷积核的大小    
    image_rows, image_cols = image.shape    
    kernel_rows, kernel_cols = kernel.shape    # 计算输出图像的大小    
    output_rows = image_rows - kernel_rows + 1    
    output_cols = image_cols - kernel_cols + 1    # 初始化输出图像矩阵，全零的矩阵    
    output = np.zeros((output_rows, output_cols))    # 执行卷积操作    
    for row in range(output_rows):        
        for col in range(output_cols):            
            output[row, col] = np.sum(image[row:row + kernel_rows, col:col + kernel_cols] * kernel)    
            return output


# -------------------------------------------------------------

# https://github.com/LonglongaaaGo/ComputerVision
