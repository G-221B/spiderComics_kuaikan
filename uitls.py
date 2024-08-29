import requests
import os
def downLoadImg(imgSrc, downLoadPath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.31',
        'Connection': 'close'
    }
    with open(downLoadPath, 'wb+') as file:
        while 1:
            try:
                imgRes = requests.get(imgSrc, headers=headers)
                file.write(imgRes.content)
                imgRes.close()
                return
            except Exception as e:
                print('下载失败，尝试重试...')

# 创建目录
def createDirectory(folder_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 获取包含关键字的scripts列表下标
def getTargetScriptIndex(scripts, keyWord):
    for index, item in enumerate(scripts):
        if keyWord in item:
            return index
    return -1

# 获取目标的script文本
def getTargetScriptText(htmlContent):
    # 提取JavaScript代码部分
    # 假设我们知道JavaScript代码在某个特定的script标签中
    pattern = r'<script\b[^>]*>([\s\S]*?)<\/script>'
    scripts = re.findall(pattern, htmlContent)
    scriptIndex = getTargetScriptIndex(scripts, 'window.__NUXT__=')
    if scriptIndex < 0:
        print('getChapterIdList_script 标签变更，无法获取window.__NUXT__')
        return ''
    scriptText = scripts[scriptIndex]  # 假设我们需要的代码在第一个script标签中

    scriptText = scriptText.replace('window.', 'var ')
    return scriptText

#  写入json文件查看调试
def wirtTextLog(logText): 
    with open('./output.json', 'w+', encoding='utf-8') as file:
        file.write(f'{logText}\n')