import requests
from selenium import webdriver#用于操作浏览器
from selenium.webdriver.chrome.options import Options#用于配置浏览器选项
from selenium.webdriver.chrome.service import Service#用于管理ChromeDriver
import time
from selenium.webdriver.common.by import By#导入元素定位方式枚举
import os

save_path = "C:/Users/lenovo/Desktop/html/下载文件"

# 设置浏览器并取网址（函数）
def setup():
    #创建设置浏览器对象（配置）
    q1=Options()

    #禁用沙盒模式（提高兼容性）
    q1.add_argument('--no-sandbox')

    #保持浏览器打开
    q1.add_experimental_option(name='detach',value=True)

    #用驱动创建并启动浏览器
    a1=webdriver.Chrome(service=Service('F:/chromedriver/chromedriver-win64/chromedriver-win64/chromedriver.exe'),options=q1)

    #打开ICANN首页
    a1.get('https://www.icann.org/resources/pages/com-2014-03-04-en')
    time.sleep(3)

    #定位下载链接网址
    links = [a.get_attribute('href') for a in a1.find_elements(By.XPATH, "//table//a[contains(@href, 'com-')]")]
    
    a1.quit()
    return links



#下载
def download_files(links, save_path):
    os.makedirs(save_path, exist_ok=True)
    for i, url in enumerate(links, 1):
        try:
            #从链接中提取文件名
            filename = url.split('/')[-1]
            print(f"正在下载第{i}个：{filename}")
            # 发送请求（模拟浏览器请求头，避免被服务器识别为爬虫）
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=20)

            # 保存文件
            with open(os.path.join(save_path, filename), 'wb') as f:
                f.write(response.content)

            time.sleep(2)

            print(f"第{i}个下载成功")

        except Exception as e:
            print(f"第{i}个下载失败：{str(e)}")



if __name__ == "__main__":
    links = setup()
    download_files(links, save_path)
    print("全部下载任务完成")

    