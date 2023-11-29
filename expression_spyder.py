import requests #请求网页
from typing import Dict,Tuple #类型提示
from PIL import Image,ImageTk #图片显示和保存
import io #配合PIL使用
import tkinter as tk #以便图片显示和交互式保存
import os  #创建图片保存的文件夹
import re  #对图片名字进行清洗

def str_to_dict(s:str)->Dict:
    return {line.split(':',1)[0].strip():line.split(':',1)[1].strip() for line in s.split('\n') if line!=''}


#############################################################################################################
#准备发送请求的参数   主网址是https://www.doutub.com/
key=input('准备从https://www.doutub.com/ 爬取表情包\n请输入关键词:\n')
mode=input('请输入模式：1表示批量模式，2表示交互模式\n')
if mode=='1':
     images_num=int(input('请输入要爬取的数量\n'))
print('开始爬取............')

dir_path=f'./表情包/{key}'
if not os.path.isdir(dir_path):
    os.makedirs(dir_path)

cur_page=1
page_size=100
search_headers_str='''Accept:application/json, text/plain, */*
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Origin:https://www.doutub.com
Referer:https://www.doutub.com/
Sec-Ch-Ua:"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
Sec-Ch-Ua-Mobile:?0
Sec-Ch-Ua-Platform:"Windows"
Sec-Fetch-Dest:empty
Sec-Fetch-Mode:cors
Sec-Fetch-Site:same-site
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
'''
search_params_str=f'''keyword: {key}
curPage: {cur_page}
pageSize: {page_size}
'''
search_url='https://api.doutub.com/api/bq/search'
search_headers=str_to_dict(search_headers_str)
search_params=str_to_dict(search_params_str)

search_resp=requests.get(url=search_url,headers=search_headers,params=search_params)

#提取信息
search_resp_content=search_resp.content
search_resp_dict=search_resp.json()
search_resp_data=search_resp_dict['data']
count=search_resp_data['count'] #图片集的数量
imgs_name=[img['imgName'] for img in search_resp_data['rows']]
imgs_path=[img['path'] for img in search_resp_data['rows']] #网址

##############################################################################################################
img_headers_str='''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Cache-Control: max-age=0
Connection: keep-alive
Cookie: Hm_lvt_0e35b200a6045f9dd8f8887cd4626da2=1701179179; Hm_lpvt_0e35b200a6045f9dd8f8887cd4626da2=1701179762
Host: qn.doutub.com
If-Modified-Since: Wed, 24 Jul 2019 14:27:31 GMT
If-None-Match: "FoaI7uga9nS0wUQm0LCqu3fxtNHH"
Referer: https://www.doutub.com/
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-site
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''
img_headers=str_to_dict(img_headers_str)


def getImage(curr:int)->Tuple[str,str,Image.Image]:
    img_name=re.sub('[\[\?\]{},.\\\\/;\<\>\+\=\(\)]','',imgs_name[curr])
    img_url=imgs_path[curr]
    img_resp=requests.get(url=img_url,headers=img_headers)
    img_type=img_resp.headers['Content-Type'].split('/')[1].strip() #解析响应对象的类型 very important skill !!!
    img_bytes=io.BytesIO(img_resp.content)
    image=Image.open(img_bytes)
    return img_name,img_type,image

def keyboardEventResp(event:tk.Event):
        global curr,img_name,img_type,image
        key=event.keysym
        if key=='s':
            image.save(dir_path+f'/{img_name}{curr}.{img_type}')
        elif key=='q':
            root.destroy()
            return

        curr+=1
        if curr>=count:
             root.destroy()
             print('没有更多图片')
             return
        try:
            img_name,img_type,image=getImage(curr)
            tk_image=ImageTk.PhotoImage(image)
            tk_image_widget.config(image=tk_image)
            tk_image_widget.image=tk_image
        except:
            print(f'读取该图片失败 {imgs_path[curr]}')

if mode=='1':
    curr=0;
    while curr<images_num and curr<count:
        try:
            img_name,img_type,image=getImage(curr)
            image.save(dir_path+f'/{img_name}{curr}.{img_type}')
            print(f'爬取成功{img_name}{curr}.{img_type}')
        except:
            print(f'读取该图片失败 {imgs_path[curr]}')
        curr+=1
else:
    curr=0
    root=tk.Tk()
    root.title('表情包')
    tk_image_widget=tk.Label(root)
    tk_image_widget.pack()

    root.bind('<KeyPress-s>',keyboardEventResp)
    root.bind('<KeyPress-q>',keyboardEventResp)
    # root.bind('<Enter>',keyboardEventResp) #鼠标移入控件事件. 注意: 这个事件不是 Enter 键按下事件, Enter 按下事件是 <Return>.
    root.bind('<Return>',keyboardEventResp)

    img_name,img_type,image=getImage(curr)
    tk_image=ImageTk.PhotoImage(image)
    tk_image_widget.config(image=tk_image)
    tk_image_widget.image=tk_image #tkinter有一个垃圾回收机制，它会自动删除没有被引用的对象，包括图片对象。如果不保存对图片对象的引用，那么当函数结束后，图片对象就会被回收，导致Label组件显示空白。

    root.mainloop()


