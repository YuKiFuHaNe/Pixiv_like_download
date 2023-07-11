from lxml import etree
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import time
from datetime import datetime
cookie = "you cookies"
cookie = "first_visit_datetime_pc=2023-07-10+09%3A25%3A18; p_ab_id=9; p_ab_id_2=5; p_ab_d_id=1538593596; yuid_b=EmUYkEA; __cf_bm=uZeh.IFzXsDxhnPZ.1.zt5qWVHIwJFH7zAcIvzC0xVI-1688948720-0-AaNvqwmPHOl6ayuZXvbRdCn2VhlzXinbvQbJbp2QlGmGKR0RoYq4j6aDhfo0SUA8Js3BLutdbub40QBNloSvJHBc7FkVNcKdxXAu4FrUfyPYhye3XHZ/4WFGfJV7NHk9rw==; PHPSESSID=38390168_j6n0bPJtFJDV8xSKWmIBVBs2ZIHqIUzb; device_token=c9afeecabc7e46a83bf04136e0cc3007; c_type=23; privacy_policy_agreement=0; privacy_policy_notification=0; a_type=0; b_type=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; login_ever=yes"
pixiv_id = re.search(r"PHPSESSID=(?P<pixivid>\d+)_",cookie).group("pixivid")
print(pixiv_id)
base_url = "https://www.pixiv.net/"
# like_url = "https://www.pixiv.net/users/{}/bookmarks/artworks".format(pixiv_id)
page = 624      # 开始 页*48 1\48\96...
sleep_time = 1  # 每张图片下载完再次请求时间
step = 48       # page页面插画数量 默认48

# choose = input("是否使用代理(Y|y):")
# if choose == 'Y' or 'y':
#     proxies = {
#         'http': 'http://localhost:7890',
#         'https': 'http://localhost:7890'
#     }
# else:
#     proxies = None
headers = {
    "Cookie":cookie,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

}

def get_data(page)->dict:
    like_url = "https://www.pixiv.net/ajax/user/{}/illusts/bookmarks?tag=&offset={}&limit=48&rest=show&lang=zh".format(pixiv_id,page)
    # https://www.pixiv.net/ajax/user/id/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh
    print(pixiv_id,page)
    resp = requests.get(like_url, headers=headers)
    resp.encoding = 'utf-8'
    data = resp.json()
    # print(resp.json())
    resp.close()
    return data


def get_picture_url(*args:str)->list:
    '''
    获取（合成）图片url
    :param args: picture_url,picture_id,title,pagecount,date
    :return:https://i.pximg.net/img-original/img/2023/01/26/03/45/10/104815394_p0.png
    :argument:
        picture_url (https://i.pximg.net/c/250x250_80_a2/custom-thumb/img/2022/06/14/00/00/40/99037207_p0_custom1200.jpg)

    '''
    picture_url,picture_id, title, pagecount, date = args
    title = title.replace("|","").replace("/","").replace("?","").replace("*","").replace(":","").replace("<","").replace(">","")
    picture_id = int(picture_id)
    pagecount = int(pagecount)
    print(picture_url,picture_id,title,pagecount,date)
    extension_name = picture_url.split('.')[-1]
    url = []
    for i in range(pagecount):
        url.append('https://i.pximg.net/img-original/img/{}/{:0>2d}/{:0>2d}/{:0>2d}/{:0>2d}/{:0>2d}/{:0>2d}_p{}.{}'.format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second,
            picture_id,
            i,
            extension_name
        ))
        print(url)
        headers['referer'] = 'https://www.pixiv.net/'
        # headers['referer']= f'https://pixivic.com/illusts/{picture_id}?VNK=418eebdd'
        url_id = f'https://www.pixiv.net/ajax/illust/{picture_id}/pages?lang=zh'
        # res = requests.get(url_id, headers=headers)
        res = requests.get(url[i],headers=headers)
        # print(res.text)
        if res.text.find("404 Not Found") != -1:
            '''
            <!DOCTYPE html>
            <html>
                <h1>404 Not Found</h1>
            </html>
            '''
            if extension_name == "jpg":
                extension_name = "png"
            else:
                extension_name = "jpg"
            res = requests.get('https://i.pximg.net/img-original/img/{}/{:0>2d}/{:0>2d}/{:0>2d}/{:0>2d}/{:0>2d}/{:0>2d}_p{}.{}'.format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second,
            picture_id,
            i,
            extension_name),headers=headers)
            # print(res.text)
        f = open("./download/{}_p{}_pictureID{}.jpg".format(title, i, picture_id), mode="wb")
        f.write(res.content)
        f.close()
        res.close()
    return url



while(1):
    data = get_data(page=page)
    error = data['error']
    body = data['body']['works']
    lenght = len(body)
    # print(body)
    # 判断该页是否请求成功与是否存在图片数据
    if error == False and lenght > 0:
        # 遍历该页的所以收藏图片
            for i in range(lenght):
                time.sleep(3)
                try:
                    picture_data = body[i]
                    picture_url = picture_data['url']
                    picture_id = picture_data['id']
                    title = picture_data['title']
                    pagecount = picture_data['pageCount']
                    createdate = picture_data['createDate']
                    update = picture_data['updateDate'] # updateDate '2023-01-26T03:45:10+09:00'
                    date = datetime.fromisoformat(update)
                    picture_list = get_picture_url(picture_url,picture_id,title,pagecount,date)
                    print(picture_list)
                    with open('test.txt',mode="a+") as f:
                        for i in picture_list:
                            f.write(i+"\n")
                except:
                    continue

    if page == 1:
        page=48
    else:
        page += 48
    print(error,body)

