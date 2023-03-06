# 高校舆情大数据分析与监控平台

![image-20230306115817351](http://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/typora/202303/06/115818-439374.png)
## 前端展示

### 1. 监控大屏模块

前端代码在文件夹 `frontend` 下

![image-20230306111902722](http://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/typora/202303/06/111903-583476.png)

+ 监控大屏模块分为七个板块，分别是新闻热度展示，当前舆情总量，全国地图展示，实时新闻爬取、各高校新闻情感分析、预警监控和词云分析

+ 新闻热度展示：为用户展现热度最高的三条新闻，并展现该新闻对应的热点评论以及该新闻博主的历史新闻热度走向
+ 当前舆情展示：在大屏中间展示全国舆情总数量（若是重邮版则展示重庆邮电大学舆情总量），用户可以直接获取实时新闻舆情总量
+ 地图展示：系统在中国地图上展现各个高校的地点以及舆情量，展示最直观的舆情地域分布以及数量。
+ 实时新闻爬取：平台数据采集展示，即时间段内新闻数据爬取量
+ 各高校新闻情感分析：采用柱状图和折线图结合进行对比，展示部分高校舆情的情感情况。（若是重邮版则展现的是六大主题的舆情情感分析情况）
+ 预警监控：若出现关于高校的热度较高的舆情，则在实时爬取板块会出现预警提醒，同时也会给该用户进行邮件提醒。

### 2. 决策管理模块

![image-20230306112456335](https://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/demo1.png)

+ 决策管理主要分为三个板块，分别是各主题舆情占比、新闻列表展示、新闻个性化分析

+ 主题舆情占比：对六大主题的舆情占比进行展示

+ 新闻列表：实现对全部新闻和六大主题下的展示，同时可以筛选出正负面的新闻并进行展示。也可以展示针对重邮版的新闻。

+ 新闻个性化分析：包括博主历史新闻热度，该条评论的情感分析、评论者写别分析和新闻词云，对数据采用图表展示更加直观。



### 3. 决策报告模块

![image-20230306113031652](http://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/typora/202303/06/113032-958908.png)

![image-20230306113040316](http://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/typora/202303/06/113041-73806.png)



## 后端

### 1. 数据获取

使用Scrapy-Redis框架，spyder-YQ为爬虫代码，执行命令为：

```sh
cd spyder-YQ
python3 start.py
```



### 2. 后端执行

python版本为3.7，框架为Django，执行命令为：

```sh
pip install requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```



## 项目演示

视频演示：

https://ksdb-blogimg.oss-cn-beijing.aliyuncs.com/%E5%AA%92%E4%BD%931.mp4



