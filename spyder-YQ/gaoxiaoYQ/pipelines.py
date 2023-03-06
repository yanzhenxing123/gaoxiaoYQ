# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime
import re
import time
from sshtunnel import SSHTunnelForwarder

import pymysql

from gaoxiaoYQ.spiders import colleges
import logging
from gaoxiaoYQ.items import AuthorAndWeiboItem, CommenterItem, WeiboItem, HistoryWeiboItem

ssh_host = "8.136.13.232"  # 堡垒机ip地址或主机名
ssh_port = 22  # 堡垒机连接mysql服务器的端口号，一般都是22，必须是数字
ssh_user = "root"  # 这是你在堡垒机上的用户名
ssh_password = "5211314Yzx"  # 这是你在堡垒机上的用户密码
mysql_host = "127.0.0.1"  # 这是你mysql服务器的主机名或ip地址
mysql_port = 3306  # 这是你mysql服务器上的端口，3306，mysql就是3306，必须是数字
mysql_user = "root"  # 这是你mysql数据库上的用户名
mysql_password = "209243"  # 这是你mysql数据库的密码
mysql_db = "gaoxiaoYQ"  # mysql服务器上的数据库名

logger = logging.getLogger(__name__)


def save_weibo_to_csv(item):
    with open('./{}.csv'.format("articles"), 'a+', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((item['weibo_id'],
                         item['raw_text'],
                         item['college'],
                         item['aspect'],)
                        )


def save_comments_to_csv(item):
    with open('./{}.csv'.format("comments"), 'a+', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((item['weibo_id'],
                         item['comment_content'],
                         ))


class GaoxiaoyqPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AuthorAndWeiboItem):
            item['college'] = spider.college
            item['aspect'] = spider.aspect
            save_weibo_to_csv(item)
        # elif isinstance(item, CommenterItem):
        #     save_comments_to_csv(item)
        return item


class MblogPipline(object):
    def process_item(self, item, spider):
        if isinstance(item, WeiboItem):
            author_and_weibo_item = AuthorAndWeiboItem()
            # 提取
            author = item['author']
            mblog = item['mblog']
            scheme = item['scheme']
            # 提取

            # 微博链接
            author_and_weibo_item['scheme'] = scheme
            # 处理时间
            author_and_weibo_item['created_at'] = self.process_time(mblog['created_at'])
            # 微博内容
            try:
                author_and_weibo_item['raw_text'] = mblog['text'].replace('\n', ",")
                author_and_weibo_item['raw_text'] = re.sub(r'<.*?>', "", author_and_weibo_item['raw_text'])
            except Exception as e:
                author_and_weibo_item['raw_text'] = ""
                logger.warning(e)

            author_and_weibo_item['transponds_cnt'] = mblog['reposts_count']
            author_and_weibo_item['comments_cnt'] = mblog['comments_count']
            author_and_weibo_item['like_cnt'] = mblog['attitudes_count']
            author_and_weibo_item['author_gender'] = author['gender']
            author_and_weibo_item['author_avatar'] = author['avatar_hd']
            author_and_weibo_item['author_id'] = author['screen_name']
            author_and_weibo_item['author_id_id'] = author['id']

            author_and_weibo_item['source'] = '微博'
            author_and_weibo_item['weibo_id'] = mblog['id']

            # 插入时间
            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
            author_and_weibo_item['insert_time'] = str(otherStyleTime)

            # logger.warning(author_and_weibo_item)

            return author_and_weibo_item

        return item

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
        created_at = format_creation_time(created_at)

        return created_at

def format_creation_time(time_str):
    str2 = time_str[0:-10] + time_str[-10:].split(" ")[-1]
    dt = datetime.datetime.strptime(str2, '%a %b %d %H:%M:%S %Y')
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class CommentPipline(object):
    def process_item(self, item, spider):
        if isinstance(item, CommenterItem):
            item['comment_content'] = self.process_content(item['comment_content'])
            item['comment_created_at'] = self.process_time(item['comment_created_at'])
            logger.warning(item)
        return item

    def process_time(self, created_at):
        created_at = format_creation_time(created_at)
        return created_at

    def process_content(self, content):
        content = re.sub(r'<.*?>', "", content)
        return content


class MysqlPipline(object):

    def __init__(self):
        # 连接ssh
        # self.server = self.get_ssh_server()
        # # # 开启server
        # self.server.start()

        # 1. 建立数据库的连接
        self.connect = self.get_connect()

        # 2. 创建一个游标cursor, 是用来操作表。
        self.cursor = self.connect.cursor()

    # 远程
    def get_ssh_server(self):
        server = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            remote_bind_address=(mysql_host, mysql_port)
        )
        return server

    # 获取数据库连接
    def get_connect(self):
        port = mysql_port
        if hasattr(self, "server"):
            port = self.server.local_bind_port
        connect = pymysql.connect(
            host=mysql_host,
            port=port,
            user=mysql_user,
            passwd=mysql_password,
            db=mysql_db
        )
        return connect

    def process_item(self, item, spider):
        # 3. 将Item数据放入数据库，默认是同步写入。
        if isinstance(item, AuthorAndWeiboItem):
            # table_name = spider.q
            table_name = 'weibo'
            # 判断数据库是否存在
            self.insert_weibo_item(table_name, item)
            # 插入用户信息
            self.insert_into_weibo_author(item)

        elif isinstance(item, CommenterItem):
            # table_name = spider.q + 'comments'
            table_name = 'comment'
            self.insert_comment_item(table_name, item)
            # 插入用户信息
            self.insert_into_comment_author(item)
        elif isinstance(item, HistoryWeiboItem):
            table_name = 'history_weibo'

            self.insert_history_weibo(table_name, item)


        return item

    def insert_into_weibo_author(self, item):
        insert_sql = """
        INSERT INTO `author` 
        (`author_id_id`, `author_id`, `author_avatar`, `author_gender`)
        VALUES 
        ('%d', '%s','%s', '%s' )""" % (
            int(item['author_id_id']),
            item['author_id'],
            item['author_avatar'],
            item['author_gender'],
        )
        try:
            self.cursor.execute(insert_sql)
        except Exception as e:
            print(e)
        # 4. 提交操作
        self.connect.commit()

    def insert_into_comment_author(self, item):
        insert_sql = """
        INSERT INTO `author` 
        (`author_id_id`, `author_id`, `author_avatar`, `author_gender`)
        VALUES 
        ('%d', '%s','%s', '%s' )""" % (
            int(item['comment_id_id']),
            item['comment_id'],
            item['comment_avatar'],
            item['comment_gender'],
        )
        try:
            self.cursor.execute(insert_sql)
        except Exception as e:
            print(e)
        # 4. 提交操作
        self.connect.commit()


    def insert_weibo_item(self, table_name, item):
        insert_sql = """
        INSERT INTO 
        `%s` 
        (weibo_id, author_id_id, author_id, author_avatar, author_gender, scheme, created_at, raw_text, comments_cnt, like_cnt, transponds_cnt, college, aspect, source) 
        VALUES 
        ('%s', '%d', '%s','%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%s', '%s')""" % (
            table_name,
            item['weibo_id'],
            int(item['author_id_id']),
            item['author_id'],
            item['author_avatar'],
            item['author_gender'],
            item['scheme'],
            item['created_at'],
            item['raw_text'],
            int(item['comments_cnt']),
            int(item['like_cnt']),
            int(item['transponds_cnt']),
            item['college'],
            item['aspect'],
            item['source'],
        )
        try:
            self.cursor.execute(insert_sql)
        except Exception as e:
            print(e)
        # 4. 提交操作
        self.connect.commit()

    def insert_comment_item(self, table_name, item):
        insert_sql = '''
        insert into `%s` (comment_id, comment_id_id, comment_avatar, comment_gender, comment_created_at, comment_content, like_count,weibo_id) values ('%s', '%d','%s', '%s', '%s', '%s', %d, '%s');
        ''' % (
            table_name,
            item['comment_id'],
            int(item['comment_id_id']),
            item['comment_avatar'],
            item['comment_gender'],
            item['comment_created_at'],
            item['comment_content'],
            item['like_count'],
            # item['college'],
            item['weibo_id'],
        )
        try:
            self.cursor.execute(insert_sql)
        except Exception as e:
            print(e, '****')
        # 4. 提交操作
        self.connect.commit()

    def insert_history_weibo(self, table_name, item):
        insert_sql = '''
        insert into 
        `%s` (`weibo_id`, `author_id_id`, `scheme`, `created_at`, `raw_text`, `transponds_cnt`, `comments_cnt`,`like_cnt`) 
        values 
        ('%s', '%d','%s', '%s', '%s', '%s', %s, '%s');
        ''' % (
            table_name,
            item['weibo_id'],
            int(item['author_id_id']),
            item['scheme'],
            # 处理时间
            item['created_at'],
            item['raw_text'],
            item['transponds_cnt'],
            item['comments_cnt'],
            item['like_cnt'],
        )
        try:
            self.cursor.execute(insert_sql)
        except Exception as e:
            print("在执行插入历史微博时出现错误:", e)
        # 4. 提交操作
        self.connect.commit()


    def is_exists(self, q):
        sql = "show tables"
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        tables_list = re.findall('(\'.*?\')', str(tables))
        tables_list = [re.sub("'", '', each) for each in tables_list]
        if q in tables_list:
            return True
        else:
            return False


    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

        if hasattr(self, "server"):
            self.server.stop()
            self.server.close()

