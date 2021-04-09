"""
@Author: yanzx
@Date: 2020/11/29 15:18
@Description: 
"""
import pymysql

mysql_host = "127.0.0.1"  # 这是你mysql服务器的主机名或ip地址
mysql_port = 3306  # 这是你mysql服务器上的端口，3306，mysql就是3306，必须是数字
mysql_user = "root"  # 这是你mysql数据库上的用户名
mysql_password = "209243"  # 这是你mysql数据库的密码
mysql_db = "gaoxiaoYQ"  # mysql服务器上的数据库名


class SpiderDBConn():
    def __init__(self):
        self.connect = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,

            passwd=mysql_password,
            db=mysql_db
        )
        # self.cursor = self.connect.cursor()

    def get_conn(self):
        return self.connect

    def __del__(self):
        print("this connection close")
        if hasattr(SpiderDBConn, 'connect'):

            self.connect.close()

# 判断用户是否登录
def is_login(request):
    return request.user.is_authenticated



