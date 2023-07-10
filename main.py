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
url = "https://www.pixiv.net/"
# like_url = "https://www.pixiv.net/users/{}/bookmarks/artworks".format(pixiv_id)
page = 1
step = 48

# choose = input("是否使用代理(Y|y):")
# if choose == 'Y' or 'y':
#     proxies = {
#         "https":"https://218.60.8.83:3129"
#     }
# else:
#     proxies = None
headers = {
    "Cookie":cookie,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "X-User-Id":pixiv_id

}

def get_data(page)->dict:
    like_url = "https://www.pixiv.net/ajax/user/{}/illusts/bookmarks?tag=&offset={}&limit=48&rest=show&lang=zh".format(pixiv_id,page)
    # https://www.pixiv.net/ajax/user/id/illusts/bookmarks?tag=&offset=0&limit=48&rest=show&lang=zh
    print(pixiv_id,page)
    resp = requests.get(like_url, headers=headers)
    resp.encoding = 'utf-8'
    data = resp.json()
    # print(resp.json())
    time.sleep(3)
    resp.close()
    return data


def get_picture_url(*args):
    '''
    获取（合成）图片url
    :param args: picture_id,title,pagecount,date
    :return:
    '''
    picture_url,picture_id, title, pagecount, date = args
    print(picture_url,picture_id,title,pagecount,date)
    pass

while (1):
    data = get_data(page=page)
    error = data['error']
    body = data['body']['works']
    lenght = len(body)
    print(body)
    # 判断该页是否请求成功与是否存在图片数据
    if error == False and lenght > 0:
        # 便利该页的所以收藏图片
        for i in range(lenght):
            picture_data = body[i]
            picture_url = body['url']
            picture_id = picture_data['id']
            title = picture_data['title']
            pagecount = picture_data['pageCount']
            createdate = picture_data['createDate']
            update = picture_data['updateDate'] # updateDate '2023-01-26T03:45:10+09:00'
            # https://i.pximg.net/img-original/img/2023/01/26/03/45/10/104815394_p0.png
            date = datetime.fromisoformat(update)
            get_picture_url(picture_url,picture_id,title,pagecount,date)
    break
    if page == 1:
        page=48
    else:
        page += 48
    print(error,body)

