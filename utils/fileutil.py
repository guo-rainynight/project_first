# -*- coding:utf-8 -*-
###########################################################################################
#   Description:文件操作工具类
###########################################################################################
import os
#文件路径是否存在
import traceback


def exists(filePath):
    return True if os.path.exists(filePath) else False

#是否为文件目录
def isDir(filePath):
    return True if os.path.isdir(filePath) else False

#是否为文件
def isFile(filePath):
    return True if os.path.isfile(filePath) else False

def isImage(filePath):
    #os.path.splitext(filePath)会对文件名的后缀分割，例如/data/xx.jpg分成元组('/data/xx','.jpg')
    (path,suffix) = os.path.splitext(filePath)
    return True if suffix=='.jpg' or suffix=='.png' or suffix=='.gif' or suffix=='.bmp' or suffix=='.feature' else False

#判断文件是否属于@suffix参数的类型的后缀
def isSuffix(filePath, suffix):
    (path,fileFuffix) = os.path.splitext(filePath)
    return True if fileFuffix in suffix else False

#判断文件是否目录为空
def isDirEmpty(filePath):
    return True if len(os.listdir(filePath)) == 0 else False

#获取文件创建时间时间戳
def scTime(filePath):
    return os.stat(filePath).st_ctime

#获取文件修改时间时间戳
def smTime(filePath):
    return os.stat(filePath).st_mtime

#（根据常见时间）判断文件是否过期(默认7天过期)
def expireByCtime(filePath, days=7):
    nowtime = round(time.time())
    timestamp = nowtime
    if(isFile(filePath)):
        timestamp = round(os.path.getctime(filePath))  #获取文件的创建时间
    if(isDir(filePath)):
        timestamp = round(os.path.getctime(filePath))  #获取文件夹创建时间
    return True if (nowtime-timestamp)/(60*60*24) > days else False

import logging,shutil
#强制删除文件目录（文件和文件夹都删除）
def rmfDirs(filePath):
    try:
        if not exists(filePath):
            return 0    #文件不存在
        # elif isdirempty(filePath):
        #     return -1   #文件目录为空
        else:
            # 删除一个文件夹，无论里面是否有文件或文件夹
            # (不支持文件，文件夹不存在会报错)
            shutil.rmtree(filePath)
            return 1
    except Exception as e:
        logging.error("删除文件目录{0}异常：{1}".format(filePath, e))


import time
if __name__ == "__main__":
    # ctime = time.localtime(sctime("D:/360安全浏览器下载/tmp/fraud"))
    # print(ctime)
    # print(time.strftime("%Y-%m-%d %H:%M:%S",ctime))
    # print(rmfdirs("D:/360安全浏览器下载/tmp/fraud"))

    # import datetime
    # #转换时间
    # nowTime = datetime.datetime.now()
    # print(nowTime)
    # print(nowTime.strftime("%Y-%m-%d %H:%M:%S"))
    # nowDate = datetime.date.today()
    # print(nowDate)
    # print(nowDate - (datetime.timedelta(days=3)))   #减去三天的后的日期
    # print(time.mktime(nowDate.timetuple())) #转换为时间戳

    # import sys
    # ntime, ftime = (round(time.time()*1000), sys.float_info.max)    #sys.float_info.max获取的为double类型的最大值
    # print(ntime,ftime)

    import datetime
    print(datetime.datetime.fromtimestamp(os.stat("D:/360安全浏览器下载/tmp/1").st_mtime))
    print(expireByCtime("D:/360安全浏览器下载/1",30))
    print(datetime.datetime.now().timetuple()   )