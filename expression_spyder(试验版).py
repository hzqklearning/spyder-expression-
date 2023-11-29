'''
变量：
表情包类型expresstion_type
要爬取的数量expression_num
网址url
放到的文件夹dir_path


伪代码：
循环体（直到数量满足）
    准备好请求头
    发出请求
    对响应头进行解析
    根据数据方式（批量/选择性）处理数据 （保存/丢弃）
'''

import requests
import os
import json
from PIL import Image,ImageTk
import io
from typing import Dict
import tkinter as tk

#把提取字符串每一行的键值 
def str_to_dict(s:str)->Dict[str,str]:
    return {line.split(':')[0].strip():line.split(':')[1].strip() for line in s.split('\n')}

#跳转到指定类型的页面 图片集
key_url='https://www.dbbqb.com/api/search/json'
key=input('请输入关键词\n')

headers_str=f'''Accept: application/json
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Client-Id: 
Connection: keep-alive
Content-Type: application/json
Cookie: Hm_lvt_7d2469592a25c577fe82de8e71a5ae60=1701095565,1701145073; Hm_lpvt_7d2469592a25c577fe82de8e71a5ae60=1701145117
Host: www.dbbqb.com
Referer: https://www.dbbqb.com/s?w={key}
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
Web-Agent: web
sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''
headers=str_to_dict(headers_str)

paras_str=f'''start: 0
w:{key}'''
paras=str_to_dict(paras_str)

resp=requests.get(key_url,headers=headers,params=paras)
resp_content=json.loads(resp.content.decode(resp.encoding))

#由粗糙的图片地址定位到原图片的地址
k=0
choice
while k<len(resp_content):
    hashid=resp_content[k]['hashId']
    photo_url='https://www.dbbqb.com/api/image/'+hashid

    photo_headers_str=f'''Accept: application/json
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    Client-Id: 
    Connection: keep-alive
    Content-Type: application/json
    Cookie: Hm_lvt_7d2469592a25c577fe82de8e71a5ae60=1701095565,1701145073; Hm_lpvt_7d2469592a25c577fe82de8e71a5ae60=1701157839
    Host: www.dbbqb.com
    Referer: https://www.dbbqb.com/detail/{hashid}.html
    Sec-Fetch-Dest: empty
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-origin
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
    Web-Agent: web
    sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
    sec-ch-ua-mobile: ?0
    sec-ch-ua-platform: "Windows"'''
    photo_headers=str_to_dict(photo_headers_str)

    photo_resp=requests.get(photo_url,headers=photo_headers)
    photo_resp_content=json.loads(photo_resp.content.decode(photo_resp.encoding))

    photo_path=photo_resp_content['path']

    #跳转到原图片地址 并得到数据保存下来
    photo_img_url='https://image.dbbqb.com/'+photo_path
    photo_img_resp=requests.get(photo_img_url)
    photo_img=photo_img_resp.content

    img_bytes=io.BytesIO(photo_img)
    image=Image.open(img_bytes)

    root=tk.Tk()
    root.title("图片确认")

    image_tk=ImageTk.PhotoImage(image)
    image_component=tk.Label(root,image=image_tk)
    image_component.pack()

    verify_input=tk.StringVar()
    entry=tk.Entry(root,textvariable=verify_input)
    entry.pack()


    def process_input():
        global choice
        choice = verify_input.get()
        if choice == '1':
            image.save('./saved_image.jpg')
            print("图像已保存")
        elif choice == '0':
            print("图像未保存")
        else:
            print("无效的输入")


        # 关闭窗口
        root.destroy()

    # 创建按钮绑定处理函数
    button = tk.Button(root, text="确定", command=process_input)
    button.pack()


    root.mainloop()
    if choice=='q':
        break
# image.show()
# image.save('./test1.jpg')

