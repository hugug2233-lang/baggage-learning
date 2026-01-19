from selenium import webdriver#用于操作浏览器
from selenium.webdriver.chrome.options import Options#用于配置浏览器选项
from selenium.webdriver.chrome.service import Service#用于管理ChromeDriver
import time
#导入元素定位方式枚举
from selenium.webdriver.common.by import By  
import os



# 设置浏览器并启动（函数）
def setup():
    #创建设置浏览器对象（配置）
    q1=Options()

    #禁用沙盒模式（提高兼容性）
    q1.add_argument('--no-sandbox')

    #保持浏览器打开
    q1.add_experimental_option(name='detach',value=True)

    #配置下载相关偏好设置
    prefs = {
        "download.default_directory": "C:/Users/lenovo/Desktop/html/下载文件",  #下载路径
        "download.prompt_for_download": False,  #关闭下载弹窗
        "plugins.always_open_pdf_externally": True  #PDF文件直接下载，不在浏览器内打开
    }

    #将下载配置添加到浏览器选项中
    q1.add_experimental_option("prefs", prefs)

    #用驱动创建并启动浏览器
    a1=webdriver.Chrome(service=Service('F:/chromedriver/chromedriver-win64/chromedriver-win64/chromedriver.exe'),options=q1)

    return a1

#调用函数，启动浏览器
a1=setup()
#打开ICANN首页
a1.get('https://www.icann.org/resources/pages/com-2014-03-04-en')

time.sleep(3)

#定位页面中表格里的所有下载链接
download_links = a1.find_elements(By.XPATH, "//table//a[contains(@href, 'com-')]")


os.makedirs("C:/Users/lenovo/Desktop/html/下载文件", exist_ok=True)

# 3.6 遍历所有找到的链接，逐个下载
# enumerate(download_links, 1)：给链接加序号，从1开始（方便看第几个）
for i, link in enumerate(download_links, 1):
    try:  # 捕获单个链接下载失败的异常，避免一个失败导致全部停止
        # 获取链接的文字内容（比如文档名称）
        link_text = link.text
        # 打印当前下载进度
        print(f"正在下载第{i}个：{link_text}")
        # 点击链接，触发下载
        link.click()
        # 等待1秒（避免短时间点击过多链接，导致浏览器卡顿或请求被拦截）
        time.sleep(3)  
    except Exception as e:  # 捕获任何下载异常
        # 打印失败信息，方便排查问题
        print(f"第{i}个下载失败：{e}")

# 3.7 所有链接处理完成后，提示下载完成
print("批量下载完成")

# 关闭整个浏览器
a1.quit()



