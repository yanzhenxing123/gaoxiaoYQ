# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    mblog = scrapy.Field()
    author = scrapy.Field()
    # 微博链接
    scheme = scrapy.Field()
    # 微博id
    weibo_id = scrapy.Field()


class AuthorAndWeiboItem(scrapy.Item):
    # 微博id 外键
    weibo_id = scrapy.Field()

    # 发博者名字
    author_id = scrapy.Field()

    # 发博者id
    author_id_id = scrapy.Field()
    # 发博者头像
    author_avatar = scrapy.Field()
    # 发博者年龄
    # author_age = scrapy.Field()
    # 发博者性别
    author_gender = scrapy.Field()
    # 发博者地区
    # author_area = scrapy.Field()

    # 微博链接
    scheme = scrapy.Field()
    # 发布时间
    created_at = scrapy.Field()
    # 微博正文
    raw_text = scrapy.Field()
    # 评论数
    comments_cnt = scrapy.Field()
    # 转发数
    transponds_cnt = scrapy.Field()
    # 点赞数
    like_cnt = scrapy.Field()
    # 方面
    aspect = scrapy.Field()

    # 来源
    source = scrapy.Field()
    # 本条数据插入的时间
    insert_time = scrapy.Field()

    college = scrapy.Field()


class CommenterItem(scrapy.Item):
    # 评论者id
    comment_id_id = scrapy.Field()
    # 评论者名字
    comment_id = scrapy.Field()
    # 评论发表时间
    comment_created_at = scrapy.Field()
    # 评论者头像
    comment_avatar = scrapy.Field()
    # 评论者年龄
    # commentr_age = scrapy.Field()
    # 评论者性别
    comment_gender = scrapy.Field()
    # 评论者地区
    # comment_area = scrapy.Field()

    # 评论内容
    comment_content = scrapy.Field()

    # like_count
    like_count = scrapy.Field()

    # 所属微博
    weibo_id = scrapy.Field()

    college = scrapy.Field()


class HistoryWeiboItem(scrapy.Item):
    author_id_id = scrapy.Field()
    weibo_id = scrapy.Field()
    scheme = scrapy.Field()
    created_at = scrapy.Field()
    raw_text = scrapy.Field()
    comments_cnt = scrapy.Field()
    transponds_cnt = scrapy.Field()
    like_cnt = scrapy.Field()

