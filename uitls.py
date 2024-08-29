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

def createDirectory(folder_name):
    current_directory = os.getcwd()
    folder_path = os.path.join(current_directory, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)