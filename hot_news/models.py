# from django.db import models
# from django.utils import timezone
#
# # Create your models here.
#
# class Href(models.Model):
#     weibo_id = models.CharField(max_length=20, primary_key=True)
#     author_id = models.CharField(max_length=255)
#     author_avatar = models.CharField(max_length=255)
#     author_gender = models.CharField(max_length=10)
#     scheme = models.CharField(max_length=255)
#     created_at = models.DateField()
#     raw_text = models.TextField()
#     comments_cnt = models.CharField(max_length=255)
#     like_cnt = models.CharField(max_length=255)
#     source = models.CharField(max_length=255)
#     insert_time = models.DateTimeField(default=timezone.now)
#     #
#     # class Meta:
#     #     app_label = 'spider'
