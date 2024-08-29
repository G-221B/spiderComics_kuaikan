from bs4 import BeautifulSoup
import requests
import re
import execjs
import numpy as np
from PIL import Image
from uitls import downLoadImg, createDirectory, getTargetScriptText


def downloadChapter(chapterId, comicsName):
    isMobi = True
    thredUrl = f'https://www.kuaikanmanhua.com/webs/comic-next/{chapterId}'
    if isMobi: 
       thredUrl = f'https://m.kuaikanmanhua.com/mobile/comics/{chapterId}/'
    
    res = requests.get(thredUrl)


    scriptText = getTargetScriptText(res.text)

    # 使用execjs执行JavaScript代码
    context = execjs.compile(scriptText)
    variable_value = context.eval('__NUXT__')

    comicInfo = variable_value['data'][0]['comicInfo']
    title = comicInfo['title']
    comicImgList = variable_value['data'][0]['res']['data']['comic_info']['comic_images']

    i = 1
    imgFileNameList = []
    createDirectory(f'./漫画爬虫资源/{title}')
    # 遍历字典中的所有键
    for item in comicImgList:
        print(item['url'])
        downLoadImg(item['url'], f'./漫画爬虫资源/{title}/{i}.png')
        imgFileNameList.append(f'./漫画爬虫资源/{title}/{i}.png')
        i +=1
    mergeImg(imgFileNameList, comicsName, title)

def mergeImg(imgFileNameList, foldName, title):
    img_array_list = []  # 初始化一个列表来保存所有图片的数组

    for v in imgFileNameList:
        img = Image.open(v)  # 打开图片
        if img.mode != 'RGB':  # 检查图片是否是RGB模式
            img = img.convert('RGB')  # 如果不是，转换为RGB模式
        img_array = np.array(img)  # 转化为np array对象
        img_array_list.append(img_array)  # 将图片数组添加到列表中

    # 使用np.concatenate将所有图片数组合并成一个长图
    img_array = np.concatenate(img_array_list, axis=0)  # 纵向拼接

    createDirectory(f'./漫画爬虫资源/{foldName}_长图合集')
    img = Image.fromarray(img_array)
    img.save(f'./漫画爬虫资源/{foldName}_长图合集/{title}.png')

def getChapterIdList():
    
    # thredUrl = input('输入漫画主页url：')
    # thredUrl = f'https://www.kuaikanmanhua.com/web/topic/16222/'
    thredUrl = f'https://m.kuaikanmanhua.com/mobile/16222/list/'
    res = requests.get(thredUrl)


    scriptText = getTargetScriptText(res.text)

    # 使用execjs执行JavaScript代码
    context = execjs.compile(scriptText)
    variable_value = context.eval('__NUXT__')

    comics = variable_value['data'][0]['comics']
    comicsName = variable_value['data'][0]['topicInfo']['title']

    createDirectory('./漫画爬虫资源')
    count = 1
    for item in comics:
        downloadChapter(item['id'], comicsName)
        print('下载完成：', item['title'])
        if count == 1:
            return

if __name__ == '__main__':
    getChapterIdList()