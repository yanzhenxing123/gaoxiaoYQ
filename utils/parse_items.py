"""
@Author: yanzx
@Date: 2020/12/10 17:35
@Description: 
"""
import datetime
import json
import re


def parse_weibo(text):
    res_dic = json.loads(text)
    result = []
    if res_dic['ok'] == 1:
        data = res_dic['data']
        cards = data['cards']
        for card in cards:
            if card['card_type'] == 9:
                print(card)
                author_and_weibo_item = {}
                scheme = card['scheme']  # 微博链接
                mblog = card['mblog']
                # 微博作者
                # 提取评论使用
                author_and_weibo_item['scheme'] = scheme
                # 处理时间
                author_and_weibo_item['created_at'] = process_time(mblog['created_at'])
                # 微博内容
                text = mblog['text'].replace('\n', ",")
                author_and_weibo_item['raw_text'] = re.sub(r"<.*?>", "", text)

                author_and_weibo_item['transponds_cnt'] = mblog['reposts_count']
                author_and_weibo_item['comments_cnt'] = mblog['comments_count']
                author_and_weibo_item['like_cnt'] = mblog['attitudes_count']
                result.append(author_and_weibo_item)
    return result

def process_time(created_at):
    today = datetime.date.today()
    if '前' in created_at:
        created_at = str(today)
    elif '昨天' in created_at:
        oneday = datetime.timedelta(days=1)
        yesterday = today - oneday
        created_at = str(yesterday)
    elif len(created_at) == 5:
        date = '2020-' + created_at
        created_at = date
    return created_at