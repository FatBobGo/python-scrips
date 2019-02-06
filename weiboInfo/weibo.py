# -*- coding:utf-8 -*-
import requests
from time import sleep
import sys, io, datetime

'''
新浪微博（移动端m.weibo.cn）博文抓取及词云显示
'''


def get_user_info(uid):
    '''
    获取博主的主要信息，参数uid为博主的id
    使用API获取微博用户的json数据，然后把关键字段提取出来
    可以使用containerid获得微博全文
    input : uid
    output: data structure - userinfo 
    '''

    # setup page code for VS Code - 中文支持 (windows + VS Code)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

    result = requests.get('https://m.weibo.cn/api/container/getIndex?type=uid&value={}'.format(uid))
    json_data = result.json()
    json_user_info = json_data['data']
    #print(json_user_info)

    userinfo = {
        'name':             json_user_info['userInfo']['screen_name'],
        'description':      json_user_info['userInfo']['description'],
        'follow_count':     json_user_info['userInfo']['follow_count'],
        'followers_count':  json_user_info['userInfo']['followers_count'],
        'profile_image_url':json_user_info['userInfo']['profile_image_url'],
        'verified_reason':  json_user_info['userInfo']['verified_reason'],
        'containerid':      json_user_info['tabsInfo']['tabs'][1]['containerid']
    }

    if json_user_info['userInfo']['gender'] == 'm':
        gender = u'男'
    elif json_user_info['userInfo']['gender'] == 'f':
        gender = u'女'
    else:
        gender = u'未知'

    userinfo['gender'] = gender

    return userinfo


def get_all_post(uid, containerid):
    '''
    获取博主的所有微博
    uid:        博主的微博id
    containerid:从函数get_use_info获得
    '''

    # setup page code for VS Code - 中文支持 (windows + VS Code)
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
    # start from page 1
    page = 0
    posts = []

    # 支持3000页抓取
    while page <= 3000:
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}&page={}'.format(uid, containerid, page)
        result = requests.get(url)

        json_data = result.json()
        cards = json_data['data']['cards']
        if not cards:
            break
        
        for card in cards:
            if card['card_type'] == 9:
                post = card['mblog']['text']
                posts.append(post)
        
        # 延时防止ip被加入黑名单
        sleep(3)
        page += 1
        print("抓取第{page}页，目前总共抓取了 {count} 条微博".format(page=page, count=len(posts)))

    return posts


def display_world(posts):
    
    # 数据可视化 - 显示关键字的比重
    import jieba.analyse
    from html2text import html2text

    content = '\n'.join([html2text(i) for i in posts])

    # 提取1000个关键词及其比重
    result = jieba.analyse.textrank(content, topK=1000, withWeight=True)

    # 生成关键词比重字典
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]

    # 生成词云图
    from PIL import Image, ImageSequence
    import numpy as np
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, ImageColorGenerator

    # WordCloud 不支持中文，所有需要加载中文字体
    wc = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',
        background_color='white', max_words=300)

    wc.generate_from_frequencies(keywords)

    # display picture
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

    # save the image to a file
    wc.to_file('test-{}.png'.format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")))


# ------------------------------------------------------
# Program Main Logic
# ------------------------------------------------------

# 古力娜扎
#print(get_user_info('1350995007'))
#posts = get_all_post('1350995007', '1076031350995007')

# 木村拓哉
# print(get_user_info('6883966016'))
posts = get_all_post('6883966016', '1076036883966016')
display_world(posts)