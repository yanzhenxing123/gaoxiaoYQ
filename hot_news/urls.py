from . import views
from django.urls import path

app_name = 'hot_news'


urlpatterns = [
    path('hot3/', views.HotThreeNews.as_view(), name='detail'),
    path('hot20/', views.HotTwentyNews.as_view(), name='detail20'),
    path('nums/', views.TotalCntView.as_view(), name='total_nums'),
    path('user/', views.WeiboUserView.as_view(), name='weibo_user'),
    path('aspectInfo/', views.AspectInfo.as_view(), name='aspectInfo'),
    path('ByUserid/', views.WeiboUserViewByUserIdView.as_view(), name='weibo_user_by_user_id'),
    path('exportExcel/', views.WeiboInfoExcelView.as_view(), name='exportExcel'),
    path('earlyWarning/', views.earlyWarningView.as_view(), name='earlyWarning'),
    path('collgePosition/', views.CollegePositionView.as_view(), name='college_postion'),
    path('weibosOfUser/', views.weibosOfUserView.as_view(), name='weibosOfUser'),
    path('realTimeCrawlNums/', views.realTimeCrawlNumsView.as_view(), name='realTimeCrawlNums'),
    path('cquptHot3/', views.cquptHotThreeNews.as_view(), name='cquptHot3'),
    path('cquptHot20/', views.cquptHotTwentyNews.as_view(), name='cquptHot20'),
    path('HandleEarlyWarning/', views.HandleEarlyWarning.as_view(), name='handleEarlyWarning'),
    # path('testModel/', views.TestModel.as_view(), name='testModel'),
    path('emotionProportion/', views.EmotionProportion.as_view(), name='emotionProportion'),
    path('cquptNums/', views.CquptNums.as_view(), name='cquptNums'),
    path('cquptWordCloud/', views.CquptWordCloudView.as_view(), name='cquptWordCloud'),
    path('cquptAspectNums/', views.CquptAspectNums.as_view(), name='cquptAspectNums'),
    path('search/', views.SeachView.as_view(), name='search'),
    path('test/', views.TestView.as_view(), name='test'),

]
