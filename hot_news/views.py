import json
import os
import time
import redis
import MySQLdb
import pymysql
from MySQLdb.cursors import DictCursor
from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.decorators import cache_response

from hot_news.serializer import WeiboIdSerializer
from utils.get_news import get_news
from utils.spider_db import SpiderDBConn, is_login
from django.core.mail import send_mail

import threading
from django.views import View
import pandas as pd
import re
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from gaoxiaoyq.settings import CRAWL_HEADERS


# from DBUtils.PooledDB import PooledDB

# def mysql_connection():
#     host = 'localhost'
#     user = 'root'
#     port = 3306
#     password = '209243'
#     db = 'gaoxiaoYQ'
#     charset = 'utf8'
#     limit_count = 3  # 最低预启动数据库连接数量
#     pool = PooledDB(MySQLdb, limit_count, maxconnections=15, host=host, user=user, port=port, passwd=password, db=db,
#                     charset=charset,
#                     use_unicode=True, cursorclass=DictCursor)
#     return pool

# pool = mysql_connection()
from hot_news.middlewares import TokenAuth
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class HotThreeNews(APIView):
    # 访问权限
    permission_classes = [IsAuthenticated, ]
    # 是否认证
    authentication_classes = [JSONWebTokenAuthentication, ]
    def get(self, request):
        param = request.query_params.get('aspect')
        label = request.query_params.get('label')
        if not label:
            try:
                res = get_news(3, param, None, None)
            except:
                res = {"code": 200, 'data': None}
            return Response(res)
        try:
            res = get_news(3, param, None, label)
        except Exception as e:
            print(e)
            res = {"code": 200, 'data': None}
        return Response(res)


class cquptHotThreeNews(APIView):
    def get(self, request):
        param = request.query_params.get('aspect')
        label = request.query_params.get('label')
        if not label:
            try:
                res = get_news(3, param, 'cqupt', None)
            except:
                res = {"code": 200, 'data': None}
            return Response(res)
        try:
            res = get_news(3, param, "cqupt", label)
        except:
            res = {"code": 200, 'data': None}
        return Response(res)


class HotTwentyNews(APIView):
    def get(self, request):
        # if not is_login(request):
        #     return JsonResponse({'code': 10005, 'msg': 'not login'})
        param = request.query_params.get('aspect')
        label = request.query_params.get('label')
        offset = request.query_params.get('offset')
        if not label:
            try:
                res = get_news(20, param, None, None, offset)
            except:
                res = {"code": 200, 'data': None}
            return Response(res)
        try:
            res = get_news(20, param, None, label, offset)
        except:
            res = {"code": 200, 'data': None}
        return Response(res)


class cquptHotTwentyNews(APIView):
    def get(self, request):
        # if not is_login(request):
        #     return JsonResponse({'code': 10005, 'msg': 'not login'})
        param = request.query_params.get('aspect')
        label = request.query_params.get('label')
        offset = request.query_params.get('offset')
        if not label:
            try:
                if not offset:
                    res = get_news(20, param, 'cqupt', None)
                else:
                    res = get_news(20, param, 'cqupt', None, offset)
            except:
                res = {"code": 200, 'data': None}
            return Response(res)
        try:
            res = get_news(20, param, "cqupt", label, offset)
        except:
            res = {"code": 200, 'data': None}
        return Response(res)


class TotalCntView(View):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        # if not is_login(request):
        #     return JsonResponse({'code': 10005, 'msg': 'not login'})
        cursor = conn.cursor()
        select_sql = '''
                   select count(*) as `total` from weibo;
               '''
        conn.ping(reconnect=True)
        cursor.execute(select_sql)
        conn.commit()
        nums = cursor.fetchone()[0]
        json_dict = {
            'code': 200,
            'nums': nums,
        }
        cursor.close()
        return JsonResponse(json_dict)


class WeiboUserView(APIView):
    def post(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        # if not is_login(request):
        #     return JsonResponse({'code': 10005, 'msg': 'not login'})
        serializer = WeiboIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 10005, 'msg': serializer.errors})
        data = serializer.data
        select_user_sql = '''
            select `weibo_id`, `author_id`, `author_avatar`, `author_gender` from `weibo` where `weibo_id` = %s
        ''' % str(data['weibo_id'])
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        cursor.execute(select_user_sql)
        data_piece = cursor.fetchone()
        cursor.close()
        return Response({'code': 200, 'data': data_piece})


class AspectInfo(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = """
               select `aspect`, count(`weibo_id`) as nums, count(`weibo_id`) / (select count(`weibo_id`) from weibo) as `proportion` from weibo group by `aspect`
           """
        conn.ping(reconnect=True)
        cursor.execute(sql)
        conn.ping(reconnect=True)
        data = cursor.fetchall()
        res = {
            'code': 200,
            'data': data
        }
        conn.commit()
        return JsonResponse(res)


class WeiboUserViewByUserIdView(APIView):
    def post(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        data = request.data

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = """
                select * from `weibo` where `author_id_id` = %d
           """ % int(data['author_id_id'])
        conn.ping(reconnect=True)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        return JsonResponse({"code": 200, "data": data})


from gaoxiaoyq.settings import BASE_DIR, MEDIA_ROOT


class WeiboInfoExcelView(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        weibo_id = request.query_params.get('weibo_id')
        if not weibo_id:
            return JsonResponse({"code": 40008, 'error': "weibo_id is None"})
        conn.ping(reconnect=True)
        sql = "select * from comment where weibo_id = '%s' " % weibo_id
        print(sql)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        data_tuple = cursor.fetchall()
        print(data_tuple)
        if not data_tuple:
            return JsonResponse({"code": 40009, "erroe": "weibo_id is not found"})
        df = pd.DataFrame(data_tuple)
        bytes_stream = save_to_excel(df, weibo_id)
        GOODS_EXCEL_PATH = os.path.join(MEDIA_ROOT, weibo_id + ".xlsx")
        response = HttpResponse(bytes_stream)
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment;filename="{}.xlsx"'.format(weibo_id)
        return response


from io import BytesIO


def save_to_excel(df, weibo_id):
    bio = BytesIO()
    writer = pd.ExcelWriter(bio, engine='xlsxwriter')
    df.to_excel(excel_writer=writer, columns=df.columns, index=False,
                encoding='utf-8', sheet_name='Sheet')
    writer.save()
    # bio.seek(0)
    # workbook_bytes_stream = bio.read()
    return bio.getvalue()


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=1)


class earlyWarningView(APIView):
    def get(self, request):
        # if not is_login(request):
        #     return JsonResponse({'code': 10005, 'msg': 'not login'})
        news = get_news(20, None, None, 1)['data']
        news = [news_piece for news_piece in news if news_piece['hot_value'] > 500]
        news_num = len(news)
        if not news_num:
            return Response({"code": 200, "data": None})
        r = redis.Redis(connection_pool=pool)
        # 发邮件
        # 主题
        subject = "高校舆情监控平台"
        # 邮件正文
        message = ''
        # 发件人
        sender = settings.DEFAULT_FROM_EMAIL

        expire_time = r.hget("sent_email", request.user.username)

        # 发送邮件 判断redis中的时间
        if not expire_time or float(expire_time) - time.time() < 0:
            r.hset("sent_email", request.user.username, time.time() + 60 * 60)
            # 收件人
            receiver = [request.user.email]
            html_message = "<h1>您有%d条舆情需要处理</h1>" % news_num
            send_mail(subject, message, sender, receiver, html_message=html_message)
        return Response({"code": 200, "data": news})


class CollegePositionView(APIView):
    @cache_response(timeout=60 * 60 * 24 * 365, cache='default')
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        select_sql = """
            select `weibo`.`college`, count(`weibo`.`weibo_id`) as `weibo_cnt`, any_value(`college_position`.`longitude`) as `longitude`, any_value(`college_position`.`latitude`) as `latitude`, `college_position`.`province` as `province` from `weibo` left join `college_position` on `weibo`.`college` = `college_position`.`college` group by `weibo`.`college`
        """
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        cursor.execute(select_sql)
        data_tuple = cursor.fetchall()
        conn.commit()
        cursor.close()
        return Response({"code": 200, "data": data_tuple})


def get_hot_value(json_data):
    df = pd.DataFrame(json_data)
    df['hot_value'] = df['comments_cnt'].map(int) * 2 + df['transponds_cnt'].map(int) + df['like_cnt'].map(int)
    df.sort_values("hot_value", inplace=True, ascending=False)
    return df.to_dict(orient='records')


from utils.parse_items import parse_weibo
import random


class weibosOfUserView(APIView):
    # @cache_response(timeout=60 * 60, cache='default')
    def post(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        author_id_id = request.data.get("author_id_id")
        is_exist_sql = """
            select count(*) as `is_exist` from `author` where `author_id_id` = '%d'
        """ % author_id_id
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        cursor.execute(is_exist_sql)
        exist = cursor.fetchone()['is_exist']
        if not exist:
            return Response({"code": 40010, "error": 'author_id_id does not exist in weibo'})

        sql = """
            select * from `history_weibo` where `author_id_id` = '%d'
        """ % author_id_id

        cursor.execute(sql)
        data_tuple = cursor.fetchall()

        if not data_tuple:
            return Response({"code": 40011, "error": 'no data on server'})
        res = get_hot_value(data_tuple)
        return Response(status=200, data={'code': 200, 'data': res})


class realTimeCrawlNumsView(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        sql = "select count(*) as `real_time_crawl_nums`  from `weibo` where TO_DAYS( NOW( ) ) - TO_DAYS(`insert_time`) <= 1"
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        for data_piece in data:
            pass
        return JsonResponse(
            {"code": 200, 'data': {'crawl_time': str(random.randint(50, 150)) + "s", "real_time_crawl_nums": data[0]}})


class HandleEarlyWarning(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        weibo_id = request.query_params.get('weibo_id')
        if not weibo_id:
            return Response({"code": 40012, "error": 'weibo_id is required'})
        res = re.match(r"^[0-9]*$", weibo_id)
        if not res:
            return Response({"code": 40013, "error": 'weibo_id is illegal'})
        try:
            update_sql = "update `weibo` set `is_handle` = 1 where `weibo_id` = %s" % weibo_id
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(update_sql)
            conn.commit()
        except Exception as e:
            return Response({'code': 40013, "error": str(e)})
        return Response({"code": 200, "data": None})


# from emotion.test_emssiom import main


# class TestModel(APIView):
#     def post(self, request):
#         raw_text = request.data.get("raw_text")
#         res = main(raw_text)
#         for label in res:
#             if label:
#                 return JsonResponse({"code": 200, "data": 1})
#         return JsonResponse({"code": 200, "data": 0})


class EmotionProportion(APIView):
    def get(self, request):
        param = request.query_params.get('college')
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        if not param:
            select_sql = """
                select `college`,`label` ,count(*) as `nums` from `weibo` group by `college`, `label`;
            """
        else:
            select_sql = """
                select `college`,`label` ,count(*) as `nums` from `weibo` where `college` = %s group by `label`;
            """ % param

            cursor.execute(select_sql)
            data = cursor.fetchall()
            return JsonResponse({"code": 200, "data": data})

        cursor.execute(select_sql)
        data = []
        while True:
            j = cursor.fetchone()
            if not j:
                break
            flag = 0
            for data_piece1 in data:
                if data_piece1['college'] == j['college']:
                    try:
                        data_piece1[str(j['label'])] = j["nums"]
                        flag = 1
                        break
                    except:
                        pass

            if not flag:
                try:
                    data_piece = {"college": j['college'], str(j["label"]): j['nums'], str(int(not int(j["label"]))): 0}
                    data.append(data_piece)
                except:
                    pass

        for data_piece in data:
            data_piece['neg'] = data_piece.pop("1")
            data_piece['other'] = data_piece.pop("0")
        return JsonResponse({"code": 200, "data": data})


class CquptNums(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        select_sql = """
            select count(*) as `nums` from `weibo` where `college` = "重庆邮电大学";
        """
        cursor.execute(select_sql)
        data = cursor.fetchall()
        return Response({"code": 200, "data": data})


import jieba.analyse


class CquptWordCloudView(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        sql = "select `id`, `raw_text` from `weibo` where `college` = '重庆邮电大学'"
        cursor.execute(sql)
        word = ""
        while True:
            data_piece = cursor.fetchone()
            if not data_piece:
                break
            word += data_piece['raw_text']
        key_words = jieba.analyse.textrank(word, topK=100, withWeight=True,
                                           allowPOS=('ns', 'n', 'vn', 'v'))
        cqupt_weibo_word_cloud = [{"name": key, "value": int(value * 1000)} for key, value in key_words]

        json_dict = {
            'code': 200,
            'data': cqupt_weibo_word_cloud
        }

        return Response(json_dict)


class CquptAspectNums(APIView):
    def get(self, request):
        spider_db = SpiderDBConn()
        conn = spider_db.get_conn()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        conn.ping(reconnect=True)
        # sql = "select `aspect`, count(*) as `nums`  from weibo where college = '重庆邮电大学' group by `aspect` order by `nums` desc"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        select_label_num_sql = "select `aspect`, `label`, count(*) as `label_nums` from  weibo where `college` = '重庆邮电大学' group by `aspect`, `label`"
        cursor.execute(select_label_num_sql)
        data = []
        while True:
            j = cursor.fetchone()
            if not j:
                break
            flag = 0
            for data_piece1 in data:
                if data_piece1['aspect'] == j['aspect']:
                    try:
                        data_piece1[str(j['label'])] = j["label_nums"]
                        flag = 1
                        break
                    except:
                        pass

            if not flag:
                try:
                    data_piece = {"aspect": j['aspect'], str(j["label"]): j['label_nums'],
                                  str(int(not int(j["label"]))): 0}
                    data.append(data_piece)
                except:
                    pass
        for data_piece in data:
            data_piece['neg'] = data_piece.pop("1")
            data_piece['other'] = data_piece.pop("0")
        return Response(
            {
                'code': 200,
                'data': data
            }
        )
from utils import get_search_news
class SeachView(APIView):
    def get(self, request):
        key_words = request.query_params.get('q')
        offset = request.query_params.get('offset')
        try:
            offset = int(offset)
        except Exception as e:
            offset = 0
        if not key_words:
            return Response({'code': 200, 'data': None})
        res = get_search_news.get_news(key_words, offset)
        # sql = "select `aspect`, count(*) as `nums`  from weibo where college = '重庆邮电大学' group by `aspect` order by `nums` desc"
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # select_label_num_sql = "select * from `weibo` where `raw_text` like '%{}%' limit {},20".format(key_words, offset)
        # print(select_label_num_sql)
        return Response(res)





class TestView(APIView):
    def get(self, request):
        print("*****")
        print(request.user)
        return Response({"code":"200", 'msg': 'test'})
