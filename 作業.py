#!/usr/bin/env python
# -*- coding=utf-8 -*-
from xml.etree import ElementTree
import sys
import xml.etree.ElementTree as ET
import urllib.request as httplib
import mylibs
import matplotlib.pyplot as plt    # 匯入 matplotlib 程式庫
#  SSL  處理，  https    SSSSSS 就需要加上以下2行
import ssl
ssl._create_default_https_context = ssl._create_unverified_context    # 因.urlopen發生問題，將ssl憑證排除
if sys.platform.startswith("linux"):  # could be "linux", "linux2", "linux3", ...
    print("linux")  # linux
elif sys.platform == "darwin":  # MAC OS X
    print("MAC OS")
    plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
    # //注意這裡用的不是'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
elif sys.platform == "win32":  # Windows (either 32-bit or 64-bit)
    print("Windows")
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）

######### 由網路下載 JSON 的 字串

url="https://apiservice.mol.gov.tw/OdService/download/A17000000J-020044-O95"
contents= mylibs.url_Get(url)
mylibs.file_write('新制勞工退休基金歷年最近月份收益率.xml',contents)


# 加载XML文件
root = ElementTree.fromstring(contents)
row= root.findall("row")

# 取得Tags
elemList = []
for elem in root.iter():
    elemList.append(elem.tag)

elemList = list(set(elemList))
print(elemList)

# 取得所有資料
yearMonthList=[]
YieldlList=[]
n=0
while n<len(row):
    # XML 解析
    yearMonth= row[n].findall("年月別")
    Yield= row[n].findall("最近月份收益率")
    date= row[n].findall("公告日期")


    str1="年月別:"         +yearMonth[0].text +\
         " ,最近月份收益率:"  +Yield[0].text+\
         " ,公告日期:"       +date[0].text


    yearMonthList.insert(0,yearMonth[0].text)
    YieldlList.insert(0,float(Yield[0].text))   # 字串轉浮點數
    n=n+1

print(YieldlList)



allMonth=len(yearMonthList)
print("統計月份:",allMonth,"個月")
average=sum(YieldlList) / float(allMonth)
average=round(average, 2)
print("平均收益率 : ",average,"%")



plt.plot(yearMonthList, YieldlList,"y-")
plt.plot(yearMonthList, YieldlList,"k^",label="最近月份收益率")
plt.axhline(average, color= 'r',label="平均收益率")
plt.xticks(rotation=-90, fontsize=10)
plt.ylabel('收益率(%)')
plt.xlabel('年月別')
plt.title("新制勞工退休基金歷年最近月份收益率")
plt.legend()
plt.show()
