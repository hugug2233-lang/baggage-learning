import pandas as pd
from bs4 import BeautifulSoup
import os   
import requests


data_path = "C:/Users/lenovo/Desktop/html/result.txt"  
API_URL = "https://www.icann.org"
download_path = "C:/Users/lenovo/Desktop/html/下载文件"

# 新增：添加浏览器请求头（解决服务器识别问题）
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

# 代理    -------------不用代理需要注释----------------
# PROXY_URL = "http://127.0.0.1:7890"  
# proxies = {
#     "http": PROXY_URL,   # HTTP请求走代理
#     "https": PROXY_URL   # HTTPS请求走代理
# }

def extract_data():
    # 提取数据
    try:   
        with open(data_path, 'r', encoding='utf-8') as f:
            full_content = BeautifulSoup(f.read(), 'html.parser')

        table = full_content.find('table', class_='convey sticky-enabled')
        
    # 报错
    except FileNotFoundError:
        print('data_path路径出错')
        return
    
    except Exception as e:
        print(f"出错：{str(e)}")
        return

    empty_data = []
    rows = table.find('tbody').find_all('tr')

    failed_items=[]

    # 提取数据
    for idx, row in enumerate(rows, 1):
        
        #取下载地址
        cols = row.find_all('td')
        a_tag=cols[4].find('a')
        if a_tag and 'href' in a_tag.attrs:
            download_url=API_URL+a_tag['href'].strip()
            file_name = download_url.split('/')[-1]
            save_path = os.path.join(download_path,  file_name)
            os.makedirs(download_path, exist_ok=True)

            #请求下载
            try:
                # 下面二选一
                resp = requests.get(download_url, headers=headers, timeout=30, stream=True)
                # resp = requests.get(download_url, headers=headers, timeout=30, stream=True, proxies=proxies)  

                resp.raise_for_status()# 检查请求是否成功
                with open(save_path, 'wb') as f:
                    f.write(resp.content)

            except Exception as e:
                # 展示出错链接
                print(f"第{idx}行下载失败: {str(e)}")
                print(f"下载链接: {download_url}")
                failed_items.append({'idx': idx, 'url': download_url, 'save_path': save_path})
  
        else:
            download_url=''
            print(f"第{idx}行下载链接失效")

        #整理  text只要文本  strip去掉空格
        unit_data = {
            'Registry': cols[0].text.strip(),
            'Month': cols[1].text.strip(),
            'Year': cols[2].text.strip(),
            'Report': cols[3].text.strip(),
            'File': cols[4].text.strip(),
            'download':download_url
        }

        empty_data.append(unit_data)



    print("第一次下载完成")


    #集中重试所有失败的项
    if failed_items:
        print(f"\n开始重试{len(failed_items)}个失败项")
        for item in failed_items:
            idx, url, save_path = item['idx'], item['url'], item['save_path']
            # 单个文件最多重试3次
            for retry in range(3):
                try:
                    resp = requests.get(url, headers=headers, timeout=30, stream=True)
                    # resp = requests.get(url, headers=headers, timeout=30, stream=True, proxies=proxies)  
                    resp.raise_for_status()
                    with open(save_path, 'wb') as f:
                        f.write(resp.content)
                    break  


                except Exception as e:
                    if retry == 2:  # 最后一次重试失败
                        print(f"第{idx}行重试3次仍失败：{url}")
    


    else:
        print("\n第一轮下载全部成功，无需重试")

    print("下载完成")
    # 转为Excel
    df = pd.DataFrame(empty_data)

    # 保存为csv
    df.to_csv('C:/Users/lenovo/Desktop/html/分数数据.csv', index=False, encoding='utf-8-sig')

    # 11. 保存为Excel文件
    df.to_excel('C:/Users/lenovo/Desktop/html/分数数据.xlsx', index=False, engine='openpyxl')

    print('保存完成')

if __name__ == "__main__":
    extract_data()


