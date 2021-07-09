import os
import sys
import json
import shutil


jsonPath = "/.../train_val_test_split/...json"                  # json文件路径
dataPath = "/.../"                                # 数据集路径
savePath = "/.../"                                # 分割后的数据集路径


if __name__ == "__main__":
    with open(jsonPath) as jsonFile:                     # 加载json文件
        jsonObject = json.load(jsonFile)
        jsonFile.close()
       
    testFilename = []
    for i in range(len(jsonObject)):                     # 读取json中名为anno_id的h5文件名
        testFilename.append(str(jsonObject[i]['anno_id']) + ".h5")
    #print(testFilename)

    data = [(x[0], x[2]) for x in os.walk(dataPath)]           # 载入完整数据集所有文件名
    
    for file in data[0][1]:                          # 复制需要的文件到指定文件夹
        if file in testFilename:
            shutil.copy(dataPath + file, savePath + file)