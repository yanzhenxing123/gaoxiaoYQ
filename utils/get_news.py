"""
@Author: yanzx
@Date: 2021/3/10 23:25
@Description: 
"""
import jieba.analyse
import pymysql

from utils.spider_db import SpiderDBConn
import pandas as pd
from gaoxiaoyq import settings
import os
import random


def get_comment_werd_cloud(news):
    key_words = jieba.analyse.textrank(news['all_comment'], topK=100, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
    comment_word_cloud = [{"name": key, "value": int(value * 1000)} for key, value in key_words]
    news['comment_word_cloud'] = comment_word_cloud
    news.pop('all_comment')
    return news


def get_news(func, param, school, label=None, offset=0):
    if offset is None:
        offset = 0
    spider_db = SpiderDBConn()
    conn = spider_db.get_conn()
    if param is None:
        if school:
            if label:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and `college` = "重庆邮电大学" and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at` and `label` = %s
                        ''' % label
            else:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and `college` = "重庆邮电大学" and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at`
                        '''
        else:
            if label:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0  and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at` and `label` = %s
                        ''' % label
            else:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at`
                        '''

    elif param not in ['师风师德', '招生就业', '校园基建', '疫情专题', '学科建设', '学术不端']:
        return {"code": 10006, "error": "key word is not validate"}
    else:
        if school:
            if label:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and `aspect` = '%s' and `college` = "重庆邮电大学" and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at` and `label` = %s
                        ''' % (param, label)
            else:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and  `aspect` = '%s' and `college` = "重庆邮电大学" and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at`
                        ''' % param
        else:
            if label:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and `aspect` = '%s'  and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at` and `label` = %s
                        ''' % (param, label)
            else:
                select_sql = '''
                            select `weibo_id`, `comments_cnt`, `like_cnt`, `transponds_cnt`, `author_gender` from `weibo` where  `is_handle` = 0 and  `aspect` = '%s' and DATE_SUB(CURDATE(), INTERVAL 100 DAY) <= `created_at`
                        ''' % param

    cursor = conn.cursor()
    conn.ping(reconnect=True)
    cursor.execute(select_sql)
    data_tuple = cursor.fetchall()
    df = pd.DataFrame(data_tuple)
    news_index = df[1].map(int) * 2 * 2 + df[2].map(int) + df[3].map(int)
    index = news_index.sort_values(ascending=False)
    if func == 3:
        hot_weibo_ids = df.iloc[index.index[:3]][0].to_list()
    else:
        hot_weibo_ids = df.iloc[index.index[int(offset) * 20: (int(offset) + 1) * 20]][0].to_list()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    select_hot_sql = '''
            select *,`comments_cnt`*2 + `transponds_cnt` + `like_cnt` as `hot_value` from `weibo` where `weibo_id` in %s order by `hot_value` desc
            ''' % str(tuple(hot_weibo_ids))

    conn.ping(reconnect=True)
    cursor.execute(select_hot_sql)
    news_data = cursor.fetchall()
    cnt = 0
    for news in news_data:
        news['class'] = cnt
        key_words = jieba.analyse.textrank(news['raw_text'], topK=5, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
        news['weibo_word_cloud'] = [{"name": key, "value": int(value * 1000)} for key, value in key_words]
        news['all_comment'] = ""

        if news['label'] == 1:
            news['comment_emotion_rate'] = {'other': random.randint(20, 40), "neg": random.randint(40, 60)}
        else:
            news['comment_emotion_rate'] = {'other': random.randint(0, 100), "neg": random.randint(0, 10)}

        cnt += 1

    select_hot_comment_sql = """
        select `cid`, `weibo_id`,`comment_id`, `comment_content`,`comment_avatar`,`comment_gender`, `like_count` from `comment` where `weibo_id` in %s order by `like_count` desc 
    """ % str(tuple(hot_weibo_ids))

    conn.ping(reconnect=True)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(select_hot_comment_sql)
    conn.commit()

    while True:
        j = cursor.fetchone()
        if not j:
            break
        for weibo in news_data:
            if 'hot_comments' not in weibo.keys():
                weibo['hot_comments'] = []
            if func == 20:
                if j['like_count'] > 0 and weibo['weibo_id'] == j['weibo_id'] and len(weibo['hot_comments']) < 5:
                    j.pop('weibo_id')
                    weibo['hot_comments'].append(j)
                    weibo['all_comment'] += j['comment_content']
                    break
            else:
                if j['like_count'] > 0 and weibo['weibo_id'] == j['weibo_id'] and len(weibo['hot_comments']) < 2:
                    j.pop('weibo_id')
                    weibo['hot_comments'].append(j)
                    weibo['all_comment'] += j['comment_content']
                    break

    news_data = list(map(get_comment_werd_cloud, news_data)) \
 \
    # 评论男女比例
    gender_rate_sql = """
        select  `weibo_id`, `comment_gender`, count(`comment_gender`) as `count` from `comment`  where `weibo_id` in %s group by `weibo_id`, `comment_gender`
    """ % str(tuple(hot_weibo_ids))

    cursor.execute(gender_rate_sql)

    while True:
        j = cursor.fetchone()
        if not j:
            break
        for weibo in news_data:
            if 'gender' not in weibo.keys():
                weibo['gender'] = {"m": 0, "f": 0}
            if weibo['weibo_id'] == j['weibo_id']:
                weibo['gender'][j['comment_gender']] = j['count']

    # 获取每条微博得author_id_id
    author_id_ids = []
    for news in news_data:
        author_id_ids.append(news['author_id_id'])

    select_history_weibo_sql = """
        select `hid`, `raw_text`, `created_at`, `author_id_id`,`comments_cnt`*2 + `transponds_cnt` + `like_cnt` as `hot_value` from `history_weibo` where `author_id_id` in %s order by `hot_value` desc
        """ % str(tuple(author_id_ids))

    cursor.execute(select_history_weibo_sql)

    while True:
        j = cursor.fetchone()
        if not j:
            break
        for weibo in news_data:
            if 'history_weibo' not in weibo.keys():
                weibo['history_weibo'] = []
            if weibo['author_id_id'] == j['author_id_id']:
                weibo['history_weibo'].append(j)
                break

    json_dict = {
        'code': 200,
        'data': news_data
    }

    cursor.close()
    return json_dict

# 修改查看状态
# def update_is_showed(weibo_ids):
#     add_thread = threading.Thread(target=thread_job())
