import 网页表格.request请求 as req
import 提取数据 as ext
import sys  

def main():
    #发送请求
    try:
        req.send_request()
    except Exception as e:
        print(f"发送请求失败：{str(e)}")
        sys.exit(1)  
    
    #提取数据
    try:
        ext.extract_data()
    except Exception as e:
        print(f"提取数据失败：{str(e)}")
        sys.exit(1)
    

if __name__ == "__main__":
    main()


