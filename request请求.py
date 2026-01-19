import requests
import json
from urllib.parse import quote#处理特殊字符
from urllib.parse import urlencode#分类key
import os

API_URL = "https://www.icann.org/resources/pages/com-2014-03-04-en"


#Fiddler代理地址
PROXY = {
    "http": "http://127.0.0.1:8888",
    "https": "http://127.0.0.1:8888"
}


#协议头
REQUEST_HEADERS = {
    "Host": "www.icann.org",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": '"Chromium";v="9", "Not?A_Brand";v="8"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.8151 SLBChan/11 SLBVPV/64-bit",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie":
    "_new_icann_session=569cbefb652a6a6264bfef459fbbc068; cf_clearance=BjFCnbOO5KxzDMxqdpCJfYEQGWGs5FqtusCAIsPaT.o-1767940591-1.2.1.1-b6fzzcmwYccONqkIODRcJhorJ8sBuWYFggM4Kt0njD2WeAinGK5Uz.bGtogy_8Qcv8V.8xexDPAfg3IvhVG64AdLqCpG98aj3Tvvqmb3YbLoTx3O1f.LYhoOcUxqMmik5dJY.uJm7uurizifEwti7_oZqz9xkVbURxXv37G1SSpeZWSwJXIonUCiLS5EmGziX9wTV4V.jNvU.4n59G2E9Lc.kXxpD2fql8DdZa7WwP0; OptanonAlertBoxClosed=2026-01-09T06:36:38.595Z; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+09+2026+14%3A36%3A38+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202411.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=12644124-c1e4-4bc8-8061-74ded4ec0144&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0&intType=3; __cf_bm=7TtqpKzAwssvcLWVFIduoojmuD0o4Be3zYq8gUQiOBc-1767940605.353083-1.0.1.1-Pr0rvYKX4oizowf368Q.OCjK8cLIMrgbdIvIAubrfGFWuWBtMwSQdNNugv2aVqpEk7_Tinh2AnoaaUpJiuJg8SeqTjCxrVjZe09XV8y09Gp.ZjmxEkwhaKVlDMTfSghk"
}




def send_request():
    try:
        #屏蔽SSL警告
        requests.packages.urllib3.disable_warnings()
            
        #创建session，通过Fiddler代理
        session = requests.Session()
        session.proxies.update(PROXY) 
        session.headers.update(REQUEST_HEADERS)

        # 发送post请求
        response = session.get(
            url=API_URL,
            # json=REQUEST_BODY,
            timeout=10,
            verify=False,  # 信任Fiddler的证书
            allow_redirects=False
            )
        
        # print("Fiddler已发送请求！！！")

        # 解析响应
        print(f"状态码：{response.status_code}")
        resp_data = response.text

        # 保存数据

        os.makedirs("C:/Users/lenovo/Desktop/html", exist_ok=True)
        
        with open(r'C:/Users/lenovo/Desktop/html/result.txt', 'w', encoding='utf-8') as f:
            f.write(resp_data)
        print("保存成功！！！")
       
    
            
    except Exception as e:
        print(f"请求失败：{str(e)}")

if __name__ == "__main__":
    send_request()
