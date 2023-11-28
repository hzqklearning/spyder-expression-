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
from PIL import Image
import io


# main_url='https://www.dbbqb.com/'
# key=input('请输入关键词\n')
key_url='https://www.dbbqb.com/api/search/json'

headers_str='''Accept: application/json
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Client-Id: 
Connection: keep-alive
Content-Type: application/json
Cookie: Hm_lvt_7d2469592a25c577fe82de8e71a5ae60=1701095565,1701145073; Hm_lpvt_7d2469592a25c577fe82de8e71a5ae60=1701145117
Host: www.dbbqb.com
Referer: https://www.dbbqb.com/s?w=%E7%86%8A%E7%8C%AB
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
Web-Agent: web
sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''
headers={line.split(':')[0].strip():line.split(':')[1].strip() for line in headers_str.split('\n')}

paras_str='''start: 0
w: %E7%86%8A%E7%8C%AB'''
paras={line.split(':')[0].strip():line.split(':')[1].strip() for line in paras_str.split('\n')}

# print(headers)
resp=requests.get(key_url,headers=headers,params=paras)
resp_content=json.loads(resp.content.decode(resp.encoding))

hashid=resp_content[0]['hashId']
photo_url='https://www.dbbqb.com/api/image/'+hashid

photo_headers_str='''Accept: application/json
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Client-Id: 
Connection: keep-alive
Content-Type: application/json
Cookie: Hm_lvt_7d2469592a25c577fe82de8e71a5ae60=1701095565,1701145073; Hm_lpvt_7d2469592a25c577fe82de8e71a5ae60=1701157839
Host: www.dbbqb.com
Referer: https://www.dbbqb.com/detail/roXWl.html
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0
Web-Agent: web
sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''
photo_headers={line.split(':')[0].strip():line.split(':')[1].strip() for line in photo_headers_str.split('\n')}
photo_resp=requests.get(photo_url,headers=photo_headers)
photo_resp_content=json.loads(photo_resp.content.decode(photo_resp.encoding))

photo_path=photo_resp_content['path']
photo_img_url='https://image.dbbqb.com/'+photo_path
photo_img_resp=requests.get(photo_img_url,photo_headers)
photo_img=photo_img_resp.content

img_bytes=io.BytesIO(photo_img)
image=Image.open(img_bytes)
image.save('./test.jpg')

# print(key_url.encode())
# print(t)
