# -*- coding: utf-8 -*-
import logging
import random
import re
import time
import datetime

import scrapy
import json

from scrapy import Request, FormRequest

from gaoxiaoYQ.items import AuthorAndWeiboItem, CommenterItem, WeiboItem, HistoryWeiboItem
from gaoxiaoYQ.spiders import colleges, aspects

logger = logging.getLogger(__name__)

conment_url = "https://m.weibo.cn/comments/hotflow"


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']

    def start_requests(self):
        for college_key in colleges:
            for college in colleges[college_key]:
                for key, values in aspects.items():
                    for value in values:
                        key_word = college + " " + value
                        for i in range(1, 3):
                            # 这里注意，不能使用中文，要改变的变量只有&kw。
                            start_url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%{}&page_type=searchall&page={}'.format(
                                key_word, i)
                            request = Request(start_url, callback=self.parse, meta={"aspect": key, "college": college},
                                              dont_filter=False)
                            yield request

    def parse(self, response):
        meta = response.meta
        text = response.text
        res_dic = json.loads(text)
        if res_dic['ok'] == 1:
            data = res_dic['data']
            cards = data['cards']
            for card in cards:
                weibo_item = WeiboItem()
                WeiboSpider.aspect = meta['aspect']
                WeiboSpider.college = meta['college']
                if card['card_type'] == 9:
                    scheme = card['scheme']  # 微博链接
                    mblog = card['mblog']
                    weibo_item['mblog'] = mblog
                    weibo_item['scheme'] = scheme
                    # 微博作者
                    author = mblog['user']
                    weibo_item['author'] = author
                    # 提取评论使用
                    mblog_id = mblog['id']
                    mblog_mid = mblog['mid']

                    weibo_item['weibo_id'] = mblog_id

                    params = {
                        'id': str(mblog_id),
                        'mid': str(mblog_mid),
                        'max_id_type': str(0)
                    }

                    meta['weibo_id'] = mblog_id
                    meta['params'] = params
                    yield weibo_item

                    yield FormRequest(
                        url=conment_url,
                        callback=self.parse_comment,
                        formdata=params,
                        meta=meta,
                        method='GET',
                        dont_filter=False
                    )

                    history_weibo_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid=107603{}".format(
                        author['id'], author['id'])

                    yield Request(
                        url=history_weibo_url,
                        callback=self.parse_history_weibo,
                        meta={"author_id_id": author['id']}
                    )

    def parse_comment(self, response):
        comment_item = CommenterItem()
        text = json.loads(response.text)
        meta = response.meta

        if 'data' in text.keys():
            comment_data_list = text['data']
            comment_data_list.keys()
            max_id = comment_data_list['max_id']
            params = response.meta['params']
            params['max_id'] = str(max_id)
            meta['params'] = params

            for comment in comment_data_list['data']:
                comment_author = comment['user']
                # 评论发表时间
                comment_created_at = comment['created_at']
                # 评论者昵称
                comment_item['comment_id'] = comment_author['screen_name']
                comment_item['comment_id_id'] = comment_author['id']
                # 评论者头像
                comment_item['comment_avatar'] = comment_author['avatar_hd']
                # 评论者性别
                comment_item['comment_gender'] = comment_author['gender']
                # 评论内容
                comment_item['comment_content'] = comment['text']

                comment_item['like_count'] = comment['like_count']
                # 评论时间
                comment_item['comment_created_at'] = comment_created_at
                comment_item['weibo_id'] = meta['weibo_id']

                WeiboSpider.college = response.meta['college']
                WeiboSpider.aspect = response.meta['aspect']
                yield comment_item

            yield FormRequest(
                conment_url,
                callback=self.parse_comment,
                formdata=params,
                meta=meta,
                dont_filter=False
            )

    # 博主历史新闻
    def parse_history_weibo(self, response):
        history_weibo_item = HistoryWeiboItem()
        text = json.loads(response.text)
        if text['ok'] == 1:
            data = text['data']
            cards = data['cards']
            for card in cards:
                if card['card_type'] == 9:
                    scheme = card['scheme']  # 微博链接
                    mblog = card['mblog']
                    # 微博作者
                    # 提取评论使用
                    history_weibo_item['scheme'] = scheme
                    # 处理时间
                    history_weibo_item['created_at'] = self.process_time(mblog['created_at'])
                    # 微博内容
                    text = mblog['text'].replace('\n', ",")
                    history_weibo_item['raw_text'] = re.sub(r"<.*?>", "", text)

                    history_weibo_item['transponds_cnt'] = mblog['reposts_count']
                    history_weibo_item['comments_cnt'] = mblog['comments_count']
                    history_weibo_item['like_cnt'] = mblog['attitudes_count']
                    history_weibo_item['weibo_id'] = mblog['id']
                    history_weibo_item['author_id_id'] = response.meta['author_id_id']

                    yield history_weibo_item

    def process_time(self, created_at):
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
        created_at = self.format_creation_time(created_at)
        return created_at

    def format_creation_time(self, time_str):
        str2 = time_str[0:-10] + time_str[-10:].split(" ")[-1]
        dt = datetime.datetime.strptime(str2, '%a %b %d %H:%M:%S %Y')
        return dt.strftime("%Y-%m-%d %H:%M:%S")
